import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

# ==========================================
# LOAD ENV
# ==========================================
load_dotenv()

# ==========================================
# LLM SETUP
# ==========================================
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0
)

# ==========================================
# TOOL: Vendor Search
# ==========================================
@tool("Search Vendor Database")
def search_vendors(category: str) -> str:
    """Search internal vendor database by category."""
    try:
        with open('data/vendors.json', 'r') as file:
            vendors = json.load(file)

        results = [
            v for v in vendors 
            if v.get('category', '').lower() == category.lower()
        ]

        return json.dumps(results, indent=2) if results else "No vendors found."

    except Exception as e:
        return f"Error reading database: {str(e)}"


# ==========================================
# MAIN FUNCTION
# ==========================================
def run_procurement_ai(user_request: str):

    # -------- AGENT 1 --------
    intake_agent = Agent(
        role='Procurement Intake Specialist',
        goal='Extract structured procurement details from user input.',
        backstory='Expert in converting natural language into structured JSON.',
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    intake_task = Task(
        description=f"""
        Analyze the user request below and extract structured data.

        REQUEST:
        "{user_request}"

        OUTPUT FORMAT (STRICT JSON):
        {{
            "item": "",
            "quantity": "",
            "budget": "",
            "department": "",
            "category": ""
        }}

        Only return JSON. No explanation.
        """,
        expected_output="Valid JSON only.",
        agent=intake_agent
    )

    # -------- AGENT 2 --------
    discovery_agent = Agent(
        role='Vendor Discovery Specialist',
        goal='Find best vendors using internal database.',
        backstory='Expert in vendor sourcing and evaluation.',
        tools=[search_vendors],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    discovery_task = Task(
        description="""
        Use the JSON output from the intake agent.

        Steps:
        1. Extract the "category"
        2. Call "Search Vendor Database"
        3. Return structured result:

        {
            "vendors": [
                {
                    "name": "",
                    "compliance_score": "",
                    "delivery_days": ""
                }
            ]
        }

        Only return JSON.
        """,
        expected_output="JSON list of vendors.",
        agent=discovery_agent
    )

    # -------- CREW --------
    crew = Crew(
        agents=[intake_agent, discovery_agent],
        tasks=[intake_task, discovery_task],
        process=Process.sequential
    )

    try:
        result = crew.kickoff()

        # Try parsing result safely
        try:
            return json.loads(result)
        except:
            return {"raw_output": result}

    except Exception as e:
        return {"error": str(e)}


# ==========================================
# TEST RUN
# ==========================================
if __name__ == "__main__":
    sample_request = "I need 50 Dell monitors for the engineering team by next week. Budget is 15000."

    output = run_procurement_ai(sample_request)

    print("\nFINAL OUTPUT:\n")
    print(json.dumps(output, indent=2))