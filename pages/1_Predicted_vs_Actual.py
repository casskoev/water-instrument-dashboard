"""
Page 1 — Predicted vs. Actual
Instructor enters predictions before seeing results, then submits to reveal the comparison radar.

Placed first in the navigation so the bare confidence/performance charts on
later pages do not spoil the prediction exercise here. After the radar, each
Anchoring Concept's divergence card surfaces the count of flagged items and
lets the instructor jump straight to those items on the Anchoring Concept
Trends page.
"""

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import auth
from data import ANCHORING_CONCEPTS, get_data
from theme import (
    inject_css, page_header, data_banner, sidebar_about, apply_plotly_theme,
    CC_COLOR, AC_COLOR, FLAG_COLOR, TEXT, TEXT_MUTED, BORDER, SURFACE, SURFACE_ALT,
)

st.set_page_config(page_title="Predicted vs. Actual", page_icon=None, layout="wide")
auth.require_login()
inject_css()

# Page-local CSS for the prediction flow (step badge, surprise tags).
st.markdown(
    f"""
    <style>
    .step-badge {{
        display: inline-block;
        background: {SURFACE_ALT};
        color: {TEXT_MUTED};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 0.18rem 0.7rem;
        font-size: 0.72rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    .surprise-tag {{
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-right: 0.4rem;
        letter-spacing: 0.02em;
    }}
    .surprise-tag.over {{
        background: rgba(255,107,107,0.12);
        color: {FLAG_COLOR};
        border: 1px solid rgba(255,107,107,0.35);
    }}
    .surprise-tag.under {{
        background: rgba(77,168,255,0.12);
        color: {AC_COLOR};
        border: 1px solid rgba(77,168,255,0.35);
    }}
    .surprise-tag.aligned {{
        background: rgba(61,220,151,0.12);
        color: {CC_COLOR};
        border: 1px solid rgba(61,220,151,0.35);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

page_header(
    "Predicted vs. actual",
    "Start here. Predict your students' performance before seeing the data, then explore the gaps.",
)

st.markdown(
    f"""
    <div class="card">
        <p style="color:{TEXT}; font-size:0.9rem; line-height:1.6; margin:0;">
            Predict your students' performance <strong>before</strong> seeing the data,
            then reveal how your expectations compare to actual results. Moments of
            surprise, where actual performance diverges from your prediction, are often
            the most productive for generating new instructional conclusions. As one
            instructor put it:
            <em>"I tend to fixate on the things that I know are problems and not necessarily
            recognize the things that they are good at."</em>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

df, is_real = get_data()
data_banner(df, is_real)

ac_names = list(ANCHORING_CONCEPTS.keys())
ac_short = [k.split(": ")[1] for k in ac_names]

actual_scores = []
flagged_counts = {}
for ac_name, ac_info in ANCHORING_CONCEPTS.items():
    items_in_ac = [i for i in ac_info["items"] if i in df["item_id"].values]
    if items_in_ac:
        ac_df = df[df["item_id"].isin(items_in_ac)]
        actual_scores.append(round(ac_df["cc_pct"].mean()))
        flagged_counts[ac_name] = int(ac_df["prominent_ac"].sum())
    else:
        actual_scores.append(50)
        flagged_counts[ac_name] = 0

if "predictions_submitted" not in st.session_state:
    st.session_state.predictions_submitted = False
if "saved_predictions" not in st.session_state:
    st.session_state.saved_predictions = None

# ── Step 1: collect predictions ──────────────────────────────────────────────
if not st.session_state.predictions_submitted:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<span class="step-badge">Step 1 of 2</span>', unsafe_allow_html=True)
    st.markdown("### Before you see the data, what do you predict?")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.88rem; line-height:1.6; margin-bottom:1rem;'>"
        "For each Anchoring Concept, estimate the percentage of your students who answered "
        "those items correctly. Your actual results will not appear until you submit.</p>",
        unsafe_allow_html=True,
    )

    predicted_scores = []
    cols = st.columns(4)
    for i, ac_name in enumerate(ac_names):
        short = ac_name.split(": ")[1]
        with cols[i % 4]:
            pred = st.slider(
                short,
                min_value=0,
                max_value=100,
                value=50,
                step=5,
                key=f"pred_{i}",
                help=f"Your predicted % correct for {ac_name}",
            )
            predicted_scores.append(pred)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Submit predictions and reveal results", type="primary"):
        st.session_state.saved_predictions = predicted_scores
        st.session_state.predictions_submitted = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Step 2: reveal ───────────────────────────────────────────────────────────
