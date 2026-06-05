import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Overall page font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium background and card styling */
    .stApp {
        background: linear-gradient(135deg, #0f1123 0%, #060814 100%);
        color: #e2e8f0;
    }
    
    /* Header Gradient Banner */
    .header-banner {
        background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 70%, #0284c7 100%);
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(14, 165, 233, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .header-banner h1 {
        color: #ffffff !important;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .header-banner p {
        color: #bae6fd;
        font-size: 1.1rem;
        font-weight: 300;
        margin: 0;
    }
    
    /* Custom Card container */
    .custom-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .custom-card:hover {
        transform: translateY(-2px);
        border-color: rgba(14, 165, 233, 0.4);
    }
    
    /* Title inside card */
    .card-title {
        font-weight: 600;
        font-size: 1.25rem;
        color: #38bdf8;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Status pills styling */
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
    }
    .status-pending { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .status-progress { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    .status-resolved { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .status-rejected { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    
    /* Priority pills styling */
    .priority-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 8px;
    }
    .priority-high { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .priority-medium { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .priority-low { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

    /* Custom metrics block */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .metric-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)
