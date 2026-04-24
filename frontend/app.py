import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os

# 1. INITIAL CONFIG
load_dotenv()
st.set_page_config(page_title="ProcureAI | Enterprise Edition", layout="wide")

# CUSTOM CSS: High-Visibility Dark Mode
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp { 
        background-color: #0E1117; 
        color: #FFFFFF; 
    }
    
    /* Input Text Areas and Boxes */
    .stTextArea textarea, .stNumberInput input, .stTextInput input {
        background-color: #1A1C24 !important;
        color: #00FFAA !important;
        border: 2px solid #30363D !important;
        border-radius: 10px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00FFAA !important;
        box-shadow: 0 0 10px #00FFAA !important;
    }

    /* Buttons - High Contrast */
    .stButton>button {
        background-color: #00FFAA !important;
        color: #0E1117 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 15px 30px !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #00CC88 !important;
        transform: scale(1.02);
    }

    /* Agent Cards */
    .agent-card { 
        background-color: #161B22; 
        border: 1px solid #30363D; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 10px;
    }

    /* Sidebar Fix */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
    }
    
    h1, h2, h3, p { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'step' not in st.session_state:
    st.session_state.step = "Intake"
if 'vendors' not in st.session_state:
    st.session_state.vendors = []

# 3. SIDEBAR AGENT MONITOR
st.sidebar.title("🤖 Agent Registry")
st.sidebar.divider()
agents = {
    "Intake": "🎯", "Discovery": "🔍", "Market": "📊", 
    "Compliance": "🛡️", "Risk": "⚖️", "Draftsman": "📝"
}

for name, icon in agents.items():
    if st.session_state.step == name:
        st.sidebar.markdown(f"### <span style='color:#00FFAA'>{icon} {name}</span>", unsafe_allow_html=True)
        st.sidebar.caption("⚡ Currently Processing...")
    else:
        st.sidebar.markdown(f"**{icon} {name}**", unsafe_allow_html=True)
        st.sidebar.caption("💤 Standby")
st.sidebar.divider()

# 4. STEP-BY-STEP INTERACTIVE UI

# --- STEP 1: INTAKE ---
if st.session_state.step == "Intake":
    st.title("🎯 Intake Agent")
    st.markdown("#### Validating requirements and budget availability.")
    
    with st.container():
        user_input = st.text_area("What are we sourcing today?", 
                                placeholder="e.g. 50 Laptops for Engineering department in Bengaluru...", 
                                height=150)
        budget = st.number_input("Estimated Budget Cap ($)", value=12000)
        
        st.markdown("---")
        if st.button("🚀 INITIATE AGENT PIPELINE"):
            if user_input:
                with st.status("Intake Agent: Validating requirements..."):
                    time.sleep(1.5)
                    st.session_state.step = "Discovery"
                    st.rerun()
            else:
                st.warning("Please enter a request to start.")

# --- STEP 2: DISCOVERY ---
elif st.session_state.step == "Discovery":
    st.title("🔍 Discovery Agent")
    st.success("Requirements validated. Scanning the Bengaluru vendor ecosystem.")
    
    with st.status("Searching Manyata Tech Park, SP Road, and Global Markets...", expanded=True):
        time.sleep(1)
        st.write("✅ Found TechSolutions Inc (International)")
        time.sleep(1)
        st.write("✅ Found Global IT Supplies (Local - Manyata Hub)")
        time.sleep(1)
        st.write("✅ Found SP Road Corporate Hub (Local)")
    
    if st.button("ANALYZE MARKET QUOTES →"):
        st.session_state.step = "Market"
        st.rerun()

# --- STEP 3: MARKET ANALYSIS ---
elif st.session_state.step == "Market":
    st.title("📊 Market Analyst Agent")
    st.markdown("#### Comparing pricing and lead times from discovered vendors.")
    
    col1, col2 = st.columns(2)
    df = pd.DataFrame({
        'Vendor': ['TechSolutions', 'Global IT', 'SP Road Hub'],
        'Price ($)': [11500, 10800, 10200],
        'Lead Time (Days)': [10, 4, 1]
    })
    
    with col1:
        fig = px.bar(df, x='Vendor', y='Price ($)', color='Vendor', 
                    title="Price Benchmarking", template="plotly_dark",
                    color_discrete_sequence=["#00FFAA", "#00CC88", "#009966"])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.pie(df, values='Lead Time (Days)', names='Vendor', 
                     title="Delivery Speed Distribution", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
        
    if st.button("AUDIT COMPLIANCE & RISK →"):
        st.session_state.step = "Compliance"
        st.rerun()

# --- STEP 4 & 5: COMPLIANCE & RISK ---
elif st.session_state.step == "Compliance":
    st.title("🛡️ Compliance & Risk Auditor")
    st.warning("Verifying vendor certifications and assessing supply chain risk.")
    
    cols = st.columns(3)
    scores = [94, 82, 71]
    vendors = ["TechSolutions", "Global IT", "SP Road Hub"]
    
    for i, col in enumerate(cols):
        with col:
            st.metric(vendors[i], f"{scores[i]}%", "Trust Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=scores[i],
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#00FFAA"}},
                title={'text': "Compliance Index", 'font': {'color': 'white'}}
            ))
            fig.update_layout(height=250, margin=dict(t=50, b=0), template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    if st.button("DRAFT PURCHASE ORDER →"):
        st.session_state.step = "Draftsman"
        st.rerun()

# --- STEP 6: DRAFTSMAN & APPROVAL ---
elif st.session_state.step == "Draftsman":
    st.title("📝 PO Draftsman Agent")
    st.success("Analysis complete. Final Purchase Order ready for execution.")
    
    st.markdown(f"""
        <div style="background:#1A1C24; border: 2px solid #00FFAA; color:white; padding:30px; border-radius:15px; margin-bottom: 25px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="color:#00FFAA !important; margin:0;">PURCHASE ORDER</h2>
                    <p style="margin:5px 0;">Vendor: <b>Global IT Supplies (Bengaluru Hub)</b></p>
                </div>
                <div style="text-align:right;">
                    <h1 style="color:#FFFFFF !important; margin:0;">#PO-2026-091</h1>
                </div>
            </div>
            <hr style="border: 0.5px solid #30363D;">
            <div style="display:flex; justify-content:space-between;">
                <p>TOTAL CONTRACT VALUE: <br><span style="font-size:24px; color:#00FFAA;">$10,800.00</span></p>
                <p style="text-align:right;">EXPECTED DELIVERY: <br><span style="font-size:24px; color:#FFFFFF;">3-5 Days</span></p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ APPROVE & ISSUE PO"):
            st.balloons()
            st.success("Workflow Complete. PO successfully pushed to ERP system.")
    with col_b:
        if st.button("❌ REJECT & RESET"):
            st.session_state.step = "Intake"
            st.rerun()