# AI-Powered Job Recommender for the Indian Market

This project implements an AI-powered job recommendation system tailored for the Indian job market. It leverages the **Gemini API** to perform intelligent, semantic matching between user resumes and job descriptions. Job data is provided through **manually uploaded Excel sheets or database entries**, making the system simple, ethical, and easy to maintain.

---

## 📌 Features

- Resume parsing and structured data extraction  
- Job recommendation using AI-powered semantic matching  
- Support for Indian job locations  
- Explainable job recommendations  
- Excel-based job data ingestion  
- Clean and scalable architecture  

---

## 🧩 System Requirements

### 1. Resume Parsing
The system accepts resumes in PDF or text formats and extracts:

- Personal Information (name, contact details, location)
- Educational Background (degree, university, graduation year)
- Work Experience (job titles, companies, duration, responsibilities)
- Skills (technical and soft skills)
- Keywords representing candidate expertise

---

### 2. Job Data Input (Manual Upload)
Job listings are maintained manually and uploaded into the system.

**Supported sources:**
- Excel files uploaded by an admin
- Any database populated manually (MySQL, PostgreSQL, MongoDB)

**Stored job attributes:**
- Job Title
- Company Name
- Location (e.g., Bengaluru, Hyderabad, Mumbai, Delhi NCR)
- Job Description
- Required Skills and Qualifications
- Experience Level
- Salary Range (optional)

---

### 3. AI-Based Matching Engine (Hugging face)
The Hugging face embeddings model powers the core recommendation logic.

- **Semantic Matching:** Understands related skills beyond keywords  
- **Contextual Analysis:** Compares responsibilities and experience holistically  
- **Location Filtering:** Matches jobs based on user preferences  
- **Experience Matching:** Aligns candidate experience with job requirements  

---

### 4. Recommendation Generation
The system outputs ranked job recommendations.

- Jobs are ranked using a similarity score (0–100)
- Each recommendation includes a short explanation for transparency

**Example explanation:**
> "Recommended because your Python and Django experience closely matches the backend responsibilities of this role."

---

### 5. User Interface
- Resume upload (PDF / DOCX)
- Job recommendations display
- Admin interface for Excel job uploads

---

## 🏗 Architecture Overview

- **Frontend:** Web or mobile interface for users
- **Backend:** Handles resume parsing, job storage, and AI logic
- **Resume Processing Module:** Converts resumes into structured JSON
- **Job Database:** Stores job listings uploaded via Excel
- **Hugging face embedding model:** Core AI engine for semantic understanding

---

## 🔑 Gemini API Setup

1. Visit **Google AI Studio**
2. Sign in with your Google account
3. Click **"Get API key"**
4. Create a new project (if required)
5. Generate and securely store your API key

⚠️ Do not expose your API key publicly.

---