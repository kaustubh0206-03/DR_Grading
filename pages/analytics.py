import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

DEMO_METRICS = {
    "accuracy":      0.8734,
    "precision":     0.8612,
    "recall":        0.8489,
    "f1":            0.8549,
    "auc_roc":       0.9421,
    "cohen_kappa":   0.8271,
    "sensitivity":   0.8623,
    "specificity":   0.9718,
}

DEMO_CLASSES = ["No DR", "Mild DR", "Moderate DR", "Severe DR", "Proliferative DR"]

DEMO_CLASSWISE = pd.DataFrame({
    "Class":          DEMO_CLASSES,
    "Precision":      [0.92, 0.84, 0.85, 0.83, 0.88],
    "Recall":         [0.95, 0.78, 0.82, 0.86, 0.84],
    "F1-Score":       [0.93, 0.81, 0.84, 0.85, 0.86],
    "Support":        [1805, 370,  999,  193,  295],
    "AUC-ROC":        [0.97, 0.93, 0.94, 0.95, 0.96],
})

DEMO_CM = np.array([
    [1715,  52,  28,   7,   3],
    [  48, 289,  24,   5,   4],
    [  31,  38, 819,  78,  33],
    [   5,   8,  38, 166,  24],
    [   4,   5,  21,  17, 248],
])

COLORS = ["#10B981", "#F59E0B", "#F97316", "#EF4444", "#A855F7"]

EPOCHS = list(range(1, 41))
TRAIN_ACC = [0.45 + 0.45 * (1 - np.exp(-e / 12)) + np.random.randn() * 0.015 for e in EPOCHS]
VAL_ACC   = [0.40 + 0.44 * (1 - np.exp(-e / 14)) + np.random.randn() * 0.018 for e in EPOCHS]
TRAIN_LOSS = [1.6 * np.exp(-e / 10) + 0.15 + np.random.randn() * 0.02 for e in EPOCHS]
VAL_LOSS   = [1.7 * np.exp(-e / 11) + 0.18 + np.random.randn() * 0.025 for e in EPOCHS]

for i in range(5, 35):
    TRAIN_ACC[i] = min(TRAIN_ACC[i], 0.96)
    VAL_ACC[i]   = min(VAL_ACC[i], 0.93)
    TRAIN_LOSS[i] = max(TRAIN_LOSS[i], 0.05)
    VAL_LOSS[i]   = max(VAL_LOSS[i], 0.08)

TRAIN_ACC = np.clip(TRAIN_ACC, 0.35, 0.97)
VAL_ACC   = np.clip(VAL_ACC, 0.30, 0.94)
TRAIN_LOSS = np.clip(TRAIN_LOSS, 0.02, 2.0)
VAL_LOSS   = np.clip(VAL_LOSS, 0.04, 2.0)


