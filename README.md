# CareerMatch — AI-Powered Internship Recommendation System

> An intelligent full-stack web application that automatically matches students to the most relevant internships by semantically analyzing their resume using Generative AI, NLP, and Vector Search.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Proposed Solution](#3-proposed-solution)
4. [System Architecture](#4-system-architecture)
5. [Technology Stack](#5-technology-stack)
6. [Module-wise Description](#6-module-wise-description)
7. [How to Run the Project](#7-how-to-run-the-project)
8. [Project Structure](#8-project-structure)
9. [Key Features](#9-key-features)
10. [Research Significance](#10-research-significance)

---

## 1. Project Overview

**CareerMatch** is a full-stack AI-powered web application that helps students and early-career professionals discover internship opportunities that closely match their profile. Instead of manually browsing job portals, a user simply uploads their resume — and the system intelligently recommends the top 5 most relevant internships using semantic understanding.

The application combines multiple modern AI technologies:
- **Large Language Models (LLM)** via Google Gemini for contextual resume understanding
- **Sentence Transformer Embeddings** for converting resumes and job descriptions into semantic vectors
- **Vector Database (ChromaDB)** for fast similarity-based retrieval
- **Hybrid NLP Pipeline** for structured information extraction from unstructured resume documents

---

## 2. Problem Statement

Traditional job portals and recommendation systems rely on **keyword matching** — a job is recommended only if the words in the resume exactly match the words in the job description. This approach has critical limitations:

- A student who knows "PyTorch" may miss a job listing that says "Deep Learning framework"
- Candidates with strong potential but non-standard resume formats are overlooked
- Manual job searching is time-consuming and inefficient
- Keyword systems do not understand context, relevance, or transferable skills

There is a clear need for a **semantically intelligent system** that understands the meaning behind a resume, not just the words.

---

## 3. Proposed Solution

CareerMatch solves this by implementing an **end-to-end AI pipeline**:

```
User uploads Resume
        ↓
Resume Text Extraction (PDF / DOCX / TXT)
        ↓
Structured Information Extraction (NLP parsing)
        ↓
AI Summary Generation (Google Gemini LLM)
        ↓
Dense Vector Embedding (HuggingFace Sentence Transformer)
        ↓
Semantic Similarity Search (ChromaDB Vector Database)
        ↓
Top 5 Internship Recommendations Returned
```

The system understands that "Python developer with data analysis experience" semantically matches a "Data Science Intern" role — even without exact keyword overlap.

---

## 4. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND (React.js)                   │
│   Home Page  |  Upload Resume  |  View Recommendations       │
└────────────────────────────┬─────────────────────────────────┘
                             │  HTTP REST API (JSON)
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                     BACKEND (Python / Flask)                  │
│                                                              │
│  ┌─────────────────┐   ┌──────────────────────────────────┐  │
│  │  resume_parser  │   │         core_logic               │  │
│  │                 │   │                                  │  │
│  │ • Text extract  │   │ • HuggingFace Embeddings         │  │
│  │ • Section split │   │ • ChromaDB Vector Store          │  │
│  │ • Skills detect │   │ • Semantic Similarity Search     │  │
│  │ • Gemini AI     │   │ • Top-N Recommendations          │  │
│  └────────┬────────┘   └──────────────┬───────────────────┘  │
└───────────┼──────────────────────────┼──────────────────────┘
            │                          │
            ▼                          ▼
   Google Gemini API            ChromaDB + jobs.csv
   (Resume Summarization)       (Vector Database)
```

---

## 5. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React.js 18 | User interface — upload, browse, view recommendations |
| **Styling** | Tailwind CSS | Responsive, modern UI design |
| **Backend API** | Python 3, Flask | REST API server, request handling |
| **CORS** | Flask-CORS | Cross-origin communication between frontend and backend |
| **Resume Parsing (PDF)** | pdfplumber | Extract raw text from PDF resumes |
| **Resume Parsing (DOCX)** | python-docx | Extract text from Word document resumes |
| **NLP Extraction** | Regex, custom rules | Parse skills, education, experience from text |
| **AI Summarization** | Google Gemini API | Generate natural language profile summary |
| **Embeddings Model** | HuggingFace `all-MiniLM-L6-v2` | Convert text to 384-dimensional semantic vectors |
| **Vector Database** | ChromaDB | Store and query job embeddings by cosine similarity |
| **ML Orchestration** | LangChain | Pipeline for embedding creation and vector retrieval |
| **Data Layer** | Pandas, CSV | Job dataset storage and loading |

---

## 6. Module-wise Description

### 6.1 Frontend (`frontend/src/App.jsx`)

A single-page React application with three views:

- **Home Page** — Displays all available internships fetched from the backend, showing company, title, location, stipend, duration, and required skills.
- **Recommendations Page** — Allows the user to upload their resume and view AI-matched internship recommendations with a match score.
- **Profile Page** — Displays the parsed resume data (name, contact, skills, education, experience) extracted by the AI.

### 6.2 Backend API (`backend/app.py`)

A Flask REST API server exposing two endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/api/internships` | GET | Returns all internships from the CSV dataset |
| `/api/recommendations` | POST | Accepts a resume file, returns top 5 matched internships |

### 6.3 Resume Parser (`backend/resume_parser.py`)

A multi-stage document processing module:

1. **Text Extraction** — Supports PDF (via pdfplumber), DOCX (via python-docx), and plain TXT files.
2. **Section Detection** — Identifies resume sections (Education, Skills, Experience, Projects, etc.) using heading pattern matching.
3. **Entity Extraction** — Extracts:
   - Candidate name (from top lines or email heuristic)
   - Email address (regex)
   - Phone number (phonenumbers library, India-aware)
   - Skills (matched against a master skills vocabulary)
   - Education (degree, institution, CGPA, year)
   - Work experience (role, company, duration, bullet points)
   - Projects
4. **AI Summary** — Sends the structured data to Google Gemini API to produce a coherent natural language summary of the candidate.

### 6.4 Core Logic / Recommendation Engine (`backend/core_logic.py`)

The heart of the recommendation system:

1. **Embeddings Model** — Loads `sentence-transformers/all-MiniLM-L6-v2` from HuggingFace. This model maps any text to a 384-dimensional vector capturing its semantic meaning.
2. **Vector Store Initialization** — Reads all internship records from `jobs.csv`, converts each job description into a vector, and stores them in ChromaDB (persisted to disk at `chroma_db/`).
3. **Recommendation Query** — Converts the uploaded resume's structured profile into a combined text query, embeds it, and performs a **cosine similarity search** against the job vectors.
4. **Result Ranking** — Returns the top 5 internships ranked by semantic relevance score.

### 6.5 Dataset (`backend/jobs.csv`)

A CSV dataset of internship listings with columns:
- `internship_title` — Job role name
- `company_name` — Hiring company
- `location` — City/Remote
- `full_description` — Detailed job description
- `required_skills` — Pipe-separated skill list
- `stipend_inr` — Monthly stipend in INR
- `duration_months` — Internship duration

---

## 7. How to Run the Project

### Prerequisites

- Python 3.9 or above
- Node.js 16 or above
- A free Google Gemini API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

### Step 1 — Run the Backend

Open a terminal and run:

```bash
cd backend

# Install Python dependencies (first time only)
pip install -r requirements.txt

# Set your Gemini API key
# On Windows PowerShell:
$env:GEMINI_API_KEY = "your_gemini_api_key_here"

# Start the Flask server
python app.py
```

The backend starts at: **http://localhost:5000**

> On first run, the HuggingFace model (~90MB) will be downloaded automatically. The vector store is built from jobs.csv and saved to `chroma_db/` for faster subsequent startups.

---

### Step 2 — Run the Frontend

Open a **second terminal** and run:

```bash
cd frontend

# Install Node dependencies (first time only)
npm install

# Start the React development server
npm start
```

The frontend opens automatically at: **http://localhost:3000**

---

### Step 3 — Use the Application

1. Open **http://localhost:3000** in your browser.
2. Browse available internships on the **Home Page**.
3. Click **"Get Recommendations"** in the navigation bar.
4. Upload your resume (PDF, DOCX, or TXT format).
5. Wait ~10–15 seconds for AI parsing and matching.
6. View your **Top 5 personalized internship recommendations**.
7. Click **"Profile"** to see the structured data extracted from your resume.

---

## 8. Project Structure

```
jst/
├── backend/
│   ├── app.py              # Flask API server — main entry point
│   ├── core_logic.py       # Embedding model + ChromaDB + recommendation engine
│   ├── resume_parser.py    # Resume text extraction + NLP + Gemini AI
│   ├── config.py           # API key and app configuration
│   ├── jobs.csv            # Internship dataset
│   ├── requirements.txt    # Python dependencies
│   ├── chroma_db/          # Persisted vector database (auto-generated)
│   └── uploads/            # Temporarily stores uploaded resumes
│
├── frontend/
│   ├── package.json        # Node.js dependencies
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   └── src/
│       ├── App.jsx         # Main React application (all pages)
│       ├── App.css         # Global styles
│       └── index.js        # React entry point
│
└── README.md               # This file
```

---

## 9. Key Features

- **Multi-format Resume Support** — Accepts PDF, DOCX, DOC, and TXT files
- **AI-Powered Understanding** — Google Gemini generates a contextual candidate profile beyond keyword extraction
- **True Semantic Matching** — Vector embeddings capture meaning, not just words — "Machine Learning" matches "AI/ML Engineer" correctly
- **Offline Vector Store** — ChromaDB persists vectors to disk; no repeated embedding on restarts
- **Clean Modern UI** — Fully responsive React interface with Tailwind CSS
- **Real-time Profile View** — Users can see exactly what information was extracted from their resume
- **Scalable Architecture** — The CSV dataset can be replaced with a live database with minimal changes

---

## 10. Research Significance

This project demonstrates the practical application of several cutting-edge AI research areas:

| Research Area | How it is Applied |
|---|---|
| **Retrieval-Augmented Generation (RAG)** | Resume profile retrieves relevant job documents from a vector store |
| **Dense Passage Retrieval** | Sentence Transformer embeddings instead of sparse BM25/TF-IDF |
| **LLM-based Information Extraction** | Gemini API extracts structured data from unstructured resume text |
| **Semantic Textual Similarity** | Cosine similarity in embedding space for job-candidate matching |
| **Hybrid NLP Pipeline** | Rule-based parsing combined with deep learning for robustness |

This system can serve as a foundation for research in:
- Automated recruitment and talent acquisition
- Fairness and bias in AI-based hiring systems
- Evaluation metrics for semantic job matching
- Privacy-preserving resume analysis

---

*Developed as part of an academic project exploring the intersection of Generative AI, NLP, and career technology.*
