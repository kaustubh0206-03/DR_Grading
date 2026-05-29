import streamlit as st


def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #F8FAFC;
        color: #0F172A;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
    .stApp { background: #F8FAFC; }

    .block-container {
        padding: 1.5rem 2rem 3rem 2rem !important;
        max-width: 1320px !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2563EB; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid #1E293B !important;
    }
    [data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.25rem 0.5rem;
    }
    .logo-icon {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #2563EB, #06B6D4);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    }
    .logo-text { line-height: 1.2; }
    .logo-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    .logo-subtitle {
        font-size: 0.65rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #334155, transparent);
        margin: 1rem 0;
    }

    .nav-section-label {
        font-size: 0.6rem;
        color: #475569;
        letter-spacing: 0.12em;
        font-weight: 600;
        padding: 0.5rem 0.75rem 0.25rem;
    }

    .stButton button {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
        color: #94A3B8;
        text-align: left;
    }
    .stButton button:hover {
        background: rgba(37,99,235,0.12);
        color: #FFFFFF;
        transform: translateX(2px);
    }
    .stButton button:active { transform: translateX(0); }
    .stButton button p { font-size: 0.82rem; }

    div[data-testid="stSidebarNav"] { display: none; }

    .nav-btn-active button {
        background: rgba(37,99,235,0.15) !important;
        color: #60A5FA !important;
        border-left: 3px solid #2563EB !important;
        border-radius: 0 10px 10px 0 !important;
        font-weight: 600 !important;
    }

    .sidebar-info {
        background: rgba(37,99,235,0.08);
        border: 1px solid rgba(37,99,235,0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .info-badge {
        font-size: 0.7rem;
        font-weight: 600;
        color: #60A5FA;
        margin-bottom: 0.4rem;
    }
    .info-text {
        font-size: 0.68rem;
        color: #64748B;
        line-height: 1.5;
    }

    .sidebar-footer {
        padding: 1rem 0.5rem 0;
        font-size: 0.68rem;
        color: #475569;
        line-height: 1.6;
        text-align: center;
    }

    /* ── Page Header ── */
    .page-header {
        margin-bottom: 2rem;
    }
    .page-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.35rem;
        letter-spacing: -0.03em;
    }
    .page-header p {
        font-size: 0.88rem;
        color: #64748B;
        font-weight: 400;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    .section-subtitle {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 400;
        margin-bottom: 0.5rem;
    }

    /* ── Cards ── */
    .rg-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease forwards;
    }
    .rg-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
        transform: translateY(-1px);
    }
    .rg-card-glass {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease forwards;
    }
    .rg-card-glass:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease forwards;
    }
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        transform: translateY(-1px);
    }
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.15rem;
    }

    /* ── Badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 0.35rem 0.75rem;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    .badge-blue {
        background: rgba(37,99,235,0.08);
        color: #2563EB;
        border: 1px solid rgba(37,99,235,0.15);
    }
    .badge-cyan {
        background: rgba(6,182,212,0.08);
        color: #0891B2;
        border: 1px solid rgba(6,182,212,0.15);
    }
    .badge-green {
        background: rgba(16,185,129,0.08);
        color: #059669;
        border: 1px solid rgba(16,185,129,0.15);
    }
    .badge-purple {
        background: rgba(139,92,246,0.08);
        color: #7C3AED;
        border: 1px solid rgba(139,92,246,0.15);
    }
    .badge-yellow {
        background: rgba(245,158,11,0.08);
        color: #D97706;
        border: 1px solid rgba(245,158,11,0.15);
    }
    .badge-red {
        background: rgba(239,68,68,0.08);
        color: #DC2626;
        border: 1px solid rgba(239,68,68,0.15);
    }

    /* ── Alerts ── */
    .rg-alert {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        font-size: 0.82rem;
        line-height: 1.6;
        animation: fadeInUp 0.4s ease forwards;
    }
    .rg-alert-info {
        background: rgba(37,99,235,0.06);
        border: 1px solid rgba(37,99,235,0.15);
        color: #1D4ED8;
    }
    .rg-alert-warning {
        background: rgba(245,158,11,0.06);
        border: 1px solid rgba(245,158,11,0.15);
        color: #B45309;
    }
    .rg-alert-success {
        background: rgba(16,185,129,0.06);
        border: 1px solid rgba(16,185,129,0.15);
        color: #047857;
    }
    .rg-alert-error {
        background: rgba(239,68,68,0.06);
        border: 1px solid rgba(239,68,68,0.15);
        color: #B91C1C;
    }

    /* ── Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 16px rgba(37,99,235,0.15); }
        50% { box-shadow: 0 0 32px rgba(37,99,235,0.3); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes scan-line {
        0% { top: 0; }
        100% { top: 100%; }
    }
    @keyframes rotate-scan {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.3); }
    }

    .animate-fade-in { animation: fadeInUp 0.5s ease forwards; }
    .animate-pulse-glow { animation: pulse-glow 2.5s ease-in-out infinite; }

    .hover-lift {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hover-lift:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }

    /* ── Divider ── */
    .rg-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
        margin: 2rem 0;
    }

    /* ── Image Container ── */
    .img-container {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .img-container:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }

    /* ── Step Indicator ── */
    .step-indicator {
        display: flex;
        align-items: center;
        gap: 0;
        margin: 1.5rem 0;
        padding: 0;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        color: #94A3B8;
        font-weight: 500;
    }
    .step-item.active {
        color: #2563EB;
        font-weight: 600;
    }
    .step-item.completed {
        color: #059669;
    }
    .step-number {
        width: 22px; height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.65rem;
        font-weight: 700;
        background: #E2E8F0;
        color: #64748B;
        flex-shrink: 0;
    }
    .step-item.active .step-number {
        background: #2563EB;
        color: #FFFFFF;
    }
    .step-item.completed .step-number {
        background: #10B981;
        color: #FFFFFF;
    }
    .step-connector {
        width: 24px;
        height: 1px;
        background: #CBD5E1;
        margin: 0 6px;
    }

    /* ── Progress Bar ── */
    .progress-bar-container {
        width: 100%;
        height: 6px;
        background: #E2E8F0;
        border-radius: 3px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.6s ease;
        background: linear-gradient(90deg, #2563EB, #06B6D4);
    }

    /* ── Status Dot ── */
    .status-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: pulse-dot 2s ease-in-out infinite;
    }

    /* ── Custom Button ── */
    .rg-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.25s ease;
        text-decoration: none;
    }
    .rg-btn-primary {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(37,99,235,0.25);
    }
    .rg-btn-primary:hover {
        box-shadow: 0 4px 16px rgba(37,99,235,0.35);
        transform: translateY(-1px);
    }
    .rg-btn-secondary {
        background: #F1F5F9;
        color: #0F172A;
        border: 1px solid #E2E8F0;
    }
    .rg-btn-secondary:hover {
        background: #E2E8F0;
        transform: translateY(-1px);
    }
    .rg-btn-success {
        background: linear-gradient(135deg, #10B981, #059669);
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(16,185,129,0.25);
    }
    .rg-btn-danger {
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(239,68,68,0.25);
    }

    /* ── Upload Zone ── */
    .upload-zone {
        background: #FFFFFF;
        border: 2px dashed #CBD5E1;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .upload-zone:hover {
        border-color: #2563EB;
        background: rgba(37,99,235,0.02);
    }
    .upload-zone.has-file {
        border-color: #10B981;
        background: rgba(16,185,129,0.02);
        border-style: solid;
    }

    /* ── Prediction Card ── */
    .prediction-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    .prediction-class {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .prediction-confidence {
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    /* ── Confusion Matrix Cell ── */
    .cm-cell {
        width: 48px; height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ── Timeline ── */
    .timeline-item {
        position: relative;
        padding-left: 20px;
        padding-bottom: 1rem;
        border-left: 2px solid #E2E8F0;
    }
    .timeline-item:last-child { border-left-color: transparent; }
    .timeline-dot {
        position: absolute;
        left: -5px;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #2563EB;
    }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        .page-header h1 { font-size: 1.5rem; }
        .metric-value { font-size: 1.4rem; }
        .prediction-class { font-size: 1.1rem; }
    }
    @media (max-width: 480px) {
        .block-container { padding: 0.75rem !important; }
        .page-header h1 { font-size: 1.25rem; }
        .metric-value { font-size: 1.2rem; }
    }

    /* ── Data Table Styling ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    [data-testid="stDataFrame"] th {
        background: #F8FAFC;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stDataFrame"] td {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #FFFFFF;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        color: #64748B;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
    }

    /* ── Spinner override ── */
    .stSpinner > div {
        border-color: #2563EB !important;
        border-top-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