else:
    predicted_scores = st.session_state.saved_predictions

    st.markdown(
        f"""
        <div class="card">
            <span class="step-badge">Step 2 of 2</span>
            <h3 style="margin:0 0 0.4rem 0;">Predictions submitted</h3>
            <p style="color:{TEXT_MUTED}; font-size:0.88rem; line-height:1.6; margin:0;">
                The radar below compares your predictions (blue dotted) against your students'
                actual performance (green). Scroll for a per-Anchoring-Concept breakdown,
                with shortcuts into the alternate conceptions present in your students'
                responses.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start over with new predictions"):
        st.session_state.predictions_submitted = False
        st.session_state.saved_predictions = None
        st.rerun()

    st.markdown("### Radar comparison")

    categories = ac_short + [ac_short[0]]
    actual_closed = actual_scores + [actual_scores[0]]
    predicted_closed = predicted_scores + [predicted_scores[0]]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=actual_closed,
        theta=categories,
        fill="toself",
        fillcolor="rgba(61,220,151,0.18)",
        line=dict(color=CC_COLOR, width=2.5),
        name="Actual performance",
        hovertemplate="<b>%{theta}</b><br>Actual: %{r}%<extra></extra>",
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=predicted_closed,
        theta=categories,
        fill="toself",
        fillcolor="rgba(77,168,255,0.10)",
        line=dict(color=AC_COLOR, width=2.5, dash="dot"),
        name="Your prediction",
        hovertemplate="<b>%{theta}</b><br>Predicted: %{r}%<extra></extra>",
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100], ticksuffix="%",
                gridcolor=BORDER, tickfont=dict(size=10, color=TEXT_MUTED),
            ),
            angularaxis=dict(tickfont=dict(size=11, color=TEXT)),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=500,
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color=TEXT),
        legend=dict(orientation="h", y=-0.1, x=0.25, font=dict(color=TEXT)),
        showlegend=True,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("### Where did expectations diverge?")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.88rem; line-height:1.6; margin:-0.25rem 0 1rem 0;'>"
        "For each Anchoring Concept below, the count of flagged items shows how many "
        "questions in that concept have prominent alternate conceptions. Click "
        "<strong style='color:{TEXT};'>View in Anchoring Concept Trends</strong> on any "
        "card to jump straight to the conceptions students chose and the tailored "
        "instructional resources for them."
        "</p>",
        unsafe_allow_html=True,
    )

    divergences = [
        (ac_names[i], actual_scores[i], predicted_scores[i],
         actual_scores[i] - predicted_scores[i])
        for i in range(len(ac_names))
    ]
    divergences.sort(key=lambda x: abs(x[3]), reverse=True)

    c1, c2, c3 = st.columns(3)
    for idx, (ac_name, actual, predicted, gap) in enumerate(divergences):
        col = [c1, c2, c3][idx % 3]
        short = ac_name.split(": ")[1]
        n_flagged = flagged_counts.get(ac_name, 0)

        if abs(gap) >= 15:
            if gap > 0:
                tag = '<span class="surprise-tag under">Students outperformed expectations</span>'
                insight = (
                    f"Your students scored {abs(gap)}% higher than predicted. "
                    "Worth examining what's working in your approach to this concept."
                )
            else:
                tag = '<span class="surprise-tag over">Students underperformed expectations</span>'
                insight = (
                    f"Your students scored {abs(gap)}% lower than predicted. "
                    "Open the flagged items below to see which alternate conceptions "
                    "they landed on instead, and what evidence-based moves might help."
                )
        else:
            tag = '<span class="surprise-tag aligned">Aligned with prediction</span>'
            insight = (
                f"Actual performance ({actual}%) closely matched your prediction "
                f"({predicted}%)."
            )

        if n_flagged == 0:
            flagged_line = (
                "No alternate conceptions in this concept reached the prominence threshold."
            )
        elif n_flagged == 1:
            flagged_line = (
                "<strong>1 flagged item</strong> with a prominent alternate conception "
                "in this concept."
            )
        else:
            flagged_line = (
                f"<strong>{n_flagged} flagged items</strong> with prominent alternate "
                "conceptions in this concept."
            )

        with col:
            st.markdown(
                f"""
                <div class="card">
                    <h4 style="margin-top:0;">{short}</h4>
                    {tag}
                    <p style="color:{TEXT}; font-size:0.85rem; margin-top:0.4rem; line-height:1.5;">
                        {insight}
                    </p>
                    <p style="margin-top:0.5rem; font-size:0.78rem; color:{TEXT_MUTED};">
                        Predicted: {predicted}% &nbsp;|&nbsp; Actual: {actual}%
                    </p>
                    <p style="margin-top:0.6rem; font-size:0.82rem; color:{TEXT};">
                        {flagged_line}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Button placed outside the card markdown so Streamlit can wire its state.
            if n_flagged > 0:
                if st.button(
                    f"View flagged items in {short}",
                    key=f"goto_{ac_name}",
                    use_container_width=True,
                ):
                    st.session_state["preselect_ac"] = ac_name
                    st.switch_page("pages/2_Anchoring_Concepts_Trends.py")
            else:
                if st.button(
                    f"Browse {short}",
                    key=f"goto_{ac_name}",
                    use_container_width=True,
                ):
                    st.session_state["preselect_ac"] = ac_name
                    st.switch_page("pages/2_Anchoring_Concepts_Trends.py")

    st.markdown(
        f"""
        <div class="card" style="margin-top:1rem;">
            <p style="color:{TEXT}; font-size:0.85rem; line-height:1.6; margin:0;">
                <strong>Where to focus:</strong> Areas where you overestimated performance
                (students underperformed) are high-priority targets. Areas where students
                outperformed your expectations can help recalibrate your instructional
                assumptions and reveal productive strengths to build on. Either way,
                the next move is to look at the specific alternate conceptions students
                chose, on the Anchoring Concept Trends page.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

sidebar_about()
