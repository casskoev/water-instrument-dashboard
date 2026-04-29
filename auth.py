"""
Authentication wrapper around streamlit-authenticator.

Use from any page:
    import auth
    user = auth.require_login()   # blocks via st.stop() if not signed in
    # user is a dict: {"username", "name", "data_path", "institution", "cohort_label", ...}

Behavior:
    1. Loads credentials from credentials.yaml at the app root.
    2. Renders the login form when the user is not authenticated.
    3. On successful login, stores the user's data_path, institution, and cohort_label
       in st.session_state so data.py and the page headers can pick them up.
    4. Adds a "Sign out" button to the sidebar.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from theme import inject_css, page_header, TEXT_MUTED, BORDER, TEXT


# ── Config loading ────────────────────────────────────────────────────────────
APP_ROOT = Path(__file__).resolve().parent
CREDENTIALS_FILE = APP_ROOT / "credentials.yaml"


def _load_config() -> dict:
    """Load credentials. Tries Streamlit secrets first, then credentials.yaml.

    For production deploys, paste the YAML content into Streamlit secrets
    under [auth] credentials_yaml = \"\"\"...\"\"\".
    For local development, the credentials.yaml file is enough.

    Loaded fresh on every run. streamlit-authenticator may mutate this dict
    in place, so caching would corrupt subsequent runs.
    """
    # Production: read the YAML blob from Streamlit secrets if present.
    try:
        yaml_str = st.secrets.get("auth", {}).get("credentials_yaml")
    except Exception:
        yaml_str = None
    if yaml_str:
        return yaml.load(yaml_str, Loader=SafeLoader)

    # Local dev: fall back to credentials.yaml on disk.
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


def _cookie_key(config: dict) -> str:
    """Prefer the cookie key from Streamlit secrets, fall back to YAML."""
    try:
        return st.secrets["auth"]["cookie_key"]
    except Exception:
        return config["cookie"]["key"]


def _build_authenticator() -> stauth.Authenticate:
    """Build fresh on every run. streamlit-authenticator must NOT be cached
    because it renders widgets, which would trigger CachedWidgetWarning and
    serve stale auth state."""
    config = _load_config()
    return stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        cookie_key=_cookie_key(config),
        cookie_expiry_days=config["cookie"]["expiry_days"],
    )


# ── Public API ────────────────────────────────────────────────────────────────
def require_login() -> dict:
    """Block the page until the user is signed in.

    Returns the logged-in user's record (a dict from credentials.yaml plus
    a 'username' key). Sets the following session_state keys for downstream code:
        - data_path
        - cohort_label
        - institution
        - display_name
    """
    inject_css()  # ensure dark theme is applied even on the login screen
    authenticator = _build_authenticator()
    config = _load_config()

    # streamlit-authenticator 0.3.x writes auth status into session_state directly.
    authenticator.login(location="main", key="login")

    status = st.session_state.get("authentication_status")

    if status is False:
        page_header("Water Instrument Dashboard", "Sign in to view your students' data.")
        st.error("Username or password is incorrect.")
        st.stop()

    if status is None:
        page_header("Water Instrument Dashboard", "Sign in to view your students' data.")
        st.markdown(
            f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; margin-top:0.5rem;'>"
            "Don't have an account? Contact the Balabanoff Research Group to be added."
            "</p>",
            unsafe_allow_html=True,
        )
        st.stop()

    # Authenticated. Look up the user record and stash useful fields in session.
    username = st.session_state.get("username")
    record = config["credentials"]["usernames"].get(username, {}) or {}

    user = {
        "username": username,
        "name": record.get("name", username),
        "email": record.get("email"),
        "data_path": _resolve_data_path(record.get("data_path")),
        "institution": record.get("institution", ""),
        "cohort_label": record.get("cohort_label", ""),
    }

    st.session_state["data_path"] = user["data_path"]
    st.session_state["cohort_label"] = user["cohort_label"]
    st.session_state["institution"] = user["institution"]
    st.session_state["display_name"] = user["name"]

    _render_sidebar_account(authenticator, user)
    return user


def _resolve_data_path(raw: Optional[str]) -> Optional[str]:
    """Normalize a credentials data_path.

    Pass through http(s) URLs unchanged (e.g. OneDrive share links).
    For local paths, turn relative paths into absolute paths anchored at the app root.
    """
    if not raw:
        return None
    if isinstance(raw, str) and raw.startswith(("http://", "https://")):
        return raw
    p = Path(raw)
    if not p.is_absolute():
        p = APP_ROOT / p
    return str(p)


# ── Sidebar account block ────────────────────────────────────────────────────
def _render_sidebar_account(authenticator: stauth.Authenticate, user: dict) -> None:
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
        try:
            authenticator.logout(button_name="Sign out", location="sidebar", key="logout")
        except TypeError:
            # older streamlit-authenticator API
            authenticator.logout("Sign out", "sidebar")
