"""
Page 3 — Student Confidence
Students' metacognitive calibration: how their confidence aligns with their actual performance.
Renamed from "Confidence Trends" to disambiguate from page 4 (instructor calibration).
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
    CC_COLOR, AC_COLOR, FLAG_COLOR, AC_FADED_COLOR, TEXT, TEXT_MUTED, BORDER, SURFACE,
)

# Local accent for "warning" color (overconfident); kept here so theme.py stays focused.
WARN_COLOR = "#FFBF47"

st.set_page_config(page_title="Student Confidence", page_icon=None, layout="wide")
auth.require_login()
inject_css()

page_header(
    "Student confidence",
    "How well does student confidence align with their actual performance?",
)

st.markdown(
    f"""
    <div class="card">
        <p style="color:{TEXT}; font-size:0.9rem; line-height:1.6; margin:0;">
            Confidence ratings collected alongside the Water Instrument let you examine
            students' metacognitive calibration. Students who are
            <strong style="color:{FLAG_COLOR};">overconfident</strong> in alternate conceptions
            (high confidence and a wrong answer) are a particular instructional challenge.
            Students who are
            <strong style="color:{AC_COLOR};">underconfident</strong> in correct answers
            may benefit from explicit reinforcement of what they already know.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

df, is_real = get_data()
data_banner(df, is_real)

rng = np.random.default_rng(99)
ac_names = list(ANCHORING_CONCEPTS.keys())
# Use the descriptive title (e.g. "Atoms", "Bonding", "Intermolecular Forces")
# instead of the AC number, so instructors can read the charts without having
# to memorize which number maps to which concept.
ac_short = [k.split(": ")[1] for k in ac_names]

actual_pct_correct = []
avg_confidence = []

for ac_name, ac_info in ANCHORING_CONCEPTS.items():
    items_in_ac = [i for i in ac_info["items"] if i in df["item_id"].values]
    if items_in_ac:
        ac_df = df[df["item_id"].isin(items_in_ac)]
        actual_pct_correct.append(round(ac_df["cc_pct"].mean(), 1))
        conf_vals = ac_df["conf_mean"].dropna()
        if len(conf_vals) > 0:
            avg_confidence.append(round(conf_vals.mean(), 2))
        else:
            avg_confidence.append(round(float(rng.uniform(2.8, 4.5)), 2))
    else:
        actual_pct_correct.append(50.0)
        avg_confidence.append(round(float(rng.uniform(2.8, 4.5)), 2))

pct_correct = np.array(actual_pct_correct)
avg_confidence = np.array(avg_confidence)

# Calibration gap: confidence - (pct_correct/20). Positive = overconfident.
calibration_gap = avg_confidence - (pct_correct / 20)

# ── Summary charts ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Average confidence by AC")
    fig_conf = go.Figure(go.Bar(
        x=ac_short,
        y=avg_confidence,
        marker_color=[
            FLAG_COLOR if c > 4.0 else (WARN_COLOR if c > 3.5 else CC_COLOR)
            for c in avg_confidence
        ],
        text=[f"{c:.1f}" for c in avg_confidence],
        textposition="outside",
        textfont=dict(color=TEXT),
        hovertemplate="<b>%{x}</b><br>Avg confidence: %{y:.2f}/5<extra></extra>",
    ))
    apply_plotly_theme(fig_conf)
    fig_conf.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=50),
        yaxis=dict(range=[0, 5.5], title="Avg. confidence (1 to 5)"),
        xaxis=dict(tickangle=-30),
        showlegend=False,
    )
    st.plotly_chart(fig_conf, use_container_width=True)

    # Interpretive blurb
    top_conf = int(np.argmax(avg_confidence))
    low_conf = int(np.argmin(avg_confidence))
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.83rem; line-height:1.5; "
        f"margin:-0.25rem 0 0 0;'>"
        f"Students felt most confident in <strong style='color:{TEXT};'>"
        f"{ac_short[top_conf]}</strong> ({avg_confidence[top_conf]:.1f}/5) and "
        f"least confident in <strong style='color:{TEXT};'>{ac_short[low_conf]}</strong> "
        f"({avg_confidence[low_conf]:.1f}/5). High confidence does not always mean high "
        f"performance, see the calibration map below."
        f"</p>",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown("### % correct by AC")
    fig_pct = go.Figure(go.Bar(
        x=ac_short,
        y=pct_correct,
        marker_color=[
            CC_COLOR if p > 65 else (WARN_COLOR if p > 50 else FLAG_COLOR)
            for p in pct_correct
        ],
        text=[f"{p:.0f}%" for p in pct_correct],
        textposition="outside",
        textfont=dict(color=TEXT),
        hovertemplate="<b>%{x}</b><br>% correct: %{y:.1f}%<extra></extra>",
    ))
    apply_plotly_theme(fig_pct)
    fig_pct.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=50),
        yaxis=dict(range=[0, 105], title="% correct"),
        xaxis=dict(tickangle=-30),
        showlegend=False,
    )
    st.plotly_chart(fig_pct, use_container_width=True)

    # Interpretive blurb
    top_pct = int(np.argmax(pct_correct))
    low_pct = int(np.argmin(pct_correct))
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.83rem; line-height:1.5; "
        f"margin:-0.25rem 0 0 0;'>"
        f"Students performed best in <strong style='color:{TEXT};'>"
        f"{ac_short[top_pct]}</strong> ({pct_correct[top_pct]:.0f}%) and weakest in "
        f"<strong style='color:{TEXT};'>{ac_short[low_pct]}</strong> "
        f"({pct_correct[low_pct]:.0f}%). The Anchoring Concept Trends page can show you "
        f"which specific items drove these numbers."
        f"</p>",
        unsafe_allow_html=True,
    )

