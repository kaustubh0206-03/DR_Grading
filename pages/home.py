import streamlit as st


def render():
    # ── Hero Section ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="animate-fade-in" style="text-align:center; padding: 2.5rem 1rem 1.5rem;">
        <div style="font-size:3.5rem; margin-bottom:0.75rem;
            filter: drop-shadow(0 0 30px rgba(59,130,246,0.4));
            line-height:1;">
            <span style="display:inline-block; animation: float 4s ease-in-out infinite;">🔬</span>
        </div>
        <h1 style="font-family:'Space Grotesk',sans-serif; font-size:2.8rem; font-weight:800;
            background:linear-gradient(135deg,#0F172A 0%,#1E40AF 40%,#3B82F6 70%,#06B6D4 100%);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text;
            margin-bottom:0.5rem; line-height:1.1;
            background-size: 200% 100%;
            animation: gradient-shift 8s ease infinite;">
            DR GRADING
        </h1>
        <div style="margin-bottom: 1rem;">
            <span class="badge badge-blue" style="font-size:0.75rem; padding:0.3rem 1rem;">AI-Powered Retinal Screening Platform</span>
        </div>
        <p style="font-size:1.05rem; color:#64748B; max-width:640px; margin:0 auto 1.25rem;
            font-weight:400; line-height:1.7;">
            Next-generation diabetic retinopathy screening powered by a hybrid CNN + Vision Transformer
            architecture. Clinical-grade artificial intelligence for early detection and prevention of vision loss.
        </p>
        <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-bottom:2rem;">
            <span class="badge badge-blue">🧠 CNN + ViT Hybrid</span>
            <span class="badge badge-cyan">⚕️ 5-Class Grading</span>
            <span class="badge badge-purple">🔬 Grad-CAM Explainability</span>
            <span class="badge badge-green">📊 Clinical Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("Start Screening", key="home_cta", width="stretch"):
            st.session_state.current_page = "predict"
            st.rerun()

    # ── Stats Row ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <h2 class="section-title" style="text-align:center;">Platform Overview</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("5-Class", "DR Grading", "#2563EB"),
        (">92%", "AUC-ROC", "#10B981"),
        ("<2s", "Inference", "#06B6D4"),
        ("2.1M", "Parameters", "#8B5CF6"),
    ]
    for col, (val, label, color) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── How It Works ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <h2 class="section-title" style="text-align:center;">Clinical Workflow</h2>
    """, unsafe_allow_html=True)

    workflow_steps = [
        ("📤", "Upload Image", "Retinal fundus photograph from standard camera"),
        ("🔍", "Quality Check", "Automated image quality assessment"),
        ("🧠", "AI Analysis", "CNN + ViT hybrid inference engine"),
        ("📋", "Clinical Report", "Grad-CAM visualization & clinical summary"),
    ]

    cols = st.columns(len(workflow_steps))
    for col, (icon, title, desc) in zip(cols, workflow_steps):
        with col:
            st.markdown(f"""
            <div class="rg-card" style="text-align:center; padding:1.25rem 1rem; height:100%;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:600; color:#0F172A; margin-bottom:0.3rem;">{title}</h4>
                <p style="font-size:0.72rem; color:#64748B; line-height:1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ── Disease Severity ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <h2 class="section-title" style="text-align:center;">Diabetic Retinopathy Severity Grades</h2>
    """, unsafe_allow_html=True)

    severity_cards = [
        ("No DR", "Normal retinal examination. No microaneurysms, hemorrhages, or exudates.",
         "#10B981", "✅", "Annual screening"),
        ("Mild NPDR", "Few microaneurysms and dot-blot hemorrhages. Early stage.",
         "#F59E0B", "⚠️", "12-month follow-up"),
        ("Moderate NPDR", "Multiple hemorrhages, exudates, and IRMA. Referral indicated.",
         "#F97316", "🔶", "3-6 month follow-up"),
        ("Severe NPDR", "Extensive hemorrhages, venous beading. High-risk pre-proliferative.",
         "#EF4444", "🚨", "1-3 month follow-up"),
        ("PDR", "Neovascularization, vitreous hemorrhage. Vision-threatening emergency.",
         "#A855F7", "🆘", "Immediate referral"),
    ]

    for sev, desc, color, icon, fup in severity_cards:
        st.markdown(f"""
        <div class="rg-card" style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem; padding:0.9rem 1.25rem;">
            <div style="font-size:1.3rem; flex-shrink:0;">{icon}</div>
            <div style="flex:1;">
                <div style="font-weight:600; font-size:0.88rem; color:{color};">{sev}</div>
                <div style="font-size:0.74rem; color:#64748B; margin-top:0.15rem;">{desc}</div>
            </div>
            <div style="text-align:right; flex-shrink:0;">
                <div style="font-size:0.65rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em;">Follow-up</div>
                <div style="font-size:0.78rem; font-weight:600; color:{color};">{fup}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Technology ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <h2 class="section-title" style="text-align:center;">Technology Stack</h2>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        <div class="rg-card" style="height:100%;">
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.9rem; font-weight:600; margin-bottom:0.75rem; color:#0F172A;">🧠 Model Architecture</h4>
        """, unsafe_allow_html=True)
        for k, v in [
            ("Backbone", "CNN + Vision Transformer"),
            ("Input Size", "224 x 224 x 3"),
            ("Parameters", "~2.1M (lightweight)"),
            ("Framework", "TensorFlow 2.x / Keras"),
            ("Output", "5-Class Softmax"),
            ("Explainability", "Grad-CAM Heatmaps"),
        ]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.3rem 0; border-bottom:1px solid #F1F5F9; font-size:0.78rem;">
                <span style="color:#64748B;">{k}</span>
                <span style="color:#0F172A; font-weight:500;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_t2:
        st.markdown("""
        <div class="rg-card" style="height:100%;">
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.9rem; font-weight:600; margin-bottom:0.75rem; color:#0F172A;">📊 Application Stack</h4>
        """, unsafe_allow_html=True)
        for k, v in [
            ("Frontend", "Streamlit + Custom CSS"),
            ("Visualization", "Plotly Interactive Charts"),
            ("Database", "SQLite (Local Storage)"),
            ("Reporting", "FPDF2 Hospital-Grade PDF"),
            ("Preprocessing", "OpenCV + CLAHE Enhancement"),
            ("Caching", "Streamlit Caching Layer"),
        ]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.3rem 0; border-bottom:1px solid #F1F5F9; font-size:0.78rem;">
                <span style="color:#64748B;">{k}</span>
                <span style="color:#0F172A; font-weight:500;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Disclaimer ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="rg-alert rg-alert-info" style="margin-top:1rem;">
        <strong>⚕️ Clinical Decision Support:</strong> DR GRADING is an AI-assisted screening platform
        designed to support clinical decision-making. All predictions and reports must be reviewed
        by a qualified ophthalmologist before any clinical action. This tool is NOT a substitute
        for professional medical examination.
    </div>
    """, unsafe_allow_html=True)
