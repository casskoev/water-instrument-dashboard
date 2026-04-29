"""
Page 1 — Anchoring Concept Trends
Per-item response distributions organized by ACS Anchoring Concept, with click-to-expand
item detail (question text, alternate conceptions, vocabulary notes, tailored resources).

"""

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import auth
from data import ANCHORING_CONCEPTS, ITEMS, RESOURCES, CORRECT_ANSWERS, get_data
from theme import (
    inject_css, page_header, data_banner, sidebar_about, apply_plotly_theme,
    CC_COLOR, AC_COLOR, AC_FADED_COLOR, FLAG_COLOR, TEXT_MUTED, TEXT, BORDER, SURFACE,
)

st.set_page_config(page_title="Anchoring Concept Trends", page_icon=None, layout="wide")
auth.require_login()
inject_css()

page_header(
    "Anchoring Concept Trends",
    "Response distributions for every question, with expandable details and tailored resources.",
)

df, is_real = get_data()
data_banner(df, is_real)

# ── Summary stats ─────────────────────────────────────────────────────────────
flagged_df = df[df["prominent_ac"] == True]
total_items = len(df)
flagged_count = len(flagged_df)
flagged_pct = round(flagged_count / total_items * 100) if total_items else 0
resource_count = sum(len(v) for v in RESOURCES.values())

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f'<div class="stat"><div class="num">{total_items}</div>'
        f'<div class="label">Total Questions</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="stat"><div class="num flag">{flagged_count}</div>'
        f'<div class="label">Questions with Prominent Alternate Conceptions</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="stat"><div class="num">{flagged_pct}%</div>'
        f'<div class="label">Of Questions Flagged</div></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="stat"><div class="num cc">{resource_count}</div>'
        f'<div class="label">Tailored Resources Available</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
# Sort options use a (label, key) structure so the visible label can be changed
# freely without breaking the sort logic below. Edit the strings; the keys
# (the second element) are what the code compares against.
SORT_OPTIONS = [
    ("Question Number",                                  "item_number"),
    ("Prominent Alternate Conceptions First",            "prominent_first"),
    ("Lowest % of Correct Conceptions Picked First",     "cc_low_to_high"),
]
SORT_LABELS = [label for label, _ in SORT_OPTIONS]
SORT_LABEL_TO_KEY = {label: key for label, key in SORT_OPTIONS}

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 2])
with col_ctrl1:
    sort_label = st.selectbox(
        "Sort questions within each Anchoring Concept by",
        SORT_LABELS,
    )
    sort_key = SORT_LABEL_TO_KEY[sort_label]
with col_ctrl2:
    show_flagged_only = st.checkbox("Show Flagged Questions Only", value=False)
with col_ctrl3:
    selected_acs = st.multiselect(
        "Filter by Anchoring Concept",
        list(ANCHORING_CONCEPTS.keys()),
        default=list(ANCHORING_CONCEPTS.keys()),
    )

# ── Legend ────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="legend-row">
        <span><span class="legend-dot" style="background:{CC_COLOR};"></span> Most Correct Conception</span>
        <span><span class="legend-dot" style="background:{AC_COLOR};"></span> Prominent Alternate Conception</span>
        <span><span class="legend-dot" style="background:{AC_FADED_COLOR};"></span> Alternate Conception</span>
        <span style="color:{FLAG_COLOR}; font-weight:600;">▲ Flagged for follow-up</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Shared chart constants ───────────────────────────────────────────────────
