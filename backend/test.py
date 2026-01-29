import os
import json
import subprocess
import sys
import shutil
import textwrap

def run_core_logic_test():
    """
    Creates a temporary environment with dummy files to test core_logic.py,
    runs the script, prints the output, and cleans up afterward.
    """
    # 1. SETUP: Create a temporary directory for our test files
    test_dir = "temp_test_dir"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    print(f"--- 📂 Created temporary directory: {test_dir} ---")

    try:
        # 2. CREATE DUMMY jobs.csv FILE
        jobs_csv_path = os.path.join(test_dir, "jobs.csv")
        jobs_data = textwrap.dedent("""\
            id,internship_title,company_name,location,full_description,required_skills,stipend_inr,duration_months
            1,Data Analyst Intern,DataCorp,New York,"Analyze large datasets, create data visualizations, and build reports. Work closely with the marketing team to identify trends.",Python;SQL;Pandas;Tableau,50000,3
            2,Frontend Developer Intern,WebWorld,San Francisco,"Build modern user interfaces using React. You will work with our design team to implement responsive web pages and new features.",JavaScript;React;HTML;CSS,60000,6
            3,Backend Engineer Intern,ServerSide Inc,Remote,"Develop scalable backend services using Java and Spring Boot. You will write unit tests, manage database schemas, and build REST APIs.",Java;Spring Boot;SQL;REST APIs,55000,4
            4,Machine Learning Intern,AI Solutions,Austin,"Work on cutting-edge AI projects. You will help train, test, and deploy machine learning models for natural language processing (NLP).",Python;TensorFlow;PyTorch;Scikit-learn,70000,6
        """)
        with open(jobs_csv_path, "w", encoding="utf-8") as f:
            f.write(jobs_data)
        print(f"--- 📝 Created dummy jobs file at: {jobs_csv_path} ---")

        # 3. CREATE DUMMY parsed_resume.json FILE
        # This resume is strong in Python and Machine Learning
        resume_data = {
            'ai_summary': "A computer science student passionate about machine learning and data science. Proven experience in building and training deep learning models.",
            'skills': ["Python", "PyTorch", "TensorFlow", "Pandas", "NumPy", "SQL"],
            'experience': [
                {
                    'title': "Research Assistant",
                    'company': "Tech University",
                    'bullets': ["Assisted research on natural language processing models."]
                }
            ]
        }
        resume_json_path = os.path.join(test_dir, "parsed_resume.json")
        with open(resume_json_path, "w", encoding="utf-8") as f:
            json.dump(resume_data, f)
        print(f"--- 📄 Created dummy resume file at: {resume_json_path} ---")

        # Define paths for the script and its output
        core_logic_script_path = "core_logic.py" 
        output_json_path = os.path.join(test_dir, "recommendations.json")

        # 4. EXECUTE the core_logic.py script as a separate process
        command = [
            sys.executable,  # Path to the current python interpreter
            core_logic_script_path,
            resume_json_path,
            output_json_path
        ]

        print(f"\n--- ▶️  Running command: {' '.join(command)} ---\n")
        
        # This runs the script and waits for it to complete.
        # We capture stdout and stderr to see the print statements from the script.
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

        # Print the output from the core_logic.py script
        print("--- Script STDOUT: ---")
        print(result.stdout)
        if result.stderr:
            print("--- Script STDERR: ---")
            print(result.stderr)
        
        print("\n--- ✅ Script execution finished ---")

        # 5. VERIFY AND PRINT THE RESULTS
        if os.path.exists(output_json_path):
            print(f"\n---  sonuçları okuma / Reading results from: {output_json_path} ---")
            with open(output_json_path, "r", encoding="utf-8") as f:
                recommendations = json.load(f)
            
            print("\n" + "="*50)
            print("          RECOMMENDATION RESULTS")
            print("="*50)
            print(json.dumps(recommendations, indent=2))
            print("="*50)

        else:
            print("\n--- ❌ TEST FAILED: Output file was not created. ---")

    finally:
        # 6. CLEANUP: Remove the temporary directory and its contents
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print(f"\n--- 🧹 Cleaned up and removed directory: {test_dir} ---")

if __name__ == "__main__":
    run_core_logic_test()
