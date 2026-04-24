import streamlit as st
import time
import sys
import os


# Add backend folder to path
sys.path.append(os.path.abspath("../backend"))

from agents import *

st.set_page_config(page_title="SmartProcure AI", layout="wide")

# Sidebar
st.sidebar.title("🤖 Agent Status")

status = {
    "Intake Agent": "Pending",
    "Vendor Agent": "Pending",
    "Quote Agent": "Pending",
    "Compliance Agent": "Pending",
    "Approval Agent": "Pending",
    "PO Agent": "Pending"
}

status_placeholder = st.sidebar.empty()

def update_status(agent, state):
    status[agent] = state
    status_placeholder.write(status)

# UI
st.title("📦 SmartProcure AI")
st.subheader("Multi-Agent Procurement System")

query = st.text_input("Enter procurement request:")

if st.button("Run Procurement"):

    if query == "":
        st.warning("Please enter a request!")
    else:

        # 1 Intake
        update_status("Intake Agent", "Processing...")
        time.sleep(1)
        data = intake_agent(query)
        update_status("Intake Agent", "Done")

        # 2 Vendor
        update_status("Vendor Agent", "Searching...")
        time.sleep(1)
        vendors = vendor_agent()
        update_status("Vendor Agent", "Done")

        # 3 Quote
        update_status("Quote Agent", "Analyzing...")
        time.sleep(1)
        vendors = quote_agent(vendors)
        update_status("Quote Agent", "Done")

        # 4 Compliance
        update_status("Compliance Agent", "Checking...")
        time.sleep(1)
        vendors = compliance_agent(vendors)

        if len(vendors) == 0:
            st.error("❌ No compliant vendors found!")
            st.stop()

        update_status("Compliance Agent", "Done")

        # Best vendor
        best = vendors[0]

        # 5 Approval
        update_status("Approval Agent", "Processing...")
        time.sleep(1)
        total_cost = best["price"] * data["quantity"]
        approval = approval_agent(total_cost)
        update_status("Approval Agent", "Done")

        # 6 PO
        update_status("PO Agent", "Generating...")
        time.sleep(1)
        po = po_agent(best, data["quantity"])
        update_status("PO Agent", "Done")

        # Display
        st.success("✅ Procurement Completed")

        st.write("### 📊 Vendor Comparison")
        st.table(vendors)

        st.write("### 🏆 Recommended Vendor")
        st.success(f"{best['vendor']} (₹{best['price']})")

        st.write("### 💰 Total Cost")
        st.info(f"₹{total_cost}")

        st.write("### ✅ Approval Status")
        st.info(approval)

        st.write("### 📄 Purchase Order")
        st.code(po)

        # Buttons
        col1, col2 = st.columns(2)

        if col1.button("Approve"):
            st.success("Order Approved ✅")

        if col2.button("Reject"):
            st.error("Order Rejected ❌")