# 🤖 JobAlign AI (Job AI Agent)

[![Medium Blog](https://img.shields.io/badge/Medium-Read_the_Blog-black?logo=medium)](https://medium.com/p/6980a7c5fcf4)

An **Agentic AI career assistant** that automates the exhausting job search process. JobAlign AI takes a natural language query, fetches live job postings, parses your resume, and provides a definitive similarity score with actionable feedback to help you land the role.

---

## 🚀 Overview

Instead of manually navigating job boards and guessing if your resume passes an ATS (Applicant Tracking System), JobAlign AI acts as your automated career advocate. 

Powered by **LangGraph**, it utilizes a multi-agent workflow to process tasks in parallel:
1.  **Intent Understanding:** Translates your natural language query into structured API parameters.
2.  **Live Market Scraping:** Scrapes real-time, relevant jobs from platforms like LinkedIn via Apify.
3.  **Resume Parsing:** Extracts structured data (skills, projects, experience) from your uploaded PDF resume.
4.  **Intelligent Evaluation:** An evaluator agent cross-references your profile against job requirements to generate a 0-100 similarity score and tailored feedback.

---

## 🏗️ Workflow

The system uses **LangGraph** to manage a multi-agent state machine, executing tasks in parallel for maximum efficiency:



1.  **Input Trigger:** The user enters a job query and uploads a PDF resume.
2.  **Parallel Track A (The Scout):**
    * An agent interprets user intent and structures search parameters.
    * The system scrapes live jobs from LinkedIn via **Apify**.
    * A "Jobs Analyzer" agent distills messy descriptions into core requirements.
3.  **Parallel Track B (The Parser):**
    * The system extracts raw text from the PDF.
    * A "Resume Fields Extractor" agent structures skills, experience, and projects into a clean schema.
4.  **Convergence:** Both tracks meet at the **Feedback & Similarity** node.
5.  **Output:** The system calculates a match score, generates feedback, and logs results to a local **SQLite** database and **Google Sheets**.

---

## 🧠 Key Features

* **Natural Language Search:** Simply type *"Looking for a data science internship in Germany"*.
* **Zero-Cost Local Inference:** Fully compatible with **Ollama** (e.g., Llama 3.1 7B). Optimized prompt engineering allows the workflow to run locally with zero API costs and total privacy.
* **Strict Structured Data:** Uses **Pydantic** to force LLMs to return reliable JSON, ensuring the matching engine never fails due to formatting issues.
* **Automated Job CRM:** Automatically pushes matched jobs, scores, and feedback into a **Google Spreadsheet** for easy tracking.
* **Sleek Frontend:** A responsive web interface built with HTML/CSS/JS for a seamless user experience.

---

## ⚙️ Tech Stack

| Category | Tools Used |
| :--- | :--- |
| **Language** | Python |
| **AI Orchestration** | LangGraph / LangChain |
| **LLMs** | Gemini 2.5 Flash Lite (Cloud) / Llama 3.1 7B (Local via Ollama) |
| **Scraping** | Apify (LinkedIn Actor) |
| **Backend & DB** | FastAPI / SQLModel / SQLite |
| **Frontend** | Vanilla HTML, CSS, & JavaScript |

---

## 🧪 Example Use Case

**Input:**
* **Query:** *"Looking for a data science internship in Germany"*
* **Resume:** Uploaded `my_resume.pdf`

**Output:**
* List of matching live internships in Germany.
* Match score for each (e.g., 78%).
* **AI Feedback:** *"Your resume matches the Python requirements but lacks 'Probability and Statistics'. Consider adding your university research project to highlight this."*

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/jugal-lachhwani/job-ai-agent.git](https://github.com/jugal-lachhwani/job-ai-agent.git)
cd job-ai-agent
2️⃣ Create Virtual Environment
Bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
3️⃣ Install Dependencies
Bash
pip install -r requirements.txt
4️⃣ Setup Environment Variables
Create a .env file in the root directory:

Code snippet
APIFY_TOKEN=your_apify_token
APIFY_ACTOR_NAME=valig/linkedin-jobs-scraper
GEMINI_API_KEY=your_gemini_api_key
5️⃣ Run the Application
Start the FastAPI backend:

Bash
python src/api.py
Access the UI by opening frontend/index.html in your browser.

📌 Future Enhancements
AI Cover Letter Generator: Drafts personalized letters based on match feedback.

Skill Learning Roadmaps: Generates a custom path to bridge identified skill gaps.

Real-Time Analytics: Dashboards for job market demand vs. candidate supply.

📜 License
MIT License

👤 Author
Jugal Lachhwani AI / Backend / Data-Driven Developer

Focused on building impactful AI systems for career and education guidance.

⭐ If you found this project useful, don’t forget to star the repository!