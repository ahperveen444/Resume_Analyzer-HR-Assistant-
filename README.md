# Resume_Analyzer-HR-Assistant-
Resume Analyzer that evaluates candidates using LLMs, first extracting data like skills, experience, projects,etc and then scoring them based on job requirements, skills match, experience relevance, then auto send emails of interview to candidates who have high score based on skills match, skills relevance.




📄 Resume Analyzer — AI + LangChain Project

An AI-powered Resume Analyzer built using LangChain, OpenAI, and Supabase.
This project evaluates resumes against job requirements and produces:

✔ Candidate overall score
✔ Skill match analysis
✔ Experience relevance score
✔ ATS compatibility score
✔ Improvement suggestions
✔ Structured output for further automation

🚀 Features
LLM-Powered Evaluation using OpenAI GPT models
LangChain Prompt Templates + Chains
Structured JSON Output Parsing
Multi-metric Scoring System
Job Requirements Matching
Easy-to-extend pipeline architecture
Supabase Database Integration

🧱 Project Structure
Resume_Analyzer/
│── main.py                  # Main entry point
│── config.py                # Loads environment variables
│── requirements.txt
│── README.md
│── .gitignore
│── src/
│   ├── llm/
│   │   └── model.py         # LLM setup
│   ├── pipeline/
│   │   ├── prompt.py        # Prompt templates
│   │   ├── analyzer.py      # Main scoring pipeline
│   │   └── parser.py        # Output parser
│   ├── utils/
│   │   └── helpers.py       # Reusable functions
│── data/
│   ├── Resumes
│   └── job_description.txt

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/your-username/resume_analyzer.git
cd resume_analyzer

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows


3️⃣ Install dependencies
pip install -r requirements.txt


4️⃣ Add .env file
Create a .env file in the project root:
OPENAI_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_API_KEY=your_key

▶️ How to Run
python main.py


The analyzer will load:
Candidate resume
Job requirements
Run multiple LLM scoring prompts
Return structured JSON output

🧠 Technologies Used
Python 3.10+
LangChain
OpenAI
Supabase
Gmail

📌 Future Improvements
Dashboard UI (Next.js)
Semantic Search (RAG)
Auto Scheduling Interviews using Google Calendar

🤝 Contributing
Pull requests are welcome.
For major changes, open an issue first to discuss what you'd like to modify.
