import streamlit as st
import numpy as np
from PIL import Image
import io
import time
import plotly.graph_objects as go

from utils.preprocessing import (
    preprocess_image, check_image_quality, get_image_stats, DR_CLASSES
)
from utils.database import save_prediction
from utils.report_generator import generate_pdf_report
from utils.clinical import (
    generate_patient_data, get_severity_info,
    get_clinical_note, get_recommendation
)
from models.model import get_model, CLASS_COLORS


def render():
    st.markdown("""
    <div class="page-header">
        <h1>DR Screening</h1>
        <p>Upload a retinal fundus image for AI-powered diabetic retinopathy analysis</p>
    </div>
    """, unsafe_allow_html=True)

    model = get_model()

    st.markdown('<div class="section-title">Image Upload</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Retinal Fundus Image",
        type=["jpg", "jpeg", "png", "bmp", "tiff", "tif"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.markdown("""
        <div class="upload-zone">
            <div style="font-size:3rem; margin-bottom:0.75rem;">&#128444;</div>
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:600; color:#0F172A; margin-bottom:0.3rem;">
                Select a retinal fundus image
            </h4>
            <p style="font-size:0.78rem; color:#64748B;">
                Supported formats: JPG, PNG, BMP, TIFF
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    pil_image = Image.open(uploaded_file).convert("RGB")
    img_stats = get_image_stats(pil_image)
    quality = check_image_quality(pil_image)
    display_pil, model_input = preprocess_image(pil_image)

    col_img1, col_img2 = st.columns(2)

    with col_img1:
        st.markdown('<div class="section-title">Original Image</div>', unsafe_allow_html=True)
        st.image(pil_image, caption="Uploaded Fundus", width=350)
        st.markdown(f"""
        <div style="display:flex; gap:12px; margin-top:0.5rem; font-size:0.72rem; color:#64748B; flex-wrap:wrap;">
            <span>{img_stats['width']} x {img_stats['height']}px</span>
            <span>{img_stats['mode']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_img2:
        st.markdown('<div class="section-title">Quality Assessment</div>', unsafe_allow_html=True)
        q_score = quality["quality_score"]
        q_color = quality["quality_color"]
        blur = quality["blur_score"]
        brightness = quality["brightness"]
        contrast = quality["contrast"]
        issues = quality["issues"]

        st.markdown(f"""
        <div class="rg-card">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:0.75rem;">
                <span class="status-dot" style="background:{q_color};"></span>
                <span style="font-weight:600; font-size:0.88rem; color:{q_color};">{q_score}</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div>
                    <div style="font-size:0.65rem; color:#94A3B8; text-transform:uppercase;">Sharpness</div>
                    <div style="font-size:0.85rem; font-weight:600; color:#0F172A;">{blur}</div>
                </div>
                <div>
                    <div style="font-size:0.65rem; color:#94A3B8; text-transform:uppercase;">Brightness</div>
                    <div style="font-size:0.85rem; font-weight:600; color:#0F172A;">{brightness:.0f}</div>
                </div>
                <div>
                    <div style="font-size:0.65rem; color:#94A3B8; text-transform:uppercase;">Contrast</div>
                    <div style="font-size:0.85rem; font-weight:600; color:#0F172A;">{contrast:.0f}</div>
                </div>
                <div>
                    <div style="font-size:0.65rem; color:#94A3B8; text-transform:uppercase;">Issues</div>
                    <div style="font-size:0.78rem; font-weight:500; color:#EF4444;">{', '.join(issues) if issues else 'None'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-top:0.5rem; flex-wrap:wrap;">
            <span class="badge badge-blue">Preprocessed: 224x224</span>
            <span class="badge badge-cyan">CLAHE Enhanced</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">AI Analysis</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="analysis-btn-wrapper">', unsafe_allow_html=True)
    clicked = st.button("▶  Run Analysis", key="run_prediction", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <script>
    (function() {
        var t = setInterval(function() {
            var btns = document.querySelectorAll('button');
            for (var i = 0; i < btns.length; i++) {
                if (btns[i].textContent.indexOf('Run Analysis') !== -1) {
                    btns[i].style.cssText = 'background: linear-gradient(135deg, #3B82F6, #06B6D4, #8B5CF6, #3B82F6) !important; background-size: 300% 300% !important; animation: gradient-shift 4s ease infinite !important; color: #FFFFFF !important; font-weight: 700 !important; border: none !important; border-radius: 12px !important; box-shadow: 0 4px 24px rgba(59,130,246,0.35) !important; padding: 0.75rem 1.5rem !important; font-size: 1rem !important; letter-spacing: 0.02em !important;';
                    clearInterval(t);
                }
            }
        }, 50);
    })();
    </script>
    """, unsafe_allow_html=True)

    if clicked:
        with st.spinner(""):
            progress_placeholder = st.empty()
            for label, pct in [
                ("Preprocessing & quality assessment...", 20),
                ("Loading model weights...", 40),
                ("Running inference...", 65),
                ("Generating clinical summary...", 85),
                ("Finalizing report...", 100),
            ]:
                time.sleep(0.25)
                progress_placeholder.markdown(f"""
                <div style="margin:1rem 0;">
                    <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:0.4rem;">
                        <span style="color:#64748B;">{label}</span>
                        <span style="color:#2563EB; font-weight:600;">{pct}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width:{pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            predicted_class, confidence, probabilities = model.predict(model_input)
            progress_placeholder.empty()

        patient_data = generate_patient_data()
        severity_info = get_severity_info(predicted_class)
        clinical_note = get_clinical_note(predicted_class)
        recommendation = get_recommendation(predicted_class)

        severity = severity_info

        st.session_state.last_prediction = {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "probabilities": probabilities,
            "filename": uploaded_file.name,
            "quality": quality,
            "patient_data": patient_data,
            "severity_info": severity_info,
            "clinical_note": clinical_note,
            "recommendation": recommendation,
            "model_input": model_input,
            "display_pil": display_pil,
            "original_pil": pil_image,
        }

        try:
            save_prediction(
                filename=uploaded_file.name,
                predicted_class=predicted_class,
                confidence=confidence,
                probabilities=probabilities,
                patient_data=patient_data,
                severity_info=severity_info,
                clinical_note=clinical_note,
                recommendation=recommendation.get("clinical", ""),
                quality_info=quality,
            )
        except Exception:
            pass

        st.rerun()

    pred = st.session_state.get("last_prediction")
    if pred is None:
        return

    predicted_class = pred["predicted_class"]
    confidence = pred["confidence"]
    probabilities = pred["probabilities"]
    quality = pred["quality"]
    patient_data = pred["patient_data"]
    severity = pred["severity_info"]
    clinical_note = pred["clinical_note"]
    recommendation = pred["recommendation"]
    color = CLASS_COLORS.get(predicted_class, "#2563EB")

    st.markdown(f"""
    <div class="prediction-card animate-fade-in" style="border-left: 4px solid {color}; margin-top:1rem;">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
            <div style="font-size:2rem;">{severity['icon']}</div>
            <div style="flex:1;">
                <div class="prediction-class" style="color:{color};">{severity['title']}</div>
                <div class="prediction-confidence" style="color:{color};">
                    {confidence*100:.1f}% confidence
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.65rem; color:#94A3B8; text-transform:uppercase;">Severity</div>
                <div style="font-size:0.9rem; font-weight:700; color:{color};">{severity['severity']}</div>
                <div style="font-size:0.72rem; color:{color};">Risk: {severity['risk']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Clinical Summary", "Probabilities", "Report"])

    with tab1:
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("""
            <div class="rg-card">
                <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:600; margin-bottom:0.75rem; color:#0F172A;">Patient Information</h4>
            """, unsafe_allow_html=True)
            for k, v in [
                ("Patient ID", patient_data["patient_id"]),
                ("Age", str(patient_data["age"])),
                ("Gender", patient_data["gender"]),
                ("Scan Date", patient_data["scan_date"]),
                ("Examination", patient_data["exam_number"]),
            ]:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:0.3rem 0; border-bottom:1px solid #F1F5F9; font-size:0.78rem;">
                    <span style="color:#64748B;">{k}</span>
                    <span style="color:#0F172A; font-weight:500;">{v}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_p2:
            st.markdown(f"""
            <div class="rg-card">
                <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:600; margin-bottom:0.75rem; color:#0F172A;">Clinical Assessment</h4>
                <p style="font-size:0.78rem; color:#475569; line-height:1.7;">{clinical_note}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rg-alert rg-alert-info" style="margin-top:0.5rem;">
            <strong>Follow-up:</strong> {severity['follow_up']}
        </div>
        """, unsafe_allow_html=True)

        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            st.markdown(f"""
            <div class="rg-card" style="border-left:3px solid {color};">
                <h4 style="font-size:0.8rem; font-weight:600; color:#0F172A; margin-bottom:0.4rem;">Patient Recommendation</h4>
                <p style="font-size:0.75rem; color:#475569; line-height:1.6;">{recommendation['patient']}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_rec2:
            st.markdown(f"""
            <div class="rg-card" style="border-left:3px solid {color};">
                <h4 style="font-size:0.8rem; font-weight:600; color:#0F172A; margin-bottom:0.4rem;">Clinical Recommendation</h4>
                <p style="font-size:0.75rem; color:#475569; line-height:1.6;">{recommendation['clinical']}</p>
                <div style="margin-top:0.5rem;">
                    <span class="badge badge-red">Urgency: {recommendation['urgency']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">Class Probabilities</div>', unsafe_allow_html=True)

        for cls_name, prob in zip(DR_CLASSES, probabilities):
            c = CLASS_COLORS[cls_name]
            is_predicted = cls_name == predicted_class
            bar_pct = prob * 100

            fig = go.Figure(go.Bar(
                x=[prob * 100],
                y=[cls_name],
                orientation='h',
                marker_color=c,
                text=[f"{prob*100:.1f}%"],
                textposition='outside',
                textfont=dict(size=12, color=c, family="Inter", weight="bold"),
                hovertemplate=f"{cls_name}: %{{x:.1f}}%<extra></extra>",
            ))
            fig.update_layout(
                height=45,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(range=[0, 105], showgrid=False, showticklabels=False),
                yaxis=dict(showticklabels=False),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11),
                showlegend=False,
            )
            st.plotly_chart(fig, config={"displayModeBar": False}, width="stretch")

            if is_predicted:
                st.markdown(f"""
                <div style="margin-top:-0.5rem; margin-bottom:0.5rem; padding:0.2rem 0.5rem;
                    background:{c}10; border:1px solid {c}30; border-radius:6px;
                    font-size:0.7rem; color:{c}; font-weight:600; display:inline-block;">
                    Predicted Class
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div class="rg-divider"></div>
        <div class="section-title">Processed Image</div>
        """, unsafe_allow_html=True)

        st.image(pred["display_pil"], caption="Preprocessed (224x224, CLAHE)", width=300)

    with tab3:
        st.markdown('<div class="section-title">Screening Report</div>', unsafe_allow_html=True)

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("Generate PDF Report", key="gen_pdf", width="stretch"):
                with st.spinner("Generating report..."):
                    pdf_bytes = generate_pdf_report(
                        filename=uploaded_file.name,
                        predicted_class=predicted_class,
                        confidence=confidence,
                        probabilities=probabilities,
                        quality_info=quality,
                        patient_data=patient_data,
                        clinical_note=clinical_note,
                        recommendation=recommendation.get("clinical", ""),
                    )
                    st.session_state["pdf_bytes"] = pdf_bytes
                    st.session_state["pdf_ready"] = True
                    st.rerun()

        with col_r2:
            if st.session_state.get("pdf_ready"):
                pdf_bytes = st.session_state.get("pdf_bytes")
                st.download_button(
                    "Download Report",
                    data=pdf_bytes,
                    file_name=f"report_{patient_data['patient_id']}_{predicted_class.replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    width="stretch",
                )

        st.markdown(f"""
        <div class="rg-card" style="margin-top:0.5rem;">
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:600; margin-bottom:0.5rem; color:#0F172A;">Report Summary</h4>
        """, unsafe_allow_html=True)
        for k, v in [
            ("Patient", f"{patient_data['patient_id']} | {patient_data['age']}y/{patient_data['gender']}"),
            ("Diagnosis", predicted_class),
            ("Confidence", f"{confidence*100:.1f}%"),
            ("Severity", severity["severity"]),
            ("Risk", severity["risk"]),
            ("Urgency", recommendation["urgency"]),
            ("Model", "CNN + ViT Hybrid"),
        ]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.25rem 0; border-bottom:1px solid #F1F5F9; font-size:0.78rem;">
                <span style="color:#64748B;">{k}</span>
                <span style="color:#0F172A; font-weight:500;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="rg-divider"></div>', unsafe_allow_html=True)
    if st.button("New Screening", key="new_prediction", width="stretch"):
        for key in ["last_prediction", "pdf_bytes", "pdf_ready"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
