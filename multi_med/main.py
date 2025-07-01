import json
import sqlite3
import time
from multi_med import get_model_config, process_single_case
from google.api_core.exceptions import ServiceUnavailable

# Initialize database
def init_db():
    conn = sqlite3.connect('medical_cases.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS case_results
                 (llm TEXT,
                  presentation TEXT,
                  correct_diagnosis TEXT,
                  doctor_diagnosis TEXT,
                  is_correct INTEGER,
                  tag TEXT,
                  conversation_log TEXT,
                  total_investigation_cost REAL)''')
    conn.commit()
    return conn

def process_cases(doctor_model, cases_file, max_retries=3):
    # Initialize configurations
    doctor_config = get_model_config(doctor_model)
    other_config = get_model_config("gemini-2.0-flash")
    
    # Initialize database
    conn = init_db()
    c = conn.cursor()
    
    # Read and process cases from JSONL file
    with open(cases_file, 'r') as f:
        for line in f:
            test_case = json.loads(line)
            
            # Process the case with retry logic
            retry_count = 0
            while retry_count <= max_retries:
                try:
                    # Process the case
                    result = process_single_case(test_case, doctor_config, other_config)
                    
                    # Check if identical row already exists
                    c.execute('''SELECT COUNT(*) FROM case_results 
                                WHERE llm = ? AND presentation = ? AND correct_diagnosis = ? 
                                AND doctor_diagnosis = ? AND is_correct = ? AND tag = ?''',
                             (doctor_model,
                              cases_file[6:],
                              result['correct_diagnosis'],
                              result['doctor_diagnosis'],
                              1 if result['is_correct'] else 0,
                              test_case.get('tag', '')))
                    
                    row_exists = c.fetchone()[0] > 0
                    
                    # Store results in database only if not a duplicate
                    if not row_exists:
                        c.execute('''INSERT INTO case_results 
                                    (llm, presentation, correct_diagnosis, doctor_diagnosis, is_correct, tag, conversation_log)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                 (doctor_model,
                                  cases_file[6:],
                                  result['correct_diagnosis'],
                                  result['doctor_diagnosis'],
                                  1 if result['is_correct'] else 0,
                                  test_case.get('tag', ''),
                                  result['conversation_log']))
                        conn.commit()
                        print(f"Added new case with diagnosis: {result['correct_diagnosis']}")
                    else:
                        print(f"Skipped duplicate case with diagnosis: {result['correct_diagnosis']}")
                    
                    # Print progress
                    print(f"Doctor's diagnosis: {result['doctor_diagnosis']}")
                    print(f"Correct: {'Yes' if result['is_correct'] else 'No'}")
                    print("-" * 50)
                    
                    # Successfully processed this case, break the retry loop
                    break
                    
                except ServiceUnavailable as e:
                    retry_count += 1
                    if retry_count <= max_retries:
                        print(f"Google API service unavailable. Error: {e}")
                        print(f"Retrying case... Attempt {retry_count} of {max_retries}")
                        time.sleep(2)  # Add a small delay before retrying
                    else:
                        print(f"Maximum retry attempts reached for this case. Skipping.")
                        break
                except Exception as e:
                    print(f"An error occurred while processing the case: {e}")
                    break
    
    # Close database connection
    conn.close()

def main():
    # Default values
    doctor_model = "gpt-4.1-nano"
    cases_file = 'cases/Back pain, lower_all_cases.jsonl'
    
    # Process cases with built-in retry
    process_cases(doctor_model, cases_file)

if __name__ == "__main__":
    main()