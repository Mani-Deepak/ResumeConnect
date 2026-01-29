import os

class Config:
    """
    Configuration class for the application.
    Stores secret keys, API keys, and other settings.
    """
    
    # It's good practice to load secrets from environment variables
    # but you can hardcode them for testing if needed.
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-secret-key'
    
    # --- MODIFIED ---
    # Retrieve the Gemini API Key from environment variables.
    # Replace 'YOUR_API_KEY_HERE' with your actual key for local testing
    # if you are not using environment variables.
    GEMINI_API_KEY = 'YOUR_API_KEY_HERE'
    # --- END MODIFIED ---
    
    # Add any other configuration variables your app needs here.
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'docx', 'pdf'}