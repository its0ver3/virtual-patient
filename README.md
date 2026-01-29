# Virtual Patient Interview

Streamlit app for physiotherapy students to practice patient interviews with an AI-simulated patient.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.streamlit/secrets.toml`:
```bash
mkdir .streamlit
```

Add your API key to `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Read the instructions on the welcome screen
2. Click "Begin Interview" to start
3. Ask the patient questions about their condition
4. Click "End Session & Get Feedback" when done
5. Review your feedback and start a new session if desired
