#Agents_original
import autogen
from typing import Dict, Any, Optional
import re

def extract_diagnosis(content: str) -> Optional[str]:
    """
    Safely extract diagnosis from doctor's message.
    
    Args:
        content: The message content from the doctor
        
    Returns:
        The extracted diagnosis or None if not found
    """
    try:
        # Look for the diagnosis pattern
        match = re.search(r'DIAGNOSIS READY:\s*(.*?)(?:\n|$)', content, re.IGNORECASE)
        if match:
            diagnosis = match.group(1).strip()
            # Basic validation - ensure it's not empty or just asterisks
            if diagnosis and not all(c == '*' for c in diagnosis):
                return diagnosis
    except Exception as e:
        print(f"Error extracting diagnosis: {e}")
    return None

def process_single_case(test_case: Dict[str, Any], doctor_config: Dict[str, Any], other_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single medical case using multiple AI agents.
    
    Args:
        test_case: Dictionary containing the medical case information
        doctor_config: Configuration for the doctor agent
        other_config: Configuration for other agents
        
    Returns:
        Dictionary containing the case results
    """
    doctor_system_message = f"""
    You are a doctor named Dr Agent, working-up a patient with the goal of finding the diagnosis. You can only respond in dialogue (text, no additional formatting)
    Each turn, you can do only ONE of the following:
    1. Ask a question to the patient for any relevant history. (only one question at a time)
    2. request to perform a specific examination and elicit signs using the format "REQUEST EXAMINATION FINDING: [specific examination]". For example, "REQUEST EXAMINATION FINDING: assess the JVP".
    3. request to perform specific imaging or laboratory tests using the format "REQUEST TESTS: [test]". For example, "REQUEST TESTS: chest x-ray". If a result is not available continue the consult without this information.
    4. If you have gathered all the information you need, output "DIAGNOSIS READY: [diagnosis here]". Be confident and provide a specific diagnosis. Explain your reasoning for the diagnosis.
    """

    patient_system_message = f"""
    Act as a patient who is being assessed by a doctor. Answer questions you are asked based on the following information:
    {test_case["OSCE_Examination"]["Patient_Actor"]}
    Respond in colloquial, non-jargon language that a non-medical person will speak in. 
    Your answer should be a direct response to the question you have been asked. Do not volunteer any additional information.
    """

    measurement_system_message = f"""
    You are a clinical assistant who has responds in dialogue to the doctor's request for information. Below are all the patient's physical examination findings and test results you have: 
    {test_case["OSCE_Examination"]["Physical_Examination_Findings"]}
    {test_case["OSCE_Examination"]["Test_Results"]}
    Respond in simple text format. Do not use json or other data structures.
    Do not volunteer any additional information that the doctor has not asked for.
    Otherwise, respond with "NO INFORMATION"
    """

    grader_system_message = f"""
    The correct diagnosis is:
    {test_case["OSCE_Examination"]["Correct_Diagnosis"]}
    Is this the same as the doctor's diagnosis? Please respond with "YES" or "NO". Explain your reasoning. 
    If the doctor's diagnosis is more specific than the correct diagnosis, consider it correct.
    After your output, please respond with "TERMINATE"
    """

    # Add agent descriptions that won't leak information
    doctor_description = "Doctor - Medical professional who asks the patient questions, requests examinations and tests, and makes a diagnosis."
    patient_description = "Patient - Person with medical concerns who answers the doctor's questions about symptoms and history."
    measurement_description = "MeasurementAssistant - Clinical assistant who provides examination findings and test results when requested."
    grader_description = "Grader - Evaluator who only speaks after the doctor makes a diagnosis with 'DIAGNOSIS READY:'."

    # Create the agents
    doctor = autogen.AssistantAgent(
        name="Doctor",
        system_message=doctor_system_message,
        description=doctor_description,
        llm_config=doctor_config
    )

    patient = autogen.AssistantAgent(
        name="Patient",
        system_message=patient_system_message,
        description=patient_description,
        llm_config=other_config
    )

    measurement_assistant = autogen.AssistantAgent(
        name="MeasurementAssistant",
        system_message=measurement_system_message,
        description=measurement_description,
        llm_config=other_config
    )

    grader = autogen.AssistantAgent(
        name="Grader",
        system_message=grader_system_message,
        description=grader_description,
        llm_config=other_config,
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper()
    )

    # Define a custom speaker selection function that follows our conversation flow
    def custom_speaker_selection(last_speaker, groupchat):
        messages = groupchat.messages
        if not messages or len(messages) == 0:
            return groupchat.agent_by_name("Patient")
        
        # Get the last message - in autogen format
        last_message = messages[-1]
        # The sender is passed as the last_speaker parameter
        sender_name = last_speaker.name if last_speaker else "None"
        # Content is directly in the message
        message_text = last_message.get("content", "")
        
        # Check for termination conditions
        if "TERMINATE" in message_text.upper() or message_text.lower().strip() == "exit":
            return None
        
        # Handle special examination or test requests
        if "REQUEST EXAMINATION FINDING:" in message_text or "REQUEST TESTS:" in message_text:
            return groupchat.agent_by_name("MeasurementAssistant")
        
        # Diagnosis handling - must be exact format
        if "DIAGNOSIS READY:" in message_text and sender_name == "Doctor":
            return groupchat.agent_by_name("Grader")
        
        # After grader speaks
        if sender_name == "Grader":
            return None
        
        # Normal conversation flow
        if sender_name == "Doctor":
            return groupchat.agent_by_name("Patient")
        elif sender_name == "Patient":
            return groupchat.agent_by_name("Doctor")
        elif sender_name == "MeasurementAssistant":
            return groupchat.agent_by_name("Doctor")
        
        return None

    # Create the group chat
    groupchat = autogen.GroupChat(
        agents=[doctor, patient, measurement_assistant, grader],
        messages=[],
        allow_repeat_speaker=False,
        max_round=50,
        speaker_selection_method=custom_speaker_selection
    )

    # Create the manager
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=other_config
    )

    # Start the conversation
    doctor.initiate_chat(
        manager,
        message="Hello, I'm Dr. Agent. What can I do to help you today?",
    )

    # Format conversation and extract results
    conversation_log = ""
    doctor_diagnosis = None
    is_correct = False

    for message in groupchat.messages:
        sender = message.get("name", "Unknown")
        content = message.get("content", "")
        conversation_log += f"{sender}: {content}\n\n"
        
        # Extract doctor's diagnosis with improved safety
        if sender == "Doctor":
            extracted_diagnosis = extract_diagnosis(content)
            if extracted_diagnosis:
                doctor_diagnosis = extracted_diagnosis
        
        # Check if diagnosis was correct with improved safety
        if sender == "Grader":
            is_correct = "YES" in content.upper() and doctor_diagnosis is not None

    # Validate the results before returning
    if not doctor_diagnosis:
        print("Warning: No valid diagnosis was extracted from the conversation")
        doctor_diagnosis = "NO DIAGNOSIS PROVIDED"

    return {
        'correct_diagnosis': test_case["OSCE_Examination"]["Correct_Diagnosis"],
        'doctor_diagnosis': doctor_diagnosis,
        'is_correct': is_correct,
        'conversation_log': conversation_log
    }

def process_single_case_streaming(test_case: Dict[str, Any], doctor_config: Dict[str, Any], other_config: Dict[str, Any]):
    """
    Process a single medical case using multiple AI agents, yielding messages as they occur.
    
    Args:
        test_case: Dictionary containing the medical case information
        doctor_config: Configuration for the doctor agent
        other_config: Configuration for other agents
        
    Yields:
        str: Formatted messages from the agent conversation
    """
    doctor_system_message = f"""
    You are a doctor named Dr Agent, working-up a patient with the goal of finding the diagnosis. 
    Each turn, you can do only ONE of the following:
    1. Ask a question to the patient for any relevant history. (only one question at a time)
    2. request to perform a specific examination and elicit signs using the format "REQUEST EXAMINATION FINDING: [specific examination]". For example, "REQUEST EXAMINATION FINDING: assess the JVP".
    3. request to perform specific imaging or laboratory tests using the format "REQUEST TESTS: [test]". For example, "REQUEST TESTS: chest x-ray". If a result is not available continue the consult without this information.
    4. If you have gathered all the information you need, output "DIAGNOSIS READY: [diagnosis here]". Be confident and provide a specific diagnosis. Explain your reasoning for the diagnosis.
    """

    patient_system_message = f"""
    Act as a patient who is being assessed by a doctor. Answer questions you are asked based on the following information:
    {test_case["OSCE_Examination"]["Patient_Actor"]}
    Respond in colloquial, non-jargon language that a non-medical person will speak in. 
    Your answer should be a direct response to the question you have been asked. Do not volunteer any additional information.
    """

    measurement_system_message = f"""
    You are a clinical assistant who has responds in dialogue to the doctor's request for information. Below are all the patient's physical examination findings and test results you have: 
    {test_case["OSCE_Examination"]["Physical_Examination_Findings"]}
    {test_case["OSCE_Examination"]["Test_Results"]}
    Respond in simple text format. Do not use json or other data structures.
    Do not volunteer any additional information that the doctor has not asked for.
    Otherwise, respond with "NO INFORMATION"
    """

    grader_system_message = f"""
    The correct diagnosis is:
    {test_case["OSCE_Examination"]["Correct_Diagnosis"]}
    Is this the same as the doctor's diagnosis? Please respond with "YES" or "NO". Explain your reasoning. 
    If the doctor's diagnosis is more specific than the correct diagnosis, consider it correct.
    After your output, please respond with "TERMINATE"
    """

    doctor_description = "Doctor - Medical professional who asks the patient questions, requests examinations and tests, and makes a diagnosis."
    patient_description = "Patient - Person with medical concerns who answers the doctor's questions about symptoms and history."
    measurement_description = "MeasurementAssistant - Clinical assistant who provides examination findings and test results when requested."
    grader_description = "Grader - Evaluator who only speaks after the doctor makes a diagnosis with 'DIAGNOSIS READY:'."

    doctor = autogen.AssistantAgent(
        name="Doctor",
        system_message=doctor_system_message,
        description=doctor_description,
        llm_config=doctor_config
    )

    patient = autogen.AssistantAgent(
        name="Patient",
        system_message=patient_system_message,
        description=patient_description,
        llm_config=other_config
    )

    measurement_assistant = autogen.AssistantAgent(
        name="MeasurementAssistant",
        system_message=measurement_system_message,
        description=measurement_description,
        llm_config=other_config
    )

    grader = autogen.AssistantAgent(
        name="Grader",
        system_message=grader_system_message,
        description=grader_description,
        llm_config=other_config,
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper()
    )

    def custom_speaker_selection_streaming(last_speaker, groupchat):
        messages = groupchat.messages
        if not messages or len(messages) == 0:
            return groupchat.agent_by_name("Patient")
        
        last_message = messages[-1]
        sender_name = last_speaker.name if last_speaker else "None"
        message_text = last_message.get("content", "")
        
        if "TERMINATE" in message_text.upper() or message_text.lower().strip() == "exit":
            return None
        
        if "REQUEST EXAMINATION FINDING:" in message_text or "REQUEST TESTS:" in message_text:
            return groupchat.agent_by_name("MeasurementAssistant")
        
        if "DIAGNOSIS READY:" in message_text and sender_name == "Doctor":
            return groupchat.agent_by_name("Grader")
        
        if sender_name == "Grader":
            return None
        
        if sender_name == "Doctor":
            return groupchat.agent_by_name("Patient")
        elif sender_name == "Patient":
            return groupchat.agent_by_name("Doctor")
        elif sender_name == "MeasurementAssistant":
            return groupchat.agent_by_name("Doctor")
        
        return None

    groupchat = autogen.GroupChat(
        agents=[doctor, patient, measurement_assistant, grader],
        messages=[],
        allow_repeat_speaker=False,
        max_round=50,
        speaker_selection_method=custom_speaker_selection_streaming
    )

    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=other_config
    )

    current_speaker = doctor
    message_content = "Hello, I'm Dr. Agent. What can I do to help you today?"
    initial_message = {"name": current_speaker.name, "content": message_content}
    groupchat.messages.append(initial_message)
    # Yield the initial message in the standard dictionary format
    yield {"type": "conversation", "name": initial_message['name'], "content": initial_message['content']}

    max_turns = 50
    for i in range(max_turns):
        print(f"\n--- Turn {i+1} ---") # DEBUG
        print(f"Current Speaker: {current_speaker.name}") # DEBUG
        print(f"Groupchat Messages ({len(groupchat.messages)}): {groupchat.messages[-3:]}") # DEBUG: Show last few messages
        
        next_speaker = custom_speaker_selection_streaming(current_speaker, groupchat)
        print(f"Selected Next Speaker: {next_speaker.name if next_speaker else 'None'}") # DEBUG
        
        if next_speaker is None:
            # Yield simulation end reason as INFO
            yield "INFO:Simulation ended by speaker selection."
            break
        
        # Let the next speaker generate a reply
        try:
            print(f"Generating reply from: {next_speaker.name}") # DEBUG
            
            # Convert messages to the expected format for generate_reply
            # Map current speaker to 'user' and next speaker (recipient) to 'assistant' from POV of next_speaker
            formatted_messages = []
            for msg in groupchat.messages:
                sender_name = msg.get('name')
                content = msg.get('content', '')
                
                if sender_name == next_speaker.name:
                    # Messages from the agent *about to speak* are considered 'assistant' in its history
                    role = "assistant"
                else:
                    # Messages from other agents are considered 'user' input to the agent about to speak
                    role = "user"
                    
                formatted_messages.append({"role": role, "content": content})
            
            print(f"Formatted messages for {next_speaker.name}: {formatted_messages[-3:]}") # DEBUG
            
            # Explicitly pass the *formatted* message history to the agent
            # We don't need the 'sender' argument if history is formatted correctly with user/assistant roles
            reply = next_speaker.generate_reply(messages=formatted_messages)
            print(f"Raw Reply from {next_speaker.name}: {reply}") # DEBUG
        except Exception as e:
            print(f"ERROR during generate_reply: {e}") # DEBUG
            yield f"ERROR:Error generating reply from {next_speaker.name}: {e}"
            # yield "[Simulation finished.]" # Redundant with CASE_PROCESSING_COMPLETE
            break # Stop simulation on error
        
        if reply is None: # Could happen if agent decides not to reply
             yield f"INFO:{next_speaker.name} did not provide a reply. Ending simulation."
             break

        # Store and yield the reply
        # Autogen typically returns dict or string, need to handle both
        if isinstance(reply, dict):
            reply_content = reply.get("content", "")
            reply_message = {"name": next_speaker.name, "content": reply_content}
        elif isinstance(reply, str):
            reply_content = reply
            reply_message = {"name": next_speaker.name, "content": reply_content}
        else:
            print(f"Unexpected reply format: {type(reply)}") # DEBUG
            yield f"ERROR:Unexpected reply format from {next_speaker.name}. Ending simulation."
            break
            
        groupchat.messages.append(reply_message)
        # Yield structured data instead of pre-formatted HTML
        yield {"type": "conversation", "name": reply_message['name'], "content": reply_message['content']}

        # Update current speaker
        current_speaker = next_speaker

        # Check for termination condition from Grader
        if current_speaker.name == "Grader" and "TERMINATE" in reply_content.upper():
             yield "INFO:Grader signaled termination."
             break
    else:
        yield "INFO:Simulation reached maximum turns."

    doctor_diagnosis = None
    is_correct = False
    correct_diagnosis_text = test_case["OSCE_Examination"]["Correct_Diagnosis"]

    for message in groupchat.messages:
        sender = message.get("name", "Unknown")
        content = message.get("content", "")
        if sender == "Doctor":
            extracted_diagnosis = extract_diagnosis(content)
            if extracted_diagnosis:
                doctor_diagnosis = extracted_diagnosis
        if sender == "Grader":
            if doctor_diagnosis and "YES" in content.upper(): 
                is_correct = True

    if not doctor_diagnosis:
        doctor_diagnosis = "NO DIAGNOSIS PROVIDED"
        yield "INFO:Warning: No valid diagnosis was extracted."
        is_correct = False # Ensure correctness is False if no diagnosis

    # Yield final results with specific prefixes for parsing
    yield f"FINAL_CORRECT_DIAGNOSIS:{correct_diagnosis_text}"
    yield f"FINAL_DOCTOR_DIAGNOSIS:{doctor_diagnosis}"
    yield f"FINAL_IS_CORRECT:{is_correct}"
    yield "CASE_PROCESSING_COMPLETE" # Signal end of processing for this case 