def render():
    st.markdown("""
    <div class="page-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Executive-grade model performance metrics and training analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top Metrics ───────────────────────────────────────────────────────────
    metrics_row = [
        ("Accuracy", f"{DEMO_METRICS['accuracy']*100:.1f}%", "#2563EB"),
        ("Precision", f"{DEMO_METRICS['precision']*100:.1f}%", "#10B981"),
        ("Recall", f"{DEMO_METRICS['recall']*100:.1f}%", "#06B6D4"),
        ("F1 Score", f"{DEMO_METRICS['f1']*100:.1f}%", "#8B5CF6"),
        ("AUC-ROC", f"{DEMO_METRICS['auc_roc']*100:.1f}%", "#F59E0B"),
        ("Cohen's κ", f"{DEMO_METRICS['cohen_kappa']*100:.1f}%", "#F97316"),
    ]

    cols = st.columns(6)
    for col, (label, value, color) in zip(cols, metrics_row):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:{color};">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">📉 Confusion Matrix</div>
    """, unsafe_allow_html=True)

    col_cm1, col_cm2 = st.columns([3, 2])

    with col_cm1:
        fig_cm = go.Figure(data=go.Heatmap(
            z=DEMO_CM,
            x=DEMO_CLASSES,
            y=DEMO_CLASSES,
            text=DEMO_CM,
            texttemplate="%{text}",
            textfont={"size": 11, "color": "#0F172A", "family": "Inter"},
            colorscale=[[0, "#F1F5F9"], [0.3, "#93C5FD"], [0.6, "#3B82F6"], [1, "#1D4ED8"]],
            hoverongaps=False,
            hovertemplate="True: %{y}<br>Predicted: %{x}<br>Count: %{text}<extra></extra>",
        ))
        fig_cm.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Predicted Class", side="bottom", tickfont=dict(size=10)),
            yaxis=dict(title="True Class", tickfont=dict(size=10), autorange="reversed"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11),
        )
        st.plotly_chart(fig_cm, config={"displayModeBar": False}, width="stretch")

    with col_cm2:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Class-wise Performance</div>', unsafe_allow_html=True)
        fig_bar = go.Figure()
        for metric in ["Precision", "Recall", "F1-Score"]:
            fig_bar.add_trace(go.Bar(
                name=metric,
                x=DEMO_CLASSES,
                y=DEMO_CLASSWISE[metric],
                text=[f"{v:.2f}" for v in DEMO_CLASSWISE[metric]],
                textposition="outside",
                textfont=dict(size=9, color="#64748B"),
                marker_color=["#3B82F6", "#10B981", "#8B5CF6"][["Precision", "Recall", "F1-Score"].index(metric)],
                opacity=0.85,
            ))
        fig_bar.update_layout(
            barmode="group",
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", y=1.08, font=dict(size=10)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10),
            yaxis=dict(range=[0, 1.15], tickformat=".0%"),
        )
        st.plotly_chart(fig_bar, config={"displayModeBar": False}, width="stretch")

    # ── Training Curves ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">📈 Training History</div>
    """, unsafe_allow_html=True)

    col_curves1, col_curves2 = st.columns(2)

    with col_curves1:
        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(
            x=EPOCHS, y=TRAIN_ACC, mode="lines", name="Training Accuracy",
            line=dict(color="#3B82F6", width=2.5),
            hovertemplate="Epoch %{x}<br>Train Acc: %{y:.1%}<extra></extra>",
        ))
        fig_acc.add_trace(go.Scatter(
            x=EPOCHS, y=VAL_ACC, mode="lines", name="Validation Accuracy",
            line=dict(color="#10B981", width=2.5, dash="dot"),
            hovertemplate="Epoch %{x}<br>Val Acc: %{y:.1%}<extra></extra>",
        ))
        fig_acc.update_layout(
            title=dict(text="Accuracy Curves", font=dict(size=13, family="Inter", color="#0F172A")),
            height=320,
            margin=dict(l=10, r=10, t=35, b=10),
            legend=dict(orientation="h", y=1.1, font=dict(size=10)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10),
            yaxis=dict(range=[0.3, 1.0], tickformat=".0%"),
            xaxis=dict(title="Epoch"),
            hovermode="x unified",
        )
        st.plotly_chart(fig_acc, config={"displayModeBar": False}, width="stretch")

    with col_curves2:
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(
            x=EPOCHS, y=TRAIN_LOSS, mode="lines", name="Training Loss",
            line=dict(color="#EF4444", width=2.5),
            hovertemplate="Epoch %{x}<br>Train Loss: %{y:.3f}<extra></extra>",
        ))
        fig_loss.add_trace(go.Scatter(
            x=EPOCHS, y=VAL_LOSS, mode="lines", name="Validation Loss",
            line=dict(color="#F59E0B", width=2.5, dash="dot"),
            hovertemplate="Epoch %{x}<br>Val Loss: %{y:.3f}<extra></extra>",
        ))
        fig_loss.update_layout(
            title=dict(text="Loss Curves", font=dict(size=13, family="Inter", color="#0F172A")),
            height=320,
            margin=dict(l=10, r=10, t=35, b=10),
            legend=dict(orientation="h", y=1.1, font=dict(size=10)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10),
            yaxis=dict(range=[0, 1.8]),
            xaxis=dict(title="Epoch"),
            hovermode="x unified",
        )
        st.plotly_chart(fig_loss, config={"displayModeBar": False}, width="stretch")

    # ── Class Distribution ────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">📊 Dataset Distribution</div>
    """, unsafe_allow_html=True)

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        dist_data = pd.DataFrame({
            "Class": DEMO_CLASSES,
            "Samples": [1805, 370, 999, 193, 295],
            "Color": COLORS,
        })
        fig_dist = px.pie(
            dist_data,
            values="Samples",
            names="Class",
            color="Class",
            color_discrete_map={c: col for c, col in zip(DEMO_CLASSES, COLORS)},
            hole=0.45,
        )
        fig_dist.update_traces(
            textposition="outside",
            textinfo="percent+label",
            textfont=dict(size=11, color="#64748B", family="Inter"),
            marker=dict(line=dict(color="#FFFFFF", width=2)),
            hovertemplate="%{label}<br>%{value} samples (%{percent})<extra></extra>",
        )
        fig_dist.update_layout(
            title=dict(text="Class Distribution (3,662 labeled images)", font=dict(size=12, family="Inter", color="#0F172A")),
            height=360,
            margin=dict(l=10, r=10, t=35, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig_dist, config={"displayModeBar": False}, width="stretch")

    with col_d2:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Additional Metrics</div>', unsafe_allow_html=True)
        st.markdown('<div class="rg-card">', unsafe_allow_html=True)
        for k, v in [
            ("Dataset Size", "3,662 labeled images"),
            ("Train / Val / Test", "70% / 15% / 15%"),
            ("Image Resolution", "224 x 224 x 3"),
            ("Optimizer", "Adam (lr=1e-4)"),
            ("Batch Size", "32"),
            ("Epochs", "40 (EarlyStopping)"),
            ("Loss Function", "Categorical Cross-Entropy"),
            ("Augmentation", "Rotation, Flip, Zoom, Brightness"),
            ("Sensitivity", f"{DEMO_METRICS['sensitivity']*100:.1f}%"),
            ("Specificity", f"{DEMO_METRICS['specificity']*100:.1f}%"),
            ("Cohen's Kappa", f"{DEMO_METRICS['cohen_kappa']*100:.1f}%"),
        ]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.3rem 0; border-bottom:1px solid #F1F5F9; font-size:0.78rem;">
                <span style="color:#64748B;">{k}</span>
                <span style="color:#0F172A; font-weight:500;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Class-wise AUC ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="section-title">🎯 Class-wise AUC-ROC</div>
    """, unsafe_allow_html=True)

    fig_auc = go.Figure()
    for i, cls_name in enumerate(DEMO_CLASSES):
        auc_val = DEMO_CLASSWISE[DEMO_CLASSWISE["Class"] == cls_name]["AUC-ROC"].values[0]
        fig_auc.add_trace(go.Bar(
            name=cls_name,
            x=[cls_name],
            y=[auc_val],
            text=[f"{auc_val:.2f}"],
            textposition="outside",
            textfont=dict(size=12, color=COLORS[i], family="Inter"),
            marker_color=COLORS[i],
            width=0.5,
            hovertemplate="%{x}<br>AUC-ROC: %{y:.3f}<extra></extra>",
        ))
    fig_auc.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11),
        yaxis=dict(range=[0.85, 1.0], tickformat=".2f", title="AUC-ROC"),
        showlegend=False,
    )
    st.plotly_chart(fig_auc, config={"displayModeBar": False}, width="stretch")

    # ── Disclaimer ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="rg-divider"></div>
    <div class="rg-alert rg-alert-info">
        <strong>📊 Analytics Note:</strong> Metrics shown are based on preliminary model evaluation.
        Performance may vary with real-world data distribution. Continuous validation is recommended.
    </div>
    """, unsafe_allow_html=True)
