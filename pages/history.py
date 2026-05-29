import streamlit as st
import pandas as pd
import io
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from utils.database import (
    get_all_predictions, delete_prediction,
    clear_all_predictions, get_stats
)
from utils.report_generator import generate_pdf_report
from utils.clinical import DR_CLASSES

CLASS_COLORS = {
    "No DR":            "#10B981",
    "Mild DR":          "#F59E0B",
    "Moderate DR":      "#F97316",
    "Severe DR":        "#EF4444",
    "Proliferative DR": "#A855F7",
}

RISK_MAP = {
    "No DR":            "Low",
    "Mild DR":          "Low-Moderate",
    "Moderate DR":      "Moderate",
    "Severe DR":        "High",
    "Proliferative DR": "Critical",
}


def render():
    st.markdown("""
    <div class="page-header">
        <h1>📋 Screening History</h1>
        <p>Complete record of all screening examinations with export capabilities</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_predictions()
    stats = get_stats()

    # ── Summary Stats ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#2563EB;">{stats["total"]}</div>
            <div class="metric-label">Total Screenings</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#10B981;">{stats.get("class_counts", {}).get("No DR", 0)}</div>
            <div class="metric-label">Normal (No DR)</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        dr_count = sum(v for k, v in stats.get("class_counts", {}).items() if k != "No DR")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F97316;">{dr_count}</div>
            <div class="metric-label">DR Detected</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_conf = stats.get("avg_confidence", 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#8B5CF6;">{avg_conf*100:.1f}%</div>
            <div class="metric-label">Avg. Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Distribution Chart ────────────────────────────────────────────────────
    if stats["total"] > 0 and stats.get("class_counts"):
        col_ch1, col_ch2 = st.columns([2, 1])
        with col_ch1:
            dist_df = pd.DataFrame({
                "Class": list(stats["class_counts"].keys()),
                "Count": list(stats["class_counts"].values()),
            }).sort_values("Count", ascending=False)
            colors_list = [CLASS_COLORS.get(c, "#94A3B8") for c in dist_df["Class"]]
            fig = go.Figure(data=[go.Bar(
                x=dist_df["Class"],
                y=dist_df["Count"],
                text=dist_df["Count"],
                textposition="outside",
                textfont=dict(size=11, color="#0F172A", family="Inter"),
                marker_color=colors_list,
                width=0.5,
                hovertemplate="%{x}: %{y} screenings<extra></extra>",
            )])
            fig.update_layout(
                title=dict(text="Screening Distribution", font=dict(size=13, family="Inter", color="#0F172A")),
                height=280,
                margin=dict(l=10, r=10, t=35, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11),
                yaxis=dict(title="Count"),
                showlegend=False,
            )
            st.plotly_chart(fig, config={"displayModeBar": False}, width="stretch")

        with col_ch2:
            st.markdown('<div class="section-title" style="font-size:0.9rem;">Quick Actions</div>', unsafe_allow_html=True)
            st.markdown('<div class="rg-card">', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:0.78rem; color:#64748B;">Export all records as CSV or clear the database.</p>', unsafe_allow_html=True)

            if not df.empty:
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    "Export CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"dr_grading_screenings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    width="stretch",
                )

            if stats["total"] > 0:
                if st.button("Clear All Records", key="clear_all", width="stretch"):
                    clear_all_predictions()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Records ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">📋 Screening Records</div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
        <div class="rg-card" style="text-align:center; padding:2rem;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">📭</div>
            <h4 style="font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:600; color:#64748B;">No Screenings Yet</h4>
            <p style="font-size:0.8rem; color:#94A3B8;">Upload a retinal fundus image on the DR Screening page to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for idx, row in df.iterrows():
        rec_id = row.get("id", idx)
        timestamp = row.get("timestamp", "")
        cls = row.get("predicted_class", "Unknown")
        conf = row.get("confidence", 0)
        color = CLASS_COLORS.get(cls, "#64748B")
        risk = row.get("risk", RISK_MAP.get(cls, ""))
        severity_label = row.get("severity", "")
        filename = row.get("filename", "")
        patient_id = row.get("patient_id", "N/A")
        age = row.get("age", "")
        gender = row.get("gender", "")
        exam = row.get("exam_number", "")

        try:
            ts_formatted = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")
        except Exception:
            ts_formatted = str(timestamp)[:16]

        st.markdown(f"""
        <div class="rg-card" style="margin-bottom:0.6rem; padding:1rem 1.25rem;">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <div style="width:4px; height:40px; border-radius:2px; background:{color}; flex-shrink:0;"></div>
                <div style="flex:1; min-width:150px;">
                    <div style="font-weight:600; font-size:0.88rem; color:{color};">{cls}</div>
                    <div style="font-size:0.7rem; color:#94A3B8;">
                        {ts_formatted} &middot; {patient_id} &middot; {age}y {gender}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.78rem; font-weight:600; color:{color};">{conf*100:.1f}%</div>
                    <div style="font-size:0.65rem; color:#64748B;">Confidence</div>
                </div>
                <div style="text-align:right;">
                    <span class="badge" style="background:{color}15; color:{color}; border:1px solid {color}30;">
                        {risk}
                    </span>
                </div>
                <div style="display:flex; gap:6px; flex-shrink:0;">
        """, unsafe_allow_html=True)

        col_acts = st.columns([1, 1])
        with col_acts[0]:
            probs_list = [
                row.get("no_dr", 0), row.get("mild", 0),
                row.get("moderate", 0), row.get("severe", 0), row.get("proliferative", 0)
            ]
            quality_info = {
                "quality_score": row.get("quality_score", "N/A"),
                "brightness": row.get("brightness", 0),
                "contrast": row.get("contrast", 0),
                "blur_score": row.get("blur_score", 0),
                "issues": [],
            }
            pdf_bytes = generate_pdf_report(
                filename=filename,
                predicted_class=cls,
                confidence=conf,
                probabilities=probs_list,
                quality_info=quality_info,
                patient_data={
                    "patient_id": patient_id,
                    "age": age,
                    "gender": gender,
                    "scan_date": ts_formatted,
                    "exam_number": exam,
                },
                clinical_note=row.get("clinical_note", ""),
                recommendation=row.get("recommendation", ""),
            )
            st.download_button(
                "PDF",
                data=pdf_bytes,
                file_name=f"report_{rec_id}_{cls.replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
                width="stretch",
                key=f"dl_{rec_id}",
            )

        with col_acts[1]:
            if st.button("Delete", key=f"del_{rec_id}", width="stretch"):
                delete_prediction(rec_id)
                st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

        notes = row.get("clinical_note", "")
        if notes:
            st.markdown(f"""
            <div style="font-size:0.72rem; color:#64748B; padding:0.25rem 1.25rem 0.5rem; margin-top:-0.3rem;">
                📝 {notes[:120]}{'...' if len(notes) > 120 else ''}
            </div>
            """, unsafe_allow_html=True)
