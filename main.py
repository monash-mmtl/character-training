import json
import sqlite3
from multi_med import get_model_config, process_single_case

# Configuration - modify this to add notes about your run
RUN_NOTES = "Unlimited budget"

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
                  conversation_log TEXT,
                  total_investigation_cost REAL,
                  notes TEXT,
                  unknown_investigations TEXT)''')
    conn.commit()
    return conn

def main():
    # Initialize configurations'
    doctor_model = "gemini-2.5-flash"
    doctor_config = get_model_config(doctor_model)
    other_config = get_model_config("gemini-2.5-flash")
    
    # Initialize database
    conn = init_db()
    c = conn.cursor()
    
    # Read and process cases from JSONL file
    cases_file = 'cases/Headache_all_cases.jsonl'
    with open(cases_file, 'r') as f:
        for line in f:
            test_case = json.loads(line)
            
            # Process the case
            result = process_single_case(test_case, doctor_config, other_config)
            
            # Store results in database
            c.execute('''INSERT INTO case_results 
                        (llm, presentation, correct_diagnosis, doctor_diagnosis, is_correct, conversation_log, total_investigation_cost, notes, unknown_investigations)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (doctor_model,
                      cases_file[6:],
                      result['correct_diagnosis'],
                      result['doctor_diagnosis'],
                      1 if result['is_correct'] else 0,
                      result['conversation_log'],
                      result.get('total_investigation_cost', 0.0),
                      RUN_NOTES,
                      ','.join(result.get('unknown_investigations', []))))
            conn.commit()
            
            # Print progress
            print(f"Processed case with correct diagnosis: {result['correct_diagnosis']}")
            print(f"Doctor's diagnosis: {result['doctor_diagnosis']}")
            print(f"Correct: {'Yes' if result['is_correct'] else 'No'}")
            print(f"Total investigation cost: ${result.get('total_investigation_cost', 0.0):.2f}")
            if result.get('unknown_investigations'):
                print(f"Unknown investigations: {', '.join(result['unknown_investigations'])}")
            print("-" * 50)
    
    # Close database connection
    conn.close()

if __name__ == "__main__":
    main() 