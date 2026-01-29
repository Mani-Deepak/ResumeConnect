import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import core_logic
import resume_parser  # Import the resume parser

# --- Core Application Setup ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# --- File Upload Configuration ---
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Pre-load the ML Model on Startup ---
print("INFO: Initializing core logic and loading ML model. This may take a moment...")
try:
    core_logic.get_vectorstore()
    print("✅ ML Model and vector store initialized successfully.")
except Exception as e:
    print(f"❌ CRITICAL: Failed to initialize ML model on startup: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/recommendations', methods=['POST'])
def handle_recommendation_request():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part"}), 400
    file = request.files['resume']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid or no file selected"}), 400

    filename = secure_filename(file.filename)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(resume_path)

    parser_output_path = resume_path.replace(os.path.splitext(resume_path)[1], '.json')
    
    try:
        # --- Step 1: Parse resume directly ---
        print(f"INFO: Parsing resume: {filename}...")
        resume_data = resume_parser.parse_resume(resume_path)
        
        if "error" in resume_data:
            raise Exception(f"Parser error: {resume_data['error']}")
        
        print("INFO: Resume parsed successfully.")

        # --- Step 2: Generate recommendations ---
        print("INFO: Generating recommendations...")
        recommendations = core_logic.get_job_recommendations(resume_data, top_n=5)
        
        if "error" in recommendations:
             raise Exception(recommendations["error"])

        print("INFO: Recommendations generated successfully.")
        return jsonify(recommendations)

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": "An error occurred on the server.", "details": str(e)}), 500
    finally:
        # --- Step 3: Clean up temporary files ---
        if os.path.exists(resume_path): 
            os.remove(resume_path)
        if os.path.exists(parser_output_path): 
            os.remove(parser_output_path)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)