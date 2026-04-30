"""
Page 5 — Demographic Trends
Performance patterns across student demographic groups (where data is available).
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import auth
from data import ANCHORING_CONCEPTS, get_data
from theme import (
    inject_css, page_header, data_banner, sidebar_about, apply_plotly_theme,
    CC_COLOR, AC_COLOR, FLAG_COLOR, BORDER, TEXT, TEXT_MUTED,
)

# Local accent for "warning" gap (5–10% difference).
WARN_COLOR = "#FFBF47"

st.set_page_config(page_title="Demographic Trends", page_icon=None, layout="wide")
auth.require_login()
inject_css()

page_header(
    "Demographic trends (illustrative demo only)",
    "Placeholder for future functionality. The numbers below are simulated.",
)

# Prominent demo-data banner. This page is currently a wireframe: every chart
# is filled with randomly generated values. Make that unmistakable so an
# instructor never confuses these bars for their actual cohort.
st.markdown(
    f"""
    <div style="background: rgba(255, 191, 71, 0.12);
                border: 1px solid rgba(255, 191, 71, 0.55);
                border-left: 4px solid #FFBF47;
                border-radius: 8px;
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;">
        <p style="color: #FFBF47; font-weight: 700; font-size: 0.95rem;
                  text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 0.5rem 0;">
            Illustrative demo only
        </p>
        <p style="color: {TEXT}; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            The numbers and groupings on this page are <strong>randomly generated</strong>,
            not your students' actual demographic data. This page is a placeholder for
            future functionality and will activate only when demographic variables are
            collected as part of your course administration and added to your dataset.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Standing equity-and-care note about how demographic data should be interpreted
# even when real. Kept here so the framing is in place when the page goes live.
st.markdown(
    f"""
    <div class="note warn">
        <span class="label">When real data is added</span>
        Differences in group-level performance reflect structural and instructional
        factors, not inherent differences in student ability. The goal of this analysis
        is to identify where instruction may be serving some students less effectively
        than others, not to characterize groups.
    </div>
    """,
    unsafe_allow_html=True,
)

df, is_real = get_data()
data_banner(df, is_real)

# ── Demo demographic data (placeholder until real demographics are wired in) ──
rng = np.random.default_rng(55)
ac_names = list(ANCHORING_CONCEPTS.keys())
ac_short = [k.split(": ")[1] for k in ac_names]

groups = ["First-gen students", "Continuing-gen students"]
group_colors = [AC_COLOR, CC_COLOR]
group_scores = {
    g: [int(rng.integers(35, 85)) for _ in ac_names]
    for g in groups
}

# ── Grouped bar chart ─────────────────────────────────────────────────────────
st.markdown("### Performance by first-generation status")
st.caption(
    "First-generation college student status is one of the most commonly collected "
    "demographic variables in chemistry education research."
)

fig = go.Figure()
for group, color in zip(groups, group_colors):
    fig.add_trace(go.Bar(
        name=group,
        x=ac_short,
        y=group_scores[group],
        marker_color=color,
        text=[f"{v}%" for v in group_scores[group]],
        textposition="outside",
        textfont=dict(color=TEXT),
        hovertemplate=f"<b>%{{x}}</b><br>{group}: %{{y}}%<extra></extra>",
    ))

apply_plotly_theme(fig)
fig.update_layout(
    barmode="group",
    height=350,
    margin=dict(l=0, r=0, t=20, b=60),
    yaxis=dict(range=[0, 110], title="% correct"),
    xaxis=dict(tickangle=-30),
    legend=dict(orientation="h", y=-0.22, x=0.2),
)
st.plotly_chart(fig, use_container_width=True)

# ── Gap analysis ──────────────────────────────────────────────────────────────
st.markdown("### Achievement gap by AC")
gaps = [
    group_scores[groups[1]][i] - group_scores[groups[0]][i]
    for i in range(len(ac_names))
]

fig_gap = go.Figure(go.Bar(
    x=ac_short,
    y=gaps,
    marker_color=[
        FLAG_COLOR if g > 10 else (WARN_COLOR if g > 5 else CC_COLOR)
        for g in gaps
    ],
    text=[f"{g:+d}%" for g in gaps],
    textposition="outside",
    textfont=dict(color=TEXT),
    hovertemplate="<b>%{x}</b><br>Gap (continuing minus first-gen): %{y:+d}%<extra></extra>",
))
fig_gap.add_hline(y=0, line_color=BORDER, line_width=1)
apply_plotly_theme(fig_gap)
fig_gap.update_layout(
    height=280,
    margin=dict(l=0, r=0, t=10, b=60),
    yaxis=dict(title="Score gap (continuing minus first-gen, %)"),
    xaxis=dict(tickangle=-30),
    showlegend=False,
)
st.plotly_chart(fig_gap, use_container_width=True)

# ── Additional demographic variables ─────────────────────────────────────────
st.markdown("### Additional demographic variables")
demo_var = st.selectbox(
    "Select a demographic variable to explore",
    ["Course section", "Year in college", "Prior chemistry coursework", "Intended major"],
)

st.info(
    f"**{demo_var}** analysis requires that this variable was collected during course "
    "administration. Upload your course roster data or connect to your LMS to enable this view."
)

st.markdown(
    f"""
    <div class="card">
        <p style="color:{TEXT}; font-size:0.85rem; line-height:1.6; margin:0;">
            <strong>Note for instructors:</strong> Equity-oriented analysis of assessment data
            is a tool for identifying where instructional structures may be creating
            differential learning outcomes. Rather than viewing group differences as fixed,
            use these data as a prompt to consider:
            <em>what aspects of how I teach, structure my course, or support students outside
            of class may be contributing to these patterns?</em>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_about()
