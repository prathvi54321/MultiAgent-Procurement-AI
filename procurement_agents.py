import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0 
)

# ==========================================
# CUSTOM TOOL: Mock Database Search
# ==========================================
@tool("Search Vendor Database")
def search_vendors(category: str) -> str:
    """Useful for searching the internal database for vendors by category."""
    try:
        with open('data/vendors.json', 'r') as file:
            vendors = json.load(file)
            results = [v for v in vendors if v['category'].lower() == category.lower()]
            return json.dumps(results, indent=2) if results else "No vendors found for this category."
    except Exception as e:
        return f"Error reading database: {e}"

# ==========================================
# AGENT 1: The Intake Specialist 
# ==========================================
intake_agent = Agent(
    role='Procurement Intake Specialist',
    goal='Extract the exact item name, quantity, budget, and department from user requests into JSON format.',
    backstory='You extract data from natural language requests into strict JSON format with keys: item, quantity, budget, department, and category.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)

intake_task = Task(
    description='''Analyze this request: "{user_request}". 
    Extract the details into JSON. Also, infer the broad 'category' of the item (e.g., if it's monitors, the category is 'Electronics').
    Expected JSON keys: item, quantity, budget, department, category.''',
    expected_output='A valid JSON object.',
    agent=intake_agent
)

# ==========================================
# AGENT 2: The Discovery Agent
# ==========================================
discovery_agent = Agent(
    role='Vendor Discovery Specialist',
    goal='Find suitable vendors for the requested items using the internal database.',
    backstory='You take the extracted JSON requirements and search the company vendor database to find the best suppliers.',
    tools=[search_vendors],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

discovery_task = Task(
    description='''Take the JSON output from the Intake Specialist. 
    1. Identify the 'category' of the item.
    2. Use the Search Vendor Database tool to find vendors matching that category.
    3. Return a list of the matching vendors, including their names, compliance scores, and delivery days.''',
    expected_output='A clear list of potential vendors with their key stats.',
    agent=discovery_agent
)

if __name__ == "__main__":
    sample_request = "I need 50 Dell monitors for the engineering team by next week. The budget is 15000."
    
def run_procurement_ai(user_request):
    """This function will be called by Prajwal's UI"""
    procurement_crew = Crew(
        agents=[intake_agent, discovery_agent],
        tasks=[intake_task, discovery_task],
        process=Process.sequential
    )
    
    # Execute the AI logic
    result = procurement_crew.kickoff(inputs={'user_request': user_request})
    return result