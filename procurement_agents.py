import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def run_procurement_flow(user_request):
    # This function uses direct Gemini calls instead of CrewAI
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Make sure this path points to your data folder
        data_file = os.path.join(base_path, '..', 'data', 'vendors.json') 
        
        with open(data_file, 'r') as f:
            vendor_data = f.read()
    except:
        vendor_data = "[]" # Fallback if file isn't found

    prompt = f"""
    You are an Autonomous Procurement System.
    Act as an Intake Agent and a Discovery Agent.
    Request: {user_request}
    Vendor Data: {vendor_data}
    
    Provide a final recommendation.
    """
    response = model.generate_content(prompt)
    return response.text