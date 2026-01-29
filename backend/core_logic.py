import os
import sys
import json
import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# --- ROBUST PATH ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV_PATH = os.path.join(SCRIPT_DIR, "jobs.csv")

# Initialize embeddings model (singleton pattern)
_embeddings = None
_vectorstore = None

def get_embeddings():
    """Get or initialize embeddings model"""
    global _embeddings
    if _embeddings is None:
        try:
            print("[INFO] Loading HuggingFace embeddings model...")
            _embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}  # This is important!
            )
            print("[SUCCESS] Hugging Face Embeddings Model loaded.")
        except Exception as e:
            print(f"[ERROR] Error loading embeddings: {e}")
            raise
    return _embeddings

def initialize_vectorstore_from_csv(csv_path):
    """Initialize vector store from a CSV file"""
    global _vectorstore

    try:
        embeddings = get_embeddings()

        try:
            df = pd.read_csv(csv_path)
            print(f"[INFO] CSV loaded with {len(df)} rows")
        except FileNotFoundError:
            print(f"[ERROR] CSV file not found at {csv_path}")
            return None

        df = df.fillna('')

        if df.empty:
            print(f"[WARNING] No jobs found in {csv_path}")
            return None
        
        print(f"[INFO] Loading {len(df)} jobs from {csv_path} into vector store...")

        docs = []
        for i, job in df.iterrows():
            # Create rich content for better matching
            content = (
                f"Job Title: {job['internship_title']}\n"
                f"Company: {job['company_name']}\n"
                f"Location: {job['location']}\n"
                f"Job Description: {job['full_description']}\n"
                f"Required Skills: {job['required_skills']}\n"
                f"Duration: {job['duration_months']} months\n"
                f"Stipend: {job['stipend_inr']} INR"
            )

            job_id = job.get('id', f"csv_{i}")

            doc = Document(
                page_content=content,
                metadata={
                    "id": str(job_id),
                    "internship_title": str(job['internship_title']),
                    "company_name": str(job['company_name']),
                    "location": str(job['location']),
                    "full_description": str(job['full_description']),
                    "required_skills": str(job['required_skills']),
                    "stipend_inr": str(job['stipend_inr']),
                    "duration_months": str(job['duration_months']),
                }
            )
            docs.append(doc)

        print("[INFO] Creating Chroma vector store...")
        _vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=None
        )
        print("[SUCCESS] Vector store created successfully.")
        return _vectorstore

    except KeyError as e:
        print(f"[ERROR] Missing column in CSV file: {e}")
        print("Ensure your CSV has columns: id, internship_title, company_name, location, full_description, required_skills, stipend_inr, duration_months")
        return None
    except Exception as e:
        print(f"[ERROR] Error creating vector store: {e}")
        import traceback
        traceback.print_exc()
        raise

def get_vectorstore():
    """Get or initialize vector store"""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = initialize_vectorstore_from_csv(DEFAULT_CSV_PATH)
    return _vectorstore

