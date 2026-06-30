"""
Authentication module — pure Streamlit + bcrypt, no third-party auth library.

Replaces streamlit-authenticator to eliminate the extra-streamlit-components
dependency, which is incompatible with Streamlit >= 1.34 on modern Python.

Auth state is stored in st.session_state for the duration of the browser
session. Users will need to sign in again if they close the tab or hard-refresh.

Use from any page:
    import auth
    user = auth.require_login()   # blocks via st.stop() if not signed in
    # user is a dict: {"username", "name", "data_path", "institution", "cohort_label", ...}
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import bcrypt
import streamlit as st
import yaml
from yaml.loader import SafeLoader

from theme import inject_css, page_header, TEXT_MUTED, BORDER, TEXT


# ── Config loading ────────────────────────────────────────────────────────────
APP_ROOT = Path(__file__).resolve().parent
CREDENTIALS_FILE = APP_ROOT / "credentials.yaml"

_SESSION_KEY = "auth_user"


def _load_config() -> dict:
    """Load credentials. Tries Streamlit secrets first, then credentials.yaml.

    For production deploys, paste the YAML content into Streamlit secrets
    under [auth] credentials_yaml = \"\"\"...\"\"\".
    For local development, the credentials.yaml file is enough.
    """
    try:
        yaml_str = st.secrets.get("auth", {}).get("credentials_yaml")
    except Exception:
        yaml_str = None
    if yaml_str:
        return yaml.load(yaml_str, Loader=SafeLoader)

    if not CREDENTIALS_FILE.exists():
        st.error(
            "No credentials configured. For local development, copy "
            "credentials.yaml.example to credentials.yaml and fill it in. "
            "For deployed apps, paste the YAML into Streamlit secrets under "
            "[auth] credentials_yaml."
        )
        st.stop()
    with CREDENTIALS_FILE.open() as f:
        return yaml.load(f, Loader=SafeLoader)


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def _resolve_data_path(raw: Optional[str]) -> Optional[str]:
    """Pass through URLs unchanged; resolve relative local paths from app root."""
    if not raw:
        return None
    if isinstance(raw, str) and raw.startswith(("http://", "https://")):
        return raw
    p = Path(raw)
    if not p.is_absolute():
        p = APP_ROOT / p
    return str(p)


# ── Login form ────────────────────────────────────────────────────────────────
def _render_login_form(config: dict) -> None:
    """Render the login form and authenticate on submit. Calls st.stop() if
    the user is not yet authenticated so the calling page does not continue."""
    page_header("Water Instrument Dashboard", "Sign in to view your students' data.")

    with st.form("login_form"):
        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        users = config.get("credentials", {}).get("usernames", {})
        record = users.get(username)
        if record and _verify_password(password, record.get("password", "")):
            st.session_state[_SESSION_KEY] = {
                "username": username,
                "name": record.get("name", username),
                "email": record.get("email"),
                "data_path": _resolve_data_path(record.get("data_path")),
                "institution": record.get("institution", ""),
                "cohort_label": record.get("cohort_label", ""),
            }
            st.rerun()
        else:
            st.error("Username or password is incorrect.")

    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; margin-top:0.5rem;'>"
        "Don't have an account? Contact the Balabanoff Research Group to be added."
        "</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ── Sidebar account block ─────────────────────────────────────────────────────
def _render_sidebar_account(user: dict) -> None:
    """Show the signed-in user and a sign-out button at the top of the sidebar."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:0.75rem 0.25rem; border-bottom:1px solid {BORDER}; margin-bottom:0.75rem;">
                <p style="margin:0; font-size:0.78rem; color:{TEXT_MUTED}; text-transform:uppercase; letter-spacing:0.05em;">
                    Signed in as
                </p>
                <p style="margin:0.15rem 0 0 0; font-size:0.95rem; font-weight:600; color:{TEXT};">
                    {user['name']}
                </p>
                <p style="margin:0; font-size:0.78rem; color:{TEXT_MUTED};">
                    {user['cohort_label']}{' · ' + user['institution'] if user['institution'] else ''}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Sign out", key="sign_out_button"):
            st.session_state.pop(_SESSION_KEY, None)
            st.rerun()


# ── Public API ────────────────────────────────────────────────────────────────
def require_login() -> dict:
    """Block the page until the user is signed in.

    Returns the logged-in user's record. Sets the following session_state keys
    for downstream code:
        - data_path
        - cohort_label
        - institution
        - display_name
    """
    inject_css()
    config = _load_config()

    user = st.session_state.get(_SESSION_KEY)
    if not user:
        _render_login_form(config)

    # Set session_state keys that data.py and page headers expect.
    st.session_state["data_path"] = user["data_path"]
    st.session_state["cohort_label"] = user["cohort_label"]
    st.session_state["institution"] = user["institution"]
    st.session_state["display_name"] = user["name"]

    _render_sidebar_account(user)
    return user
