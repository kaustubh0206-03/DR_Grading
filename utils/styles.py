import streamlit as st


def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #F0F5FF;
        color: #0F172A;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    .stApp {
        background: 
            radial-gradient(ellipse 80% 60% at 0% 0%, rgba(37,99,235,0.04) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 100% 100%, rgba(6,182,212,0.04) 0%, transparent 60%),
            radial-gradient(ellipse 50% 40% at 50% 50%, rgba(139,92,246,0.02) 0%, transparent 50%),
            #F0F5FF;
    }

    .block-container {
        padding: 1.5rem 2rem 3rem 2rem !important;
        max-width: 1320px !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #3B82F6, #06B6D4); }

    /* ── Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 16px rgba(37,99,235,0.15); }
        50% { box-shadow: 0 0 40px rgba(37,99,235,0.3); }
    }
    @keyframes pulse-glow-cyan {
        0%, 100% { box-shadow: 0 0 16px rgba(6,182,212,0.15); }
        50% { box-shadow: 0 0 40px rgba(6,182,212,0.3); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes scan-line {
        0% { top: -2px; }
        100% { top: 100%; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-10px) rotate(1deg); }
        66% { transform: translateY(5px) rotate(-1deg); }
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.3); }
    }
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes border-glow {
        0%, 100% { border-color: rgba(37,99,235,0.2); }
        50% { border-color: rgba(37,99,235,0.5); }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    /* ── Floating Orbs ── */
    .bg-orb {
        position: fixed;
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: float 8s ease-in-out infinite;
        opacity: 0.3;
    }
    .bg-orb-1 {
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(37,99,235,0.08) 0%, transparent 70%);
        top: -100px; left: -100px;
        animation-delay: 0s;
    }
    .bg-orb-2 {
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(6,182,212,0.06) 0%, transparent 70%);
        bottom: -80px; right: -80px;
        animation-delay: -3s;
    }
    .bg-orb-3 {
        width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(139,92,246,0.05) 0%, transparent 70%);
        top: 40%; left: 60%;
        animation-delay: -5s;
        animation-duration: 10s;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1120 0%, #162032 50%, #1A2538 100%) !important;
        border-right: 1px solid rgba(37,99,235,0.15) !important;
        position: relative;
        overflow: hidden;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3B82F6, #06B6D4, transparent);
    }
    [data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem;
        position: relative;
        z-index: 1;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.25rem 0.5rem;
        animation: fadeIn 0.6s ease;
    }
    .logo-icon {
        width: 44px; height: 44px;
        background: linear-gradient(135deg, #3B82F6, #06B6D4);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        box-shadow: 0 4px 16px rgba(37,99,235,0.35);
        position: relative;
        flex-shrink: 0;
    }
    .logo-icon::after {
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 16px;
        background: linear-gradient(135deg, #3B82F6, #06B6D4);
        opacity: 0.3;
        z-index: -1;
        animation: pulse-glow 3s ease-in-out infinite;
    }
    .logo-text { line-height: 1.2; }
    .logo-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF 60%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    .logo-subtitle {
        font-size: 0.6rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-top: 1px;
    }

    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59,130,246,0.3), rgba(6,182,212,0.3), transparent);
        margin: 1rem 0;
    }

    .nav-section-label {
        font-size: 0.6rem;
        color: #475569;
        letter-spacing: 0.15em;
        font-weight: 600;
        padding: 0.5rem 0.75rem 0.25rem;
    }

    .stButton button {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        background: transparent;
        color: #94A3B8;
        text-align: left;
        position: relative;
        overflow: hidden;
    }
    .stButton button:hover {
        background: rgba(59,130,246,0.1);
        color: #FFFFFF;
        transform: translateX(3px);
    }
    .stButton button:active { transform: translateX(0); }
    .stButton button p { font-size: 0.82rem; }

    div[data-testid="stSidebarNav"] { display: none; }

    .nav-btn-active button {
        background: rgba(59,130,246,0.15) !important;
        color: #93C5FD !important;
        border-left: 3px solid #3B82F6 !important;
        border-radius: 0 10px 10px 0 !important;
        font-weight: 600 !important;
        box-shadow: inset 0 0 20px rgba(59,130,246,0.05) !important;
    }

    .sidebar-info {
        background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(6,182,212,0.04));
        border: 1px solid rgba(59,130,246,0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .info-badge {
        font-size: 0.7rem;
        font-weight: 600;
        color: #93C5FD;
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
        border-top: 1px solid rgba(59,130,246,0.08);
    }
    .sidebar-footer .version {
        font-family: 'JetBrains Mono', monospace;
        color: #3B82F6;
        font-size: 0.65rem;
    }

    /* ── Page Header ── */
    .page-header {
        margin-bottom: 2rem;
        animation: fadeInUp 0.6s ease;
    }
    .page-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0F172A 0%, #1E40AF 50%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
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
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(226,232,240,0.6);
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease forwards;
        position: relative;
        overflow: hidden;
    }
    .rg-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59,130,246,0.2), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .rg-card:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04);
        transform: translateY(-2px);
        border-color: rgba(59,130,246,0.2);
        background: rgba(255,255,255,0.95);
    }
    .rg-card:hover::before {
        opacity: 1;
    }
    .rg-card-glass {
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.4);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.04);
        transition: all 0.4s ease;
        animation: fadeInUp 0.6s ease forwards;
    }
    .rg-card-glass:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        background: rgba(255,255,255,0.75);
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        border: 1px solid rgba(226,232,240,0.5);
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        transition: all 0.4s ease;
        animation: fadeInUp 0.6s ease forwards;
        position: relative;
        overflow: hidden;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 20%; right: 20%;
        height: 2px;
        border-radius: 1px;
        background: linear-gradient(90deg, transparent, currentColor, transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .metric-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        transform: translateY(-2px);
        border-color: rgba(59,130,246,0.15);
        background: rgba(255,255,255,0.95);
    }
    .metric-card:hover::after {
        opacity: 0.3;
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
        transition: all 0.3s ease;
    }
    .badge:hover {
        transform: translateY(-1px);
    }
    .badge-blue {
        background: rgba(59,130,246,0.08);
        color: #2563EB;
        border: 1px solid rgba(59,130,246,0.15);
    }
    .badge-blue:hover {
        background: rgba(59,130,246,0.12);
        box-shadow: 0 2px 8px rgba(59,130,246,0.15);
    }
    .badge-cyan {
        background: rgba(6,182,212,0.08);
        color: #0891B2;
        border: 1px solid rgba(6,182,212,0.15);
    }
    .badge-cyan:hover {
        background: rgba(6,182,212,0.12);
        box-shadow: 0 2px 8px rgba(6,182,212,0.15);
    }
    .badge-green {
        background: rgba(16,185,129,0.08);
        color: #059669;
        border: 1px solid rgba(16,185,129,0.15);
    }
    .badge-green:hover {
        background: rgba(16,185,129,0.12);
    }
    .badge-purple {
        background: rgba(139,92,246,0.08);
        color: #7C3AED;
        border: 1px solid rgba(139,92,246,0.15);
    }
    .badge-purple:hover {
        background: rgba(139,92,246,0.12);
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
        animation: fadeInUp 0.5s ease forwards;
    }
    .rg-alert-info {
        background: linear-gradient(135deg, rgba(59,130,246,0.06), rgba(6,182,212,0.04));
        border: 1px solid rgba(59,130,246,0.15);
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

    .animate-fade-in { animation: fadeInUp 0.6s ease forwards; }
    .animate-slide-left { animation: slideInLeft 0.6s ease forwards; }
    .animate-slide-right { animation: slideInRight 0.6s ease forwards; }
    .animate-scale-in { animation: scaleIn 0.5s ease forwards; }
    .animate-pulse-glow { animation: pulse-glow 3s ease-in-out infinite; }

    .hover-lift {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hover-lift:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.08);
    }

    /* ── Divider ── */
    .rg-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148,163,184,0.3), rgba(59,130,246,0.2), rgba(148,163,184,0.3), transparent);
        margin: 2rem 0;
    }

    /* ── Image Container ── */
    .img-container {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(226,232,240,0.5);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.4s ease;
    }
    .img-container:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        border-color: rgba(59,130,246,0.2);
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
        color: #3B82F6;
        font-weight: 600;
    }
    .step-item.completed {
        color: #10B981;
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
        transition: all 0.3s ease;
    }
    .step-item.active .step-number {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(59,130,246,0.3);
    }
    .step-item.completed .step-number {
        background: linear-gradient(135deg, #10B981, #059669);
        color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(16,185,129,0.3);
    }
    .step-connector {
        width: 24px;
        height: 1px;
        background: linear-gradient(90deg, #CBD5E1, rgba(59,130,246,0.3));
        margin: 0 6px;
    }

    /* ── Progress Bar ── */
    .progress-bar-container {
        width: 100%;
        height: 6px;
        background: rgba(226,232,240,0.5);
        border-radius: 3px;
        overflow: hidden;
        position: relative;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(90deg, #3B82F6, #06B6D4, #3B82F6);
        background-size: 200% 100%;
        animation: shimmer 2s linear infinite;
        position: relative;
    }

    /* ── Status Dot ── */
    .status-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: pulse-dot 2s ease-in-out infinite;
        box-shadow: 0 0 6px currentColor;
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-decoration: none;
        position: relative;
        overflow: hidden;
    }
    .rg-btn::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.1) 100%);
        pointer-events: none;
    }
    .rg-btn-primary {
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        color: #FFFFFF;
        box-shadow: 0 4px 16px rgba(59,130,246,0.3);
    }
    .rg-btn-primary:hover {
        box-shadow: 0 8px 32px rgba(59,130,246,0.4);
        transform: translateY(-2px);
    }
    .rg-btn-secondary {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(8px);
        color: #0F172A;
        border: 1px solid rgba(226,232,240,0.6);
    }
    .rg-btn-secondary:hover {
        background: rgba(255,255,255,0.95);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    .rg-btn-success {
        background: linear-gradient(135deg, #10B981, #059669);
        color: #FFFFFF;
        box-shadow: 0 4px 16px rgba(16,185,129,0.3);
    }
    .rg-btn-success:hover {
        box-shadow: 0 8px 32px rgba(16,185,129,0.4);
        transform: translateY(-2px);
    }
    .rg-btn-danger {
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: #FFFFFF;
        box-shadow: 0 4px 16px rgba(239,68,68,0.3);
    }

    /* ── Upload Zone ── */
    .upload-zone {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 2px dashed rgba(203,213,225,0.6);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
        animation: fadeInUp 0.6s ease;
    }
    .upload-zone:hover {
        border-color: #3B82F6;
        background: rgba(59,130,246,0.03);
        box-shadow: 0 4px 24px rgba(59,130,246,0.06);
    }
    .upload-zone.has-file {
        border-color: #10B981;
        background: rgba(16,185,129,0.03);
        border-style: solid;
    }

    /* ── Prediction Card ── */
    .prediction-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(226,232,240,0.5);
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.04);
        animation: scaleIn 0.5s ease;
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
        border-left: 2px solid rgba(226,232,240,0.5);
    }
    .timeline-item:last-child { border-left-color: transparent; }
    .timeline-dot {
        position: absolute;
        left: -5px;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3B82F6, #06B6D4);
        box-shadow: 0 0 8px rgba(59,130,246,0.3);
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
        border: 1px solid rgba(226,232,240,0.5);
    }
    [data-testid="stDataFrame"] th {
        background: linear-gradient(135deg, #F8FAFC, #F0F5FF);
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
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(226,232,240,0.5);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        color: #64748B;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(59,130,246,0.3) !important;
    }

    /* ── Spinner override ── */
    .stSpinner > div {
        border-color: #3B82F6 !important;
        border-top-color: transparent !important;
        border-width: 3px !important;
        width: 28px !important;
        height: 28px !important;
    }

    /* ── Progress bar override ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3B82F6, #06B6D4) !important;
    }

    /* ── Colorful Run Analysis Button (wraps st.button) ── */
    .analysis-btn-wrapper {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    }
    .analysis-btn-wrapper div[data-testid*="stButton"] {
        min-width: 280px;
    }
    </style>
    """, unsafe_allow_html=True)