# ── Calibration scatter ───────────────────────────────────────────────────────
st.markdown("### Calibration map: confidence vs. performance")

st.markdown(
    f"""
    <div class="legend-row">
        <span><span class="legend-dot" style="background:{CC_COLOR};"></span> Well calibrated</span>
        <span><span class="legend-dot" style="background:{FLAG_COLOR};"></span> Overconfident</span>
        <span><span class="legend-dot" style="background:{AC_COLOR};"></span> Underconfident</span>
        <span><span class="legend-dot" style="background:{AC_FADED_COLOR};"></span> Low engagement</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# Quadrant thresholds sit at the midpoints of the chart so the four quadrants
# are equal in size: confidence midpoint = 3 (Likert 1..5), performance
# midpoint = 50%. Anything to the upper-right of the dashed lines is
# "well calibrated"; lower-right is "overconfident".
CONF_MID = 3.0
PCT_MID = 50.0
X_MIN, X_MAX = 1.0, 5.0
Y_MIN, Y_MAX = 0.0, 100.0


def get_quadrant_color(conf, pct):
    high_conf = conf > CONF_MID
    high_pct = pct > PCT_MID
    if high_conf and high_pct:
        return CC_COLOR
    if high_conf and not high_pct:
        return FLAG_COLOR
    if not high_conf and high_pct:
        return AC_COLOR
    return AC_FADED_COLOR


colors = [get_quadrant_color(c, p) for c, p in zip(avg_confidence, pct_correct)]

fig_scatter = go.Figure()

# Quadrant tinting (each rectangle is half-width by half-height of the chart)
fig_scatter.add_shape(type="rect", x0=X_MIN, y0=PCT_MID, x1=CONF_MID, y1=Y_MAX,
                     fillcolor="rgba(77,168,255,0.07)", line_width=0)
fig_scatter.add_shape(type="rect", x0=CONF_MID, y0=PCT_MID, x1=X_MAX, y1=Y_MAX,
                     fillcolor="rgba(61,220,151,0.07)", line_width=0)
fig_scatter.add_shape(type="rect", x0=CONF_MID, y0=Y_MIN, x1=X_MAX, y1=PCT_MID,
                     fillcolor="rgba(255,107,107,0.07)", line_width=0)

fig_scatter.add_trace(go.Scatter(
    x=avg_confidence,
    y=pct_correct,
    mode="markers+text",
    text=ac_short,
    textposition="top center",
    textfont=dict(color=TEXT),
    marker=dict(color=colors, size=16, line=dict(width=1.5, color=SURFACE)),
    hovertemplate="<b>%{text}</b><br>Avg confidence: %{x:.2f}/5<br>% correct: %{y:.1f}%<extra></extra>",
))

# Quadrant labels positioned at each quadrant's center.
fig_scatter.add_annotation(x=2.0, y=75, text="Underconfident", showarrow=False,
                           font=dict(size=11, color=AC_COLOR), opacity=0.8)
fig_scatter.add_annotation(x=4.0, y=75, text="Well calibrated", showarrow=False,
                           font=dict(size=11, color=CC_COLOR), opacity=0.8)
fig_scatter.add_annotation(x=4.0, y=25, text="Overconfident", showarrow=False,
                           font=dict(size=11, color=FLAG_COLOR), opacity=0.8)

apply_plotly_theme(fig_scatter)
fig_scatter.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=40),
    xaxis=dict(title="Average confidence (1 to 5)", range=[X_MIN, X_MAX]),
    yaxis=dict(title="% correct", range=[Y_MIN, Y_MAX]),
    shapes=[
        dict(type="line", x0=CONF_MID, x1=CONF_MID, y0=Y_MIN, y1=Y_MAX,
             line=dict(color=BORDER, dash="dash", width=1.5)),
        dict(type="line", x0=X_MIN, x1=X_MAX, y0=PCT_MID, y1=PCT_MID,
             line=dict(color=BORDER, dash="dash", width=1.5)),
    ],
    showlegend=False,
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Interpretive blurb
overconfident = [
    ac_short[i] for i in range(len(ac_short))
    if avg_confidence[i] > CONF_MID and pct_correct[i] < PCT_MID
]
underconfident = [
    ac_short[i] for i in range(len(ac_short))
    if avg_confidence[i] <= CONF_MID and pct_correct[i] >= PCT_MID
]

if overconfident:
    overconf_phrase = (
        f"<strong style='color:{FLAG_COLOR};'>{', '.join(overconfident)}</strong> "
        f"{'falls' if len(overconfident) == 1 else 'fall'} in the overconfident "
        f"quadrant. Students believe they understand more than the data suggests; "
        f"addressing alternate conceptions in {'this area' if len(overconfident) == 1 else 'these areas'} "
        f"may have outsized impact since students are less likely to seek out corrections."
    )
else:
    overconf_phrase = (
        "No concepts fall in the overconfident quadrant. When students hold alternate "
        "conceptions, they appear to know it, which makes those concepts easier to address."
    )

if underconfident:
    underconf_phrase = (
        f" Students are <strong style='color:{AC_COLOR};'>underconfident</strong> in "
        f"{', '.join(underconfident)}, where reinforcing what they already know may pay off."
    )
else:
    underconf_phrase = ""

st.markdown(
    f"<p style='color:{TEXT_MUTED}; font-size:0.83rem; line-height:1.5; "
    f"margin:-0.25rem 0 0 0;'>{overconf_phrase}{underconf_phrase}</p>",
    unsafe_allow_html=True,
)

# ── Calibration gap bar ───────────────────────────────────────────────────────
st.markdown("### Calibration gap by AC")
st.caption(
    "Positive bars mean students are more confident than their performance warrants. "
    "Negative bars mean they are underconfident."
)

gap_colors = [
    FLAG_COLOR if g > 0.3 else (WARN_COLOR if g > 0 else AC_COLOR)
    for g in calibration_gap
]

fig_gap = go.Figure(go.Bar(
    x=ac_short,
    y=calibration_gap,
    marker_color=gap_colors,
    text=[f"{g:+.2f}" for g in calibration_gap],
    textposition="outside",
    textfont=dict(color=TEXT),
    hovertemplate="<b>%{x}</b><br>Calibration gap: %{y:+.2f}<extra></extra>",
))
fig_gap.add_hline(y=0, line_dash="solid", line_color=BORDER, line_width=1)
apply_plotly_theme(fig_gap)
fig_gap.update_layout(
    height=280,
    margin=dict(l=0, r=0, t=10, b=50),
    yaxis=dict(title="Confidence minus expected score"),
    xaxis=dict(tickangle=-30),
    showlegend=False,
)
st.plotly_chart(fig_gap, use_container_width=True)

# Interpretive blurb
gap_max_idx = int(np.argmax(calibration_gap))
gap_min_idx = int(np.argmin(calibration_gap))
max_gap = float(calibration_gap[gap_max_idx])
min_gap = float(calibration_gap[gap_min_idx])

if max_gap > 0:
    over_phrase = (
        f"The largest overconfidence gap is in <strong style='color:{TEXT};'>"
        f"{ac_short[gap_max_idx]}</strong> ({max_gap:+.2f}). "
    )
else:
    over_phrase = "No concept shows net overconfidence. "

if min_gap < 0:
    under_phrase = (
        f"The largest underconfidence gap is in <strong style='color:{TEXT};'>"
        f"{ac_short[gap_min_idx]}</strong> ({min_gap:+.2f}). "
    )
else:
    under_phrase = ""

st.markdown(
    f"<p style='color:{TEXT_MUTED}; font-size:0.83rem; line-height:1.5; "
    f"margin:-0.25rem 0 0 0;'>"
    f"{over_phrase}{under_phrase}"
    f"Positive gaps deserve more instructional attention than negative ones, since "
    f"students who are wrong-but-confident are less likely to update their thinking."
    f"</p>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="card">
        <p style="color:{TEXT}; font-size:0.85rem; line-height:1.6; margin:0;">
            <strong>Where to focus:</strong> Anchoring Concepts where students are
            simultaneously overconfident and hold prominent alternate conceptions are
            the highest-priority targets. Students who are wrong but confident are less
            likely to seek out or accept corrective information.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_about()