LETTERS = ["A", "B", "C", "D"]
n_students_global = int(df["n_students"].max()) if len(df) else 46
x_max = max(10, n_students_global)
x_max = ((x_max + 4) // 5) * 5  # round up to nearest 5 for a clean axis end


def _safe_int(value):
    """Coerce a DataFrame cell to int, or None if missing/NaN/non-numeric.
    Needed because pandas turns columns with any None values into float64,
    so prominent_choice arrives as 2.0 instead of 2."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _prominent_set(row) -> set:
    """Return the set of choice numbers (1..4) that are flagged as prominent
    for this row. Empty set when no AC crosses the prominence threshold."""
    raw = row.get("prominent_choices")
    if raw is None:
        return set()
    try:
        return {int(c) for c in raw if c is not None}
    except TypeError:
        return set()


def render_resource_card(res: dict) -> str:
    """Return the HTML for one tailored-resource card."""
    return (
        f'<div class="resource-card">'
        f'<div class="resource-title">'
        f'<span class="resource-type">{res["type"]}</span>'
        f'<a href="{res["url"]}" target="_blank">{res["title"]}</a>'
        f'</div>'
        f'<p style="font-size:0.85rem; color:{TEXT_MUTED}; margin:0.4rem 0 0 0;">'
        f'{res["description"]}</p>'
        f'<div class="note asset" style="margin-top:0.5rem;">'
        f'<span class="label">Asset framing</span>{res["asset_note"]}</div>'
        f'</div>'
    )


def _choice_text(choice: int, correct: int, item: dict) -> str:
    """Return the conception text for a given answer choice (1..4).

    The alternate_conceptions list is stored in choice-number order
    (skipping the correct choice), so for correct=3 the wrong choices
    are [1, 2, 4] and map to alternate_conceptions[0], [1], [2].
    """
    if choice == correct:
        return item["correct_conception"]
    wrong_choices = [c for c in range(1, 5) if c != correct]
    try:
        ac_idx = wrong_choices.index(choice)
        return item["alternate_conceptions"][ac_idx]
    except (ValueError, IndexError):
        return ""


def render_inline_summary(iid: int, row, item: dict, is_flagged: bool) -> None:
    """Compact summary shown next to the bar chart.
    Walks A..D order so the pills line up with the chart. Shows the correct
    conception plus every prominent AC. Non-prominent ACs are deferred to the
    full-detail expander."""
    n = int(row["n_students"]) or 1
    counts = row["choice_counts"]
    correct = CORRECT_ANSWERS[iid]
    prominent_set = _prominent_set(row)
    n_choices = 1 + len(item["alternate_conceptions"])

    blocks = []
    for choice in (1, 2, 3, 4):
        if choice > n_choices:
            continue
        is_correct = choice == correct
        is_prominent = choice in prominent_set
        if not (is_correct or is_prominent):
            continue

        letter = chr(ord("A") + choice - 1)
        pct = round(counts.get(choice, 0) / n * 100)
        text = _choice_text(choice, correct, item)

        if is_correct:
            pill_class = "pill cc"
            role_tag = "Most Correct Conception"
        else:
            pill_class = "pill prominent"
            role_tag = "Prominent Alternate Conception"

        blocks.append(
            f'<div style="margin-bottom:0.6rem;">'
            f'<span class="{pill_class}">{letter} &middot; {pct}% &middot; '
            f'<span style="font-weight:600;">{role_tag}</span></span>'
            f'<p style="color:{TEXT_MUTED}; font-size:0.82rem; line-height:1.5; '
            f'margin:0.3rem 0 0 0;">{text}</p>'
            f'</div>'
        )

    st.markdown("".join(blocks), unsafe_allow_html=True)


def render_full_detail(iid: int, row, item: dict, is_flagged: bool) -> None:
    """Full item detail. Question text, all conceptions in A..D order, vocab, resources."""
    n = int(row["n_students"]) or 1
    counts = row["choice_counts"]
    correct = CORRECT_ANSWERS[iid]
    prominent_set = _prominent_set(row)
    n_choices = 1 + len(item["alternate_conceptions"])

    # Question text
    st.markdown(
        f'<p style="font-size:1rem; font-weight:500; color:{TEXT}; '
        f'margin:0 0 0.9rem 0; line-height:1.5;">{item["text"]}</p>',
        unsafe_allow_html=True,
    )

    # All conceptions in A..D order so they match the chart above
    for choice in (1, 2, 3, 4):
        if choice > n_choices:
            continue
        letter = chr(ord("A") + choice - 1)
        pct = round(counts.get(choice, 0) / n * 100)
        text = _choice_text(choice, correct, item)

        if choice == correct:
            pill_class = "pill cc"
            role_tag = "Most Correct Conception"
        elif choice in prominent_set:
            pill_class = "pill prominent"
            role_tag = "Prominent Alternate Conception"
        else:
            pill_class = "pill ac"
            role_tag = "Alternate Conception"

        st.markdown(
            f'<div style="margin-bottom:0.6rem;">'
            f'<span class="{pill_class}">{letter} &middot; {pct}% &middot; {role_tag}</span>'
            f'<p style="color:{TEXT}; font-size:0.88rem; line-height:1.5; '
            f'margin:0.3rem 0 0 0.5rem;">{text}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Vocabulary notes follow the same gating rule as tailored resources:
    # only surface them when the item has at least one prominent AC, so the
    # instructor sees them when they are actionable.
    if is_flagged and item.get("vocab_note"):
        st.markdown(
            f'<div class="note"><span class="label">Vocabulary</span>'
            f'{item["vocab_note"]}</div>',
            unsafe_allow_html=True,
        )

    # Tailored resources (only for flagged items)
    if is_flagged and iid in RESOURCES:
        st.markdown(
            f'<p style="color:{TEXT_MUTED}; font-size:0.82rem; line-height:1.5; '
            f'margin:0.9rem 0 0.4rem 0;">'
            "Tailored pedagogical resources for this prominent alternate conception. "
            "These are framed in alignment with responsive teaching principles, positioning "
            "alternate conceptions as productive starting points rather than errors to correct."
            "</p>",
            unsafe_allow_html=True,
        )
        resources_html = "".join(render_resource_card(res) for res in RESOURCES[iid])
        st.markdown(resources_html, unsafe_allow_html=True)
    elif is_flagged:
        st.markdown(
            f'<p style="color:{TEXT_MUTED}; font-size:0.82rem; margin-top:0.9rem;">'
            "Resources for this alternate conception are being developed. "
            "The resource library grows as the CER literature expands.</p>",
            unsafe_allow_html=True,
        )


# ── Per-AC blocks ─────────────────────────────────────────────────────────────
for ac_name, ac_info in ANCHORING_CONCEPTS.items():
    if ac_name not in selected_acs:
        continue

    ac_items = [i for i in ac_info["items"] if i in ITEMS]
    ac_df = df[df["item_id"].isin(ac_items)].copy()

    if show_flagged_only:
        ac_df = ac_df[ac_df["prominent_ac"] == True]
        if ac_df.empty:
            continue

    if sort_key == "prominent_first":
        # Flagged items first; within each group, fall back to item number.
        ac_df = ac_df.sort_values(["prominent_ac", "item_id"], ascending=[False, True])
    elif sort_key == "cc_low_to_high":
        ac_df = ac_df.sort_values("cc_pct")
    else:  # item_number, default
        ac_df = ac_df.sort_values("item_id")

    n_flagged_in_ac = int(ac_df["prominent_ac"].sum())
    flag_html = (
        f'<span class="flag-badge">{n_flagged_in_ac} flagged</span>'
        if n_flagged_in_ac > 0 else ""
    )

    st.markdown(
        f'<div class="card" style="margin-bottom:0.5rem;">'
        f'<div style="display:flex; align-items:center; gap:0.5rem;">'
        f'<h3 style="margin:0;">{ac_name}</h3>{flag_html}</div>'
        f'<p style="color:{TEXT_MUTED}; font-size:0.82rem; margin: 0.25rem 0 0;">'
        f'{ac_info["description"]}</p></div>',
        unsafe_allow_html=True,
    )

    for _, row in ac_df.iterrows():
        iid = int(row["item_id"])
        item = ITEMS[iid]
        counts = row["choice_counts"]
        correct = CORRECT_ANSWERS[iid]
        prominent_set = _prominent_set(row)
        n_choices = 1 + len(item["alternate_conceptions"])
        is_flagged = bool(row["prominent_ac"])

        x_vals = [counts.get(i, 0) for i in (1, 2, 3, 4)]
        bar_colors = []
        for i in (1, 2, 3, 4):
            if i > n_choices:
                bar_colors.append("rgba(0,0,0,0)")
            elif i == correct:
                bar_colors.append(CC_COLOR)
            elif i in prominent_set:
                bar_colors.append(AC_COLOR)
            else:
                bar_colors.append(AC_FADED_COLOR)

        flag_suffix = "  ▲" if is_flagged else ""
        title_text = f"Item {iid}{flag_suffix}"

        fig = go.Figure(go.Bar(
            x=x_vals,
            y=LETTERS,
            orientation="h",
            marker_color=bar_colors,
            hovertemplate="<b>%{y}</b>: %{x} students<extra></extra>",
        ))
        apply_plotly_theme(fig)
        fig.update_layout(
            height=190,
            margin=dict(l=10, r=10, t=34, b=24),
            title=dict(
                text=title_text,
                x=0.5,
                xanchor="center",
                font=dict(size=14, color=FLAG_COLOR if is_flagged else TEXT),
            ),
            xaxis=dict(range=[0, x_max], dtick=2 if x_max <= 50 else 5, title=None),
            yaxis=dict(autorange="reversed", title=None),
            showlegend=False,
        )

        # Chart on the left, brief correct/prominent summary on the right
        col_chart, col_summary = st.columns([3, 2])
        with col_chart:
            st.plotly_chart(fig, use_container_width=True, key=f"ac_chart_{iid}")
        with col_summary:
            render_inline_summary(iid, row, item, is_flagged)

        # Click-to-expand: full question text, all conceptions in A..D order,
        # vocabulary note, and tailored resources.
        expander_label = (
            f"Full detail and resources for Question {iid}"
            if is_flagged
            else f"Full detail for Question {iid}"
        )
        with st.expander(expander_label):
            render_full_detail(iid, row, item, is_flagged)

sidebar_about()
