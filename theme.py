"""
Shared theme: color tokens, CSS, and small render helpers.
Every page imports from here so the look stays consistent and CSS lives in one place.
"""

import streamlit as st

# ── Color tokens ──────────────────────────────────────────────────────────────
# Surfaces
BG = "#0E1117"            # page background
SURFACE = "#161B22"       # cards, panels
SURFACE_ALT = "#1C222D"   # hover/secondary surfaces
BORDER = "#2A2F3A"        # subtle borders
DIVIDER = "#222831"       # axis grids, dividers

# Text
TEXT = "#E6E8EC"
TEXT_MUTED = "#8A93A6"
TEXT_DIM = "#5A6276"

# Data semantics
CC_COLOR = "#3DDC97"        # correct conception (bright green for dark canvas)
AC_COLOR = "#4DA8FF"        # prominent alternate conception (blue)
AC_FADED_COLOR = "#4A5060"  # non-prominent ACs (gray)
FLAG_COLOR = "#FF6B6B"      # flag for follow-up

# Soft fills (10% accents, used for callouts)
CC_SOFT = "rgba(61, 220, 151, 0.12)"
AC_SOFT = "rgba(77, 168, 255, 0.12)"
FLAG_SOFT = "rgba(255, 107, 107, 0.12)"
WARN_SOFT = "rgba(255, 191, 71, 0.10)"

# Plotly defaults applied to every figure via apply_plotly_theme()
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=TEXT, size=12),
    xaxis=dict(gridcolor=DIVIDER, zerolinecolor=DIVIDER, linecolor=BORDER, tickcolor=BORDER),
    yaxis=dict(gridcolor=DIVIDER, zerolinecolor=DIVIDER, linecolor=BORDER, tickcolor=BORDER),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
    hoverlabel=dict(bgcolor=SURFACE, bordercolor=BORDER, font=dict(color=TEXT)),
)


def apply_plotly_theme(fig):
    """Apply shared dark layout to a Plotly figure. Call before st.plotly_chart."""
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: {TEXT};
}}

.stApp {{
    background: {BG};
}}

h1, h2, h3, h4 {{
    color: {TEXT};
    letter-spacing: -0.01em;
    font-weight: 600;
}}

p, li, span, label {{
    color: {TEXT};
}}

a {{
    color: {AC_COLOR};
    text-decoration: none;
}}
a:hover {{ text-decoration: underline; }}

/* ── Page header (replaces the gradient hero) ──────────────────────────── */
.page-title {{
    font-size: 1.6rem;
    font-weight: 600;
    margin: 0.25rem 0 0.25rem 0;
    color: {TEXT};
}}
.page-subtitle {{
    font-size: 0.92rem;
    color: {TEXT_MUTED};
    margin: 0 0 1.5rem 0;
}}
.page-divider {{
    height: 1px;
    background: {BORDER};
    margin: 0 0 1.5rem 0;
}}

/* ── Cards ─────────────────────────────────────────────────────────────── */
.card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}}
.card.flagged {{
    border-left: 3px solid {FLAG_COLOR};
}}

/* ── Pills and tags ────────────────────────────────────────────────────── */
.pill {{
    display: inline-block;
    border-radius: 20px;
    padding: 0.18rem 0.7rem;
    font-size: 0.78rem;
    font-weight: 500;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
    border: 1px solid {BORDER};
    background: {SURFACE_ALT};
    color: {TEXT};
}}
.pill.cc {{
    background: {CC_SOFT};
    border-color: rgba(61, 220, 151, 0.35);
    color: {CC_COLOR};
}}
.pill.ac {{
    /* Non-prominent alternate conception. Matches the gray bar in the chart. */
    background: rgba(74, 80, 96, 0.25);
    border-color: {BORDER};
    color: {TEXT_MUTED};
}}
.pill.prominent {{
    /* Prominent alternate conception. Matches the blue bar in the chart. */
    background: {AC_SOFT};
    border-color: rgba(77, 168, 255, 0.45);
    color: {AC_COLOR};
    font-weight: 600;
}}
.pill.muted {{
    color: {TEXT_MUTED};
}}

/* ── Flag glyph (used inline next to flagged items) ────────────────────── */
.flag-mark {{
    color: {FLAG_COLOR};
    font-weight: 600;
    margin-right: 0.25rem;
}}
.flag-badge {{
    display: inline-block;
    background: {FLAG_SOFT};
    color: {FLAG_COLOR};
    border: 1px solid rgba(255, 107, 107, 0.35);
    border-radius: 20px;
    padding: 0.1rem 0.55rem;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 0.5rem;
    vertical-align: middle;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}}

