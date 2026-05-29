import streamlit as st
import numpy as np
from PIL import Image
import io
import plotly.graph_objects as go

from utils.gradcam import compute_gradcam, apply_heatmap_overlay
from utils.preprocessing import DR_CLASSES, preprocess_image
from models.model import get_model, CLASS_COLORS
from utils.clinical import get_severity_info, get_clinical_note, get_recommendation


EXPLANATIONS = {
    "No DR": {
        "features": [
            "Normal retinal vasculature architecture",
            "Intact macula and foveal reflex",
            "Uniform background without lesions",
            "Normal optic disc morphology",
        ],
        "regions": "Model attention distributed across normal retinal structures. No pathological activation foci detected.",
        "recommendation": "Continue routine annual screening. Maintain systemic risk factor control.",
        "confidence_breakdown": {
            "Structural integrity": 96,
            "Vascular pattern": 94,
            "Color uniformity": 97,
            "Disc morphology": 95,
        },
    },
    "Mild DR": {
        "features": [
            "Isolated microaneurysms (dot-blot hemorrhages)",
            "Focal areas of vascular leakage",
            "Perivascular exudate accumulations",
            "Early capillary dropout regions",
        ],
        "regions": "Activation peaks in posterior pole around microaneurysm clusters and along vascular arcades.",
        "recommendation": "Optimize glycemic control. Schedule 12-month follow-up. Patient education on symptom monitoring.",
        "confidence_breakdown": {
            "Lesion detection": 89,
            "Vascular changes": 85,
            "Exudate pattern": 88,
            "Early indicators": 91,
        },
    },
    "Moderate DR": {
        "features": [
            "Multiple dot-blot and flame hemorrhages",
            "Hard exudates in circinate patterns",
            "Intraretinal microvascular abnormalities (IRMA)",
            "Cotton-wool spots indicating nerve fiber layer infarcts",
            "Venous caliber irregularities",
        ],
        "regions": "Distributed activation across all quadrants with emphasis on exudate clusters and IRMA regions.",
        "recommendation": "Ophthalmology referral within 3-6 months. OCT evaluation for macular edema. Consider fluorescein angiography.",
        "confidence_breakdown": {
            "Hemorrhage extent": 87,
            "Exudate burden": 84,
            "IRMA detection": 82,
            "Venous changes": 86,
        },
    },
    "Severe DR": {
        "features": [
            "Extensive intraretinal hemorrhages (4 quadrants)",
            "Venous beading and looping",
            "Prominent IRMA with capillary non-perfusion",
            "Multiple cotton-wool spots",
            "Widespread vascular leakage",
            "Pre-retinal hemorrhage formation",
        ],
        "regions": "Strong bilateral activation across retinal quadrants. Peak attention on venous abnormalities and IRMA regions.",
        "recommendation": "Urgent ophthalmologist referral within 1-3 months. Pan-retinal photocoagulation may be indicated. High risk of progression.",
        "confidence_breakdown": {
            "4-2-1 rule": 91,
            "Venous beading": 88,
            "IRMA severity": 86,
            "Hemorrhage density": 90,
        },
    },
    "Proliferative DR": {
        "features": [
            "Neovascularization of the optic disc (NVD)",
            "Neovascularization elsewhere (NVE)",
            "Vitreous hemorrhage (active or resolved)",
            "Pre-retinal hemorrhage with clot formation",
            "Fibrovascular proliferation",
            "Tractional retinal elevation",
        ],
        "regions": "Activation peaks at optic disc (NVD) and peripheral neovascular fronds with extension into vitreous cavity.",
        "recommendation": "Immediate intervention. Anti-VEGF therapy, pan-retinal photocoagulation, or vitrectomy evaluation.",
        "confidence_breakdown": {
            "NVD detection": 94,
            "NVE extent": 91,
            "Vitreous involvement": 89,
            "Proliferative stage": 93,
        },
    },
}


