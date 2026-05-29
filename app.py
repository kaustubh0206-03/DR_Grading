import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.styles import inject_global_css
from utils.database import init_database

st.set_page_config(
    page_title="RetinaGuard AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "RetinaGuard AI v2.0 — Advanced Diabetic Retinopathy Screening Platform"
    }
)

init_database()
inject_global_css()

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">👁️</div>
        <div class="logo-text">
            <span class="logo-title">RetinaGuard</span>
            <span class="logo-subtitle">AI Screening Platform</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-section-label">MAIN</div>', unsafe_allow_html=True)

    pages = {
        "🏠  Home": "home",
        "🔬  DR Screening": "predict",
        "🧠  Explainability": "explainability",
        "📊  Analytics": "analytics",
        "📋  History": "history",
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    for label, key in pages.items():
        is_active = st.session_state.current_page == key
        btn_class = "nav-btn-active" if is_active else "nav-btn"
        if st.button(label, key=f"nav_{key}", width="stretch"):
            st.session_state.current_page = key
            st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-info">
        <div class="info-badge">⚕️ Clinical Decision Support</div>
        <p class="info-text">AI-assisted screening tool. All results require professional medical review.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-footer">
        <span>RetinaGuard AI v2.0</span><br>
        <span style="color:#475569; font-size:10px;">© 2026 · All rights reserved</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Page Router ─────────────────────────────────────────────────────────────
page = st.session_state.current_page

if page == "home":
    from pages.home import render
    render()
elif page == "predict":
    from pages.predict import render
    render()
elif page == "explainability":
    from pages.explainability import render
    render()
elif page == "analytics":
    from pages.analytics import render
    render()
elif page == "history":
    from pages.history import render
    render()