/* ── Notes / callouts ──────────────────────────────────────────────────── */
.note {{
    border-left: 2px solid {AC_COLOR};
    background: {AC_SOFT};
    padding: 0.6rem 0.9rem;
    border-radius: 4px;
    font-size: 0.85rem;
    color: {TEXT};
    margin: 0.5rem 0;
}}
.note .label {{
    text-transform: uppercase;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    color: {AC_COLOR};
    font-weight: 600;
    margin-right: 0.4rem;
}}
.note.warn {{
    border-left-color: #FFBF47;
    background: {WARN_SOFT};
}}
.note.warn .label {{
    color: #FFBF47;
}}
.note.asset {{
    border-left-color: {CC_COLOR};
    background: {CC_SOFT};
}}
.note.asset .label {{
    color: {CC_COLOR};
}}

/* ── Resource cards (used in tailored resources expander) ──────────────── */
.resource-card {{
    background: {SURFACE_ALT};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin: 0.6rem 0;
}}
.resource-title {{
    font-weight: 600;
    color: {TEXT};
    margin-bottom: 0.25rem;
}}
.resource-type {{
    display: inline-block;
    background: {SURFACE};
    color: {TEXT_MUTED};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 0.05rem 0.45rem;
    font-size: 0.7rem;
    font-weight: 600;
    margin-right: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

/* ── Summary stat ──────────────────────────────────────────────────────── */
.stat {{
    text-align: center;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1rem;
}}
.stat .num {{
    font-size: 2rem;
    font-weight: 700;
    color: {TEXT};
    line-height: 1.1;
}}
.stat .num.flag {{ color: {FLAG_COLOR}; }}
.stat .num.cc {{ color: {CC_COLOR}; }}
.stat .label {{
    font-size: 0.75rem;
    color: {TEXT_MUTED};
    margin-top: 0.25rem;
    letter-spacing: 0.02em;
}}

/* ── Legend row ────────────────────────────────────────────────────────── */
.legend-row {{
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    align-items: center;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 1.25rem;
    font-size: 0.82rem;
    color: {TEXT_MUTED};
}}
.legend-dot {{
    width: 12px;
    height: 12px;
    border-radius: 3px;
    display: inline-block;
    margin-right: 0.4rem;
    vertical-align: middle;
}}

/* ── Sidebar polish ────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {SURFACE};
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] .sidebar-info {{
    font-size: 0.82rem;
    color: {TEXT_MUTED};
    line-height: 1.6;
}}

/* ── Streamlit widget tone-down ────────────────────────────────────────── */
.stButton > button {{
    background: {SURFACE};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 8px;
    font-weight: 500;
}}
.stButton > button:hover {{
    border-color: {AC_COLOR};
    color: {AC_COLOR};
}}
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
}}

/* Streamlit's default success/info/error banners look heavy on dark */
div[data-testid="stAlert"] {{
    background: {SURFACE_ALT};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

/* Tighten default top padding so headers land higher on the page */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}}
</style>
"""


# ── Render helpers ────────────────────────────────────────────────────────────
def inject_css():
    """Apply the shared stylesheet. Call once at the top of every page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Render the page title block. Replaces the old gradient hero."""
    st.markdown(
        f"""
        <div>
            <h1 class="page-title">{title}</h1>
            {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
            <div class="page-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def data_banner(df, is_real: bool):
    """Single source of truth for the 'real data vs demo data' banner.
    Renders a small caption-style line, not a heavy alert box."""
    if is_real:
        n = int(df["n_students"].max()) if len(df) else 0
        st.markdown(
            f"<p style='color:{TEXT_MUTED}; font-size:0.82rem; margin:-0.5rem 0 1rem 0;'>"
            f"Connected to your data file. n = {n} students.</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<p style='color:{TEXT_MUTED}; font-size:0.82rem; margin:-0.5rem 0 1rem 0;'>"
            f"Demo data. Add your Excel file to the app folder to see your students' results.</p>",
            unsafe_allow_html=True,
        )


def sidebar_about():
    """Standardized sidebar footer used on every page."""
    st.sidebar.markdown(
        f"""
        <div class="sidebar-info" style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid {BORDER};">
            <strong style="color:{TEXT};">About</strong><br>
            Built to bridge the researcher and practitioner gap by connecting
            Water Instrument outputs to evidence-based instructional supports.
            <br><br>
            Balabanoff Research Group, University of Louisville.
        </div>
        """,
        unsafe_allow_html=True,
    )
