import streamlit as st
import time

# Set up the page layout
st.set_page_config(page_title="Autonomous Procurement AI", page_icon="📦", layout="centered")

# Customizing the header
st.title("📦 Autonomous Procurement Agent")
st.markdown("""
Welcome to the Digital Assembly Line. Enter your purchase request below, and our multi-agent AI will autonomously handle intake, vendor discovery, and compliance checks.
""")
st.divider()

# The Chat Input Interface
st.subheader("New Purchase Request")
user_input = st.text_area(
    "Describe what you need to buy:", 
    placeholder="e.g., I need 50 Dell monitors for the engineering team by next week. The budget is $15,000.",
    height=100
)

# The Execution Block
if st.button("🚀 Process Request", type="primary", use_container_width=True):
    if not user_input:
        st.warning("Please enter a request first!")
    else:
        # This creates a cool animated dropdown showing the agents working
        with st.status("Robotic Agents Initializing...", expanded=True) as status:
            
            st.write("🕵️‍♂️ **Intake Agent:** Analyzing request and extracting parameters...")
            time.sleep(2) # Fake delay for visual effect
            st.success("Intake complete: Extracted JSON data.")
            
            st.write("🔍 **Discovery Agent:** Searching internal vendor database...")
            time.sleep(2)
            st.success("Discovery complete: Found 2 matching vendors.")
            
            status.update(label="Workflow Complete!", state="complete", expanded=False)

        # Mock Final Output (We will connect the REAL AI output here in Sprint 2)
        st.divider()
        st.subheader("✅ Final Procurement Recommendation")
        
        st.markdown("""
        **Category Found:** Electronics
        
        **Recommended Vendors:**
        1. **TechSupply Co.** (Compliance Score: 98, Delivery: 3 days)
        2. **Global Monitors Inc.** (Compliance Score: 60, Delivery: 14 days)
        
        *Action Required:* Awaiting human approval to generate Purchase Order.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("✅ Approve & Generate PO", use_container_width=True)
        with col2:
            st.button("❌ Reject Request", use_container_width=True)