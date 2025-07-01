# Multi-Med: Medical AI Diagnostic Benchmark

A medical diagnostic system that simulates doctor-patient interactions using multiple AI agents. The system uses a combination of different language models to create a realistic medical consultation environment.

## Project Overview

This project implements an AI-powered medical diagnostic system that:
- Simulates doctor-patient interactions
- Processes medical cases from a structured dataset
- Uses multiple AI agents to represent different roles (doctor, patient, measurement assistant, and grader)
- Evaluates diagnostic accuracy
- Stores results in a SQLite database

## System Components

### AI Agents
1. **Doctor Agent**: Conducts the medical consultation, asks questions, requests examinations, and makes diagnoses
2. **Patient Agent**: Responds to doctor's questions based on case information
3. **Measurement Assistant**: Provides examination findings and test results
4. **Grader Agent**: Evaluates the doctor's diagnosis against the correct diagnosis

### Key Files
- `main.py`: Core application logic and agent orchestration
- `multi_med/llm_config.py`: Configuration for different language models
- `agentclinic_medqa.jsonl`: Dataset containing medical cases
- `medical_cases.db`: SQLite database storing case results

## Setup

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **API Keys**
   Create a `.env` file with the following API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   OPEN_ROUTER_KEY=your_openrouter_key
   DEEPSEEK_API_KEY=your_deepseek_key
   ```

3. **Database**
   The system automatically initializes a SQLite database (`medical_cases.db`) to store case results.

## Usage

Run the main application:
```bash
python main.py
```

The system will:
1. Process each case from the `agentclinic_medqa.jsonl` file
2. Simulate doctor-patient interactions
3. Store results in the database
4. Print progress and results to the console

## Running the Web Interface (Flask)

Alternatively, you can use the Flask web interface to run simulations:

1.  **Ensure Setup**: Make sure you've completed the Environment Setup and API Keys steps above.
2.  **Run Flask App**:
    ```bash
    python app.py
    ```
3.  **Access Interface**: Open your web browser and navigate to `http://127.0.0.1:5000` (or the address provided in the console).
4.  **Select Options**: Choose the desired Doctor LLM and the case file from the dropdowns.
5.  **Run Simulation**: Click "Run Simulation" to start the process and view the live conversation log.

## Supported Language Models

The system supports multiple language models:
- GPT4o
- GPT4o-mini
- Gemini 2.0 Flash
- Gemini 2.5 Pro
- DeepSeek V3
- DeepSeek R1

## Database Schema

The `medical_cases.db` contains a table `case_results` with the following columns:
- `case_id`: Unique identifier
- `correct_diagnosis`: The actual diagnosis
- `doctor_diagnosis`: The AI doctor's diagnosis
- `is_correct`: Boolean indicating if the diagnosis was correct
- `conversation_log`: Full text of the consultation

## Project Structure

```
.
├── main.py                  # Main application logic
├── multi_med/
│   └── llm_config.py       # Language model configurations
├── agentclinic_medqa.jsonl  # Medical case dataset
├── medical_cases.db        # Results database
├── requirements.txt        # Project dependencies
└── .env                    # API keys (not in repo)
```