def get_job_recommendations(resume_summary_data, top_n=10):
    """
    Get job recommendations based on resume summary using semantic search
    """
    try:
        vectorstore = get_vectorstore()

        if vectorstore is None:
            return {"error": "Vector store not initialized or CSV file not found/empty"}

        # Build resume text with better structure
        resume_text_parts = []

        # Add name and objective
        if resume_summary_data.get('name'):
            resume_text_parts.append(f"Candidate: {resume_summary_data['name']}")

        # Add AI summary (most important)
        if resume_summary_data.get('ai_summary'):
            ai_summary = resume_summary_data['ai_summary']
            # Remove error messages from AI summary
            if not ai_summary.startswith('['):
                resume_text_parts.append(f"Profile: {ai_summary}")

        # Add skills (very important for matching)
        if resume_summary_data.get('skills'):
            skills_text = "Technical Skills: " + ", ".join(resume_summary_data['skills'][:15])
            resume_text_parts.append(skills_text)

        # Add education
        if resume_summary_data.get('education'):
            for edu in resume_summary_data.get('education', [])[:2]:
                edu_text = f"Education: {edu.get('degree', '')} from {edu.get('institution', '')}"
                resume_text_parts.append(edu_text)

        # Add experience
        if resume_summary_data.get('experience'):
            for exp in resume_summary_data.get('experience', [])[:3]:
                exp_text = f"Experience: {exp.get('title', '')} at {exp.get('company', '')}"
                if exp.get('duration'):
                    exp_text += f" ({exp.get('duration')})"
                if exp.get('bullets'):
                    exp_text += " - " + " ".join(exp['bullets'][:2])
                resume_text_parts.append(exp_text)

        # Add projects
        if resume_summary_data.get('projects'):
            for proj in resume_summary_data.get('projects', [])[:3]:
                proj_title = proj.get('title', '').split('.')[0].strip()
                proj_text = f"Project: {proj_title}"
                if proj.get('bullets'):
                    proj_text += " - " + " ".join(proj['bullets'][:1])
                resume_text_parts.append(proj_text)

        resume_text = "\n".join(resume_text_parts)

        if not resume_text.strip():
            resume_text = "Looking for internship opportunities in technology"
        
        print(f"\n{'='*60}")
        print(f"[DEBUG] Resume Search Query:")
        print(f"{'='*60}")
        print(resume_text[:500])  # Print first 500 chars
        print(f"{'='*60}\n")
        print(f"[INFO] Total resume text length: {len(resume_text)} characters")

        # Perform similarity search
        print(f"[INFO] Searching for top {top_n} matches...")
        matched_docs_and_scores = vectorstore.similarity_search_with_score(resume_text, k=top_n)
        
        print(f"[SUCCESS] Found {len(matched_docs_and_scores)} matches")
        
        # Debug: Print raw scores
        print(f"\n[DEBUG] Raw similarity scores:")
        for idx, (doc, score) in enumerate(matched_docs_and_scores[:3]):
            print(f"  Match {idx+1}: {doc.metadata.get('internship_title', 'Unknown')} - Score: {score:.4f}")

        recommendations = []
        for doc, score in matched_docs_and_scores:
            job_dict = doc.metadata.copy()

            # Fix the similarity calculation
            # Chroma uses L2 distance by default, where smaller = more similar
            # Convert distance to similarity percentage (0 = 100%, higher distance = lower %)
            # Typical L2 distances range from 0 to 2 for normalized vectors
            
            if score < 0.5:
                similarity_percentage = 100
            elif score < 1.0:
                similarity_percentage = 100 - (score * 50)  # 0.5 -> 75%, 1.0 -> 50%
            else:
                similarity_percentage = max(0, 50 - ((score - 1.0) * 25))  # 1.5 -> 37.5%, 2.0 -> 25%

            job_dict['matching_percentage'] = round(similarity_percentage, 2)
            job_dict['raw_distance'] = round(float(score), 4)

            recommendations.append(job_dict)

        # Sort by matching percentage (highest first)
        recommendations.sort(key=lambda x: x['matching_percentage'], reverse=True)

        print(f"\n[DEBUG] Top 3 recommendations:")
        for idx, rec in enumerate(recommendations[:3]):
            print(f"  {idx+1}. {rec.get('internship_title')} - {rec['matching_percentage']}%")

        return recommendations

    except Exception as e:
        print(f"[ERROR] Error in recommendation logic: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python core_logic.py <path_to_parsed_resume.json> <output_path_for_recommendations.json>")
        sys.exit(1)

    parsed_resume_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"CORE_LOGIC: Loading parsed resume from {parsed_resume_path}")
    try:
        with open(parsed_resume_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
    except Exception as e:
        print(f"CORE_LOGIC: Error reading resume JSON file: {e}")
        sys.exit(1)

    print("CORE_LOGIC: Generating recommendations...")
    recommendations = get_job_recommendations(resume_data, top_n=5)

    print(f"CORE_LOGIC: Writing recommendations to {output_path}")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, indent=2)
    except Exception as e:
        print(f"CORE_LOGIC: Error writing recommendations JSON file: {e}")
        sys.exit(1)

    print("CORE_LOGIC: Script finished successfully.")