from flask import Flask, render_template, request, Response, stream_with_context, jsonify
import json
import os
import sys
import time # Import time module
import autogen # Import autogen

# Adjust the path to include the parent directory (where multi_med might be)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the correct functions
from multi_med import get_model_config # Still needed for config
from multi_med.agents_1 import process_single_case_streaming # Import the streaming function
from multi_med.llm_config import MODEL_CONFIGS # Import model configs to get keys

# TODO: Import necessary function to call LLM directly if available
# from multi_med.some_module import call_llm_directly

app = Flask(__name__)

# Configuration - Get model names directly from the config keys
MODELS = list(MODEL_CONFIGS.keys())
CASES_DIR = 'cases'

def get_cases_files():
    """Lists available .jsonl files in the cases directory."""
    if not os.path.exists(CASES_DIR):
        return []
    return [f for f in os.listdir(CASES_DIR) if f.endswith('.jsonl')]

@app.route('/')
def index():
    """Serves the new landing page."""
    return render_template('index.html')

@app.route('/test')
def test_models():
    """Serves the test page (previously the index)."""
    cases_files = get_cases_files()
    return render_template('test.html', models=MODELS, cases_files=cases_files)

@app.route('/about')
def about():
    """Serves the About Us page."""
    return render_template('about.html')

@app.route('/leaderboard')
def leaderboard():
    """Serves the Leaderboard page."""
    return render_template('leaderboard.html')