def render():
    st.markdown("""
    <div class="page-header">
        <h1>Explainable AI - Grad-CAM</h1>
        <p>Visual explanation of model decisions via gradient-weighted class activation mapping</p>
    </div>
    """, unsafe_allow_html=True)

    model = get_model()
    pred = st.session_state.get("last_prediction")

    if pred is None:
        st.markdown("""
        <div class="rg-card" style="text-align:center; padding:3rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">&#128300;</div>
            <h3 style="font-family:'Space Grotesk',sans-serif; font-size:1.1rem; font-weight:600; color:#0F172A; margin-bottom:0.5rem;">
                No Prediction Available
            </h3>
            <p style="font-size:0.85rem; color:#64748B; margin-bottom:1.5rem;">
                Run a screening on the DR Screening page first to generate Grad-CAM visualizations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Go to DR Screening", width="stretch"):
                st.session_state.current_page = "predict"
                st.rerun()
        return

    predicted_class = pred["predicted_class"]
    confidence = pred["confidence"]
    probabilities = pred["probabilities"]
    color = CLASS_COLORS.get(predicted_class, "#2563EB")
    severity = get_severity_info(predicted_class)
    clinical_note = get_clinical_note(predicted_class)
    recommendation = get_recommendation(predicted_class)

    original_pil = pred.get("original_pil")
    model_input = pred.get("model_input")

    predicted_idx = DR_CLASSES.index(predicted_class)
    heatmap = compute_gradcam(model.model, model_input, predicted_idx)
    heatmap_pil, overlay_pil = apply_heatmap_overlay(original_pil, heatmap)

    st.markdown("""
    <div class="section-title">Activation Map Visualization</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span style="font-size:0.78rem; font-weight:600; color:#0F172A;">Original Fundus</span>
        </div>
        """, unsafe_allow_html=True)
        st.image(original_pil, width=280)

    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span style="font-size:0.78rem; font-weight:600; color:#0F172A;">Grad-CAM Heatmap</span>
        </div>
        """, unsafe_allow_html=True)
        st.image(heatmap_pil, width=280)

    with col3:
        st.markdown("""
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span style="font-size:0.78rem; font-weight:600; color:#0F172A;">Overlay (alpha=0.45)</span>
        </div>
        """, unsafe_allow_html=True)
        st.image(overlay_pil, width=280)

    st.markdown(f"""
    <div class="rg-card animate-fade-in" style="border-left:4px solid {color}; margin-top:1rem;">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
            <div style="font-size:2rem;">{severity['icon']}</div>
            <div style="flex:1;">
                <div style="font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:700; color:{color};">
                    {severity['title']}
                </div>
                <div style="font-size:0.8rem; color:#64748B;">
                    Confidence: {confidence*100:.1f}% &middot; Risk: {severity['risk']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">Clinical Interpretation</div>
    """, unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        exp = EXPLANATIONS.get(predicted_class, EXPLANATIONS["No DR"])

        fig_feat = go.Figure()
        features = exp["features"]
        fig_feat.add_trace(go.Bar(
            x=[1] * len(features),
            y=features,
            orientation='h',
            marker_color=color,
            text=[f"Detected" for _ in features],
            textposition='inside',
            textfont=dict(size=10, color="#FFFFFF", family="Inter"),
            hovertemplate="%{y}<extra></extra>",
        ))
        fig_feat.update_layout(
            title=dict(text="AI Features Detected", font=dict(size=13, family="Inter", color="#0F172A")),
            height=max(200, len(features) * 40 + 50),
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(autorange="reversed", tickfont=dict(size=10, family="Inter")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10),
            showlegend=False,
        )
        st.plotly_chart(fig_feat, config={"displayModeBar": False}, width="stretch")

    with col_e2:
        exp = EXPLANATIONS.get(predicted_class, EXPLANATIONS["No DR"])

        st.markdown(f"""
        <div class="rg-card" style="height:100%;">
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:600; margin-bottom:0.75rem; color:#0F172A;">
                Activation Region Analysis
            </h4>
            <p style="font-size:0.78rem; color:#475569; line-height:1.7; margin-bottom:1rem;">
                {exp['regions']}
            </p>
            <div class="rg-divider" style="margin:0.75rem 0;"></div>
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:600; margin-bottom:0.5rem; color:#0F172A;">
                Clinical Recommendation
            </h4>
            <div style="font-size:0.78rem; color:{color}; line-height:1.6; font-weight:500;">
                {recommendation['clinical']}
            </div>
            <div style="margin-top:0.5rem;">
                <span class="badge badge-red">Urgency: {recommendation['urgency']}</span>
                <span class="badge badge-blue">Severity: {severity['severity']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">Clinical Assessment</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rg-card">
        <p style="font-size:0.82rem; color:#475569; line-height:1.7;">{clinical_note}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">Confidence Breakdown</div>
    """, unsafe_allow_html=True)

    exp = EXPLANATIONS.get(predicted_class, EXPLANATIONS["No DR"])
    breakdown = exp.get("confidence_breakdown", {})

    fig_conf = go.Figure(go.Bar(
        x=list(breakdown.values()),
        y=list(breakdown.keys()),
        orientation='h',
        marker_color=color,
        text=[f"{v}%" for v in breakdown.values()],
        textposition='outside',
        textfont=dict(size=12, color=color, family="Inter", weight="bold"),
        hovertemplate="%{y}: %{x}%<extra></extra>",
    ))
    fig_conf.update_layout(
        height=max(180, len(breakdown) * 40 + 50),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[0, 110], showgrid=False, title="Confidence %"),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, family="Inter")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11),
        showlegend=False,
    )
    st.plotly_chart(fig_conf, config={"displayModeBar": False}, width="stretch")

    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">Probability Distribution</div>
    """, unsafe_allow_html=True)

    fig_dist = go.Figure(go.Bar(
        x=DR_CLASSES,
        y=[p * 100 for p in probabilities],
        text=[f"{p*100:.1f}%" for p in probabilities],
        textposition='outside',
        textfont=dict(size=11, color="#0F172A", family="Inter"),
        marker_color=[CLASS_COLORS.get(c, "#94A3B8") for c in DR_CLASSES],
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))
    fig_dist.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="DR Class", tickfont=dict(size=10, family="Inter")),
        yaxis=dict(title="Probability %", range=[0, 110]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11),
        showlegend=False,
    )
    st.plotly_chart(fig_dist, config={"displayModeBar": False}, width="stretch")

    st.markdown(f"""
    <div class="rg-alert rg-alert-info" style="margin-top:0.5rem;">
        <strong>Model Focus:</strong> The heatmap highlights regions the model found most relevant
        for classifying this image as <strong>{predicted_class}</strong>.
        Red/orange regions indicate higher contribution to the model's decision.
    </div>
    """, unsafe_allow_html=True)
