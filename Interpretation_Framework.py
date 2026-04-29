"""
Water Instrument Dashboard — landing page.
Authenticated entry point. After login, routes to the four data pages.
"""

import streamlit as st

import auth
from theme import inject_css, page_header, sidebar_about, AC_COLOR, CC_COLOR, TEXT, TEXT_MUTED

st.set_page_config(
    page_title="Water Instrument Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# Block until the user is signed in. Sets data_path / cohort_label / institution
# in session_state for downstream pages.
user = auth.require_login()

# ── Authenticated landing ─────────────────────────────────────────────────────
subtitle = (
    f"{user['cohort_label']} · {user['institution']}"
    if user.get("institution") else user.get("cohort_label", "")
)

page_header(
    f"Welcome back, {user['name'].split()[0]}",
    subtitle or "Where do your students think differently, and what can you do about it?",
)

st.markdown(
    f"""
    <div class="card">
        <p style="color:{TEXT}; line-height:1.6; margin:0;">
            This dashboard surfaces patterns in how your students answered the
            <strong>Water Instrument</strong>, a research-based assessment covering the eight
            ACS Anchoring Concepts for General Chemistry. Use it to find where students
            landed on a different idea than the correct one, and to pull up
            evidence-based instructional resources for those specific patterns.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Start here")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="card">
            <h4 style="margin-top:0;">Anchoring Concept trends</h4>
            <p style="color:{TEXT_MUTED}; font-size:0.85rem; line-height:1.5; margin-bottom:0.5rem;">
                Per-item response distributions with click-to-expand item detail and tailored
                pedagogical resources for flagged alternate conceptions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open trends", key="go_trends", use_container_width=True):
        st.switch_page("pages/1_Anchoring_Concepts_Trends.py")

with col2:
    st.markdown(
        f"""
        <div class="card">
            <h4 style="margin-top:0;">Student confidence</h4>
            <p style="color:{TEXT_MUTED}; font-size:0.85rem; line-height:1.5; margin-bottom:0.5rem;">
                How well student confidence aligns with their actual performance, per Anchoring Concept.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open confidence", key="go_conf", use_container_width=True):
        st.switch_page("pages/3_Student_Confidence.py")

with col3:
    st.markdown(
        f"""
        <div class="card">
            <h4 style="margin-top:0;">Predicted vs. actual</h4>
            <p style="color:{TEXT_MUTED}; font-size:0.85rem; line-height:1.5; margin-bottom:0.5rem;">
                Compare what you expected your students to know to what the data revealed.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open radar", key="go_radar", use_container_width=True):
        st.switch_page("pages/2_Predicted_vs_Actual.py")

st.markdown(
    f"""
    <div class="card" style="margin-top:1.25rem;">
        <p style="color:{TEXT_MUTED}; font-size:0.82rem; line-height:1.6; margin:0;">
            <strong style="color:{TEXT};">Why this tool exists.</strong>
            Instructors can usually identify gaps in student understanding. The harder
            step is moving from <em>what to notice</em> to <em>what to do next</em>. This
            dashboard is built around that step. The
            <span style="color:{CC_COLOR};">tailored resources</span> on the
            Alternate Conceptions page connect each prominent pattern in your data to a
            specific evidence-based instructional move.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_about()