@app.route('/methodology')
def methodology():
    """Serves the Methodology page."""
    return render_template('methodology.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Handles post-simulation chat requests."""
    data = request.get_json()
    model_name = data.get('model_name')
    history = data.get('history') # Expecting a list of conversation turns
    user_message = data.get('user_message')

    # Check if keys exist and required fields are not empty strings.
    # Allow history to be an empty list.
    if model_name is None or history is None or user_message is None or model_name == '' or user_message == '':
        return jsonify({"error": "Missing required data (model_name, history, user_message)"}), 400

    try:
        # 1. Get model configuration
        doctor_config = get_model_config(model_name)

        # 2. Construct the prompt and message history
        # TODO: Format history correctly for the specific model - autogen expects list of dicts
        # prompt_history = "\n".join([f"{turn['speaker']}: {turn['text']}" for turn in history])
        transcript = "\n".join([f"{turn['speaker']}: {turn['text']}" for turn in history])
        system_prompt = f"You are a doctor named Dr Agent. You have just finished seeing a patient and made a diagnosis:\n{transcript}\nYour supervising doctor is now discussing the case with you to assess your clinical reasoning. Answer any questions in a clear and succinct way"
        # full_prompt = f"{system_prompt}\n\n**Consultation History:**\n{prompt_history}\n\n**Supervisor's Question:**\n{user_message}"

        # Format for autogen's generate_reply
        messages_for_llm = [
            # Add original history first, mapping speakers to roles
            # Assuming 'Doctor' maps to 'assistant' and 'Patient' maps to 'user' for the purpose of the LLM's context
            # This might need adjustment based on how the original simulation was run
            *[{'role': 'assistant' if turn['speaker'] == 'Doctor' else 'user', 'content': turn['text']} for turn in history],
            # Add the system prompt as a system message if supported, or prepend to user query
            # For simplicity here, we include it implicitly via the agent's system_message
            # Add the supervisor's new question as the last user message
            {'role': 'user', 'content': user_message}
        ]

        # 3. Call the LLM using autogen
        # Create a temporary agent instance to use its generate_reply method
        temp_assistant = autogen.AssistantAgent(
            name="ChatAssistant",
            system_message=system_prompt, # Set the system prompt for the agent
            llm_config=doctor_config,
        )

        # Use generate_reply to get a direct response
        # Note: generate_reply might implicitly use the agent's system_message.
        # We pass the conversation history + new user message.
        llm_response = temp_assistant.generate_reply(messages=messages_for_llm)

        # Handle potential dict response from autogen
        if isinstance(llm_response, dict):
            llm_response_content = llm_response.get('content', 'Error: Could not extract content from LLM response.')
        elif isinstance(llm_response, str):
            llm_response_content = llm_response
        else:
            llm_response_content = "Error: Unexpected response type from LLM."
            print(f"Warning: Unexpected LLM response type: {type(llm_response)}")

        # Example: llm_response = call_llm_directly(doctor_config, full_prompt)
        # Using a placeholder response for now:
        # time.sleep(1) # Simulate network delay
        # llm_response = f"Placeholder response from {model_name} regarding: '{user_message[:50]}...'"

        # Return the content part of the response
        return jsonify({"response": llm_response_content})

    except ValueError as e:
        return jsonify({"error": f"Invalid model name: {str(e)}"}), 400
    except Exception as e:
        # Log the detailed error server-side for debugging
        print(f"Error during /chat handling: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

@app.route('/run')
def run_simulation():
    doctor_model_name = request.args.get('doctor_model', 'gemini-2.0-flash')
    case_file_name = request.args.get('case_file')

    if not case_file_name:
        # Use yield for errors within the stream for consistency
        def error_stream(): yield "data: ERROR:Case file not specified.\n\n" 
        return Response(stream_with_context(error_stream()), mimetype='text/event-stream')

    case_file_path = os.path.join(CASES_DIR, case_file_name)
    if not os.path.exists(case_file_path):
         def error_stream(): yield f"data: ERROR:Case file '{case_file_name}' not found.\n\n"
         return Response(stream_with_context(error_stream()), mimetype='text/event-stream')

    try:
        doctor_config = get_model_config(doctor_model_name)
        # Use a default for other models for now, or allow selection later
        other_config = get_model_config("gemini-2.0-flash")
    except ValueError as e:
        def error_stream(): yield f"data: ERROR:{str(e)}\n\n"
        return Response(stream_with_context(error_stream()), mimetype='text/event-stream')

    def generate_stream():
        # Include model name in the start message
        yield f"data: SIMULATION_START:{doctor_model_name}:Starting simulation with Doctor: {doctor_model_name}, Case File: {case_file_name}\n\n"
        case_number = 0
        print(f"--- [Stream] Attempting to open case file: {case_file_path}") # DEBUG
        try:
            with open(case_file_path, 'r') as f:
                print("--- [Stream] Successfully opened case file.") # DEBUG
                print("--- [Stream] Starting to read lines...") # DEBUG
                for line in f:
                    print(f"--- [Stream] Read line {case_number + 1}: {line[:100]}...") # DEBUG: Print start of line
                    if not line.strip():
                        print("--- [Stream] Skipping empty line.") # DEBUG
                        continue # Skip empty lines

                    case_number += 1
                    yield f"data: CASE_START:{case_number}\n\n"
                    print(f"--- [Stream] Yielded CASE_START for case {case_number}.") # DEBUG

                    try:
                        test_case = json.loads(line)
                        print(f"--- [Stream] Successfully parsed JSON for case {case_number}.") # DEBUG
                    except json.JSONDecodeError as json_err:
                        print(f"--- [Stream] ERROR parsing JSON in line {case_number}: {json_err}") # DEBUG
                        yield f"data: ERROR:Invalid JSON in line {case_number}: {json_err}\n\n"
                        continue # Skip to next line

                    # Store final results for this case
                    case_results = {
                        "case_number": case_number,
                        "correct_diagnosis": "N/A",
                        "doctor_diagnosis": "N/A",
                        "is_correct": False
                    }

                    try:
                        # Call the streaming function and iterate through yielded messages
                        print(f"--- [Stream] Calling process_single_case_streaming for case {case_number}...") # DEBUG
                        for message in process_single_case_streaming(test_case, doctor_config, other_config):
                            print(f"--- [Stream] Received message of type {type(message)}: {str(message)[:150]}...") # DEBUG: See what generate_stream receives

                            # Check if it's a structured conversation message (yielded as dict)
                            if isinstance(message, dict) and message.get("type") == "conversation":
                                time.sleep(0.5) # Add 0.5 second delay
                                yield f"data: CONVERSATION:{json.dumps(message)}\n\n"
                            # Check for string markers for final results or filtered INFO
                            elif isinstance(message, str):
                                if message.startswith("FINAL_CORRECT_DIAGNOSIS:"):
                                    case_results["correct_diagnosis"] = message.split(":", 1)[1]
                                elif message.startswith("FINAL_DOCTOR_DIAGNOSIS:"):
                                    case_results["doctor_diagnosis"] = message.split(":", 1)[1]
                                elif message.startswith("FINAL_IS_CORRECT:"):
                                    is_correct_str = message.split(":", 1)[1]
                                    case_results["is_correct"] = is_correct_str.lower() == 'true'
                                elif message == "CASE_PROCESSING_COMPLETE":
                                    # Yield the final structured result for this case
                                    yield f"data: CASE_RESULT:{json.dumps(case_results)}\n\n"
                                    break # End processing for this case
                                elif message.startswith("INFO:"):
                                    # Filter out specific INFO messages we don't want to show
                                    info_content = message.split(":", 1)[1]
                                    if info_content not in ["Grader signaled termination.", "Simulation ended by speaker selection.", "Simulation reached maximum turns."]:
                                         # Keep other potentially useful INFO like warnings
                                         yield f"data: INFO:{info_content}\n\n"
                                elif message.startswith("ERROR:"): # Pass through ERROR messages
                                     yield f"data: {message}\n\n"
                                # Ignore other uncategorized string messages from the stream
                            else:
                                # Log unexpected message types server-side
                                print(f"Warning: Unhandled message type from stream: {type(message)} - {message}")

                    except Exception as case_exc:
                        print(f"--- [Stream] ERROR processing case {case_number}: {str(case_exc)}") # DEBUG
                        import traceback
                        traceback.print_exc() # Print full traceback
                        # Yield error specific to this case
                        yield f"data: ERROR:Error processing case {case_number}: {str(case_exc)}\n\n"
                        # Yield a partial/error result for this case to keep UI consistent
                        yield f"data: CASE_RESULT:{json.dumps(case_results)}\n\n"
                        # Continue to the next case

        except FileNotFoundError:
            print(f"--- [Stream] ERROR: Case file not found: {case_file_name}") # DEBUG
            yield f"data: ERROR:Case file not found: {case_file_name}\n\n"
        except Exception as e:
            print(f"--- [Stream] ERROR: An unexpected error occurred in generate_stream: {str(e)}") # DEBUG
            import traceback
            traceback.print_exc() # Print full traceback
            # General error outside the case loop
            yield f"data: ERROR:An unexpected error occurred: {str(e)}\n\n"
        finally:
            print("--- [Stream] Reached finally block. Yielding SIMULATION_COMPLETE.") # DEBUG
            # Send a completion signal *before* the stream implicitly ends
            yield "data: SIMULATION_COMPLETE\n\n"

    # Set headers to prevent caching for SSE
    response = Response(stream_with_context(generate_stream()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    # Note: debug=True is convenient for development but should be False in production.
    # Ensure API keys are set via environment variables or .env file as needed by get_model_config
    app.run(host='0.0.0.0', debug=True, threaded=True) # Bind to 0.0.0.0
