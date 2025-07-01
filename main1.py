import json
import sqlite3
import argparse
from multi_med import get_model_config, process_single_case

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
    parser = argparse.ArgumentParser(description='Run a range of medical cases')
    parser.add_argument('--start', type=int, default=0, help='Start case number (0-based index, inclusive)')
    parser.add_argument('--end', type=int, default=1, help='End case number (0-based index, exclusive)')
    parser.add_argument('--notes', type=str, default='', help='Notes about this run (e.g., experimental conditions, changes made)')
    args = parser.parse_args()

    doctor_model = "gpt-4o-mini"
    doctor_config = get_model_config(doctor_model)
    other_config = get_model_config("gpt-4o-mini")
    
    # Initialize database
    conn = init_db()
    c = conn.cursor()
    
    # Read and process cases from JSONL file
    cases_file = 'cases/Headache_all_cases.jsonl'
    with open(cases_file, 'r') as f:
        lines = f.readlines()
        start = max(0, args.start)
        end = min(len(lines), args.end)
        if start >= end or start >= len(lines):
            print(f"Error: Invalid range. There are {len(lines)} cases available.")
        else:
            for i in range(start, end):
                test_case = json.loads(lines[i])
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
                          args.notes,
                          ','.join(result['unknown_investigations']) if result.get('unknown_investigations') else ''))
                conn.commit()
                # Print progress
                print(f"Processing case {i + 1} of {len(lines)}")
                print(f"Correct diagnosis: {result['correct_diagnosis']}")
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
