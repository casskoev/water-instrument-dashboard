# Water Instrument Dashboard

Instructor-facing interpretation tool for the Water Instrument, a research-based
General Chemistry assessment covering eight of the ACS Anchoring Concepts. Each
instructor signs in and sees only their own students' data alongside tailored
pedagogical resources.

Built by the Balabanoff Research Group at the University of Louisville.

## Documentation

- [docs/ONBOARDING.md](docs/ONBOARDING.md) — start here if you are a new
  graduate student joining the research group with no background in code,
  GitHub, or deployed apps. A gentle, hands-on tour of where everything
  lives and what the back end actually is.
- [docs/COLLABORATORS.md](docs/COLLABORATORS.md) — start here if you are a new
  instructor being onboarded onto the dashboard. Covers what the tool does,
  how to log in, a tour of each page, and how to read the charts.
- [docs/MAINTENANCE.md](docs/MAINTENANCE.md) — start here if you are
  maintaining the dashboard. SOPs for editing items, adding tailored
  resources, adding or removing instructors, testing locally, and pushing
  changes to the deployed app.

The rest of this README covers initial setup, local development, and
deployment. Most day-to-day work belongs in one of the two docs above.

## Project layout

```
.
├── Interpretation_Framework.py      Entry point (Streamlit looks for this)
├── pages/
│   ├── 1_Anchoring_Concepts_Trends.py    Per-item charts + AC detail (merged)
│   ├── 2_Predicted_vs_Actual.py          Predict, then reveal (sequenced first to avoid spoilers)
│   ├── 3_Student_Confidence.py
│   └── 5_Demographic_Trends.py
├── auth.py                          Login wrapper around streamlit-authenticator
├── theme.py                         All shared CSS, colors, and render helpers
├── data.py                          Item bank, resources, data loader
├── scripts/
│   └── hash_password.py             Generate bcrypt hashes for new instructors
├── data/                            (gitignored) instructor data files live here
├── credentials.yaml                 (gitignored) real users; copy from .example
├── credentials.yaml.example         template you fill in
├── .streamlit/
│   ├── config.toml                  dark theme
│   ├── secrets.toml                 (gitignored) cookie key in production
│   └── secrets.toml.example         template
├── requirements.txt
└── .gitignore
```

## Running locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up credentials (one-time)
cp credentials.yaml.example credentials.yaml
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Generate a random cookie key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Paste it into .streamlit/secrets.toml under [auth] cookie_key.

# Generate a bcrypt hash for each user
python scripts/hash_password.py
# Paste the hash into credentials.yaml under that user's password: field.

# 3. Drop each user's Excel file into data/ and update their data_path:
#    data/jdoe_fall2025.xlsx
#    data/mlee_spring2026.xlsx

# 4. Run
streamlit run Interpretation_Framework.py
```

The app opens at http://localhost:8501.

## Deploying to Streamlit Community Cloud

1. Push the repo to GitHub. Keep it **private** if your `data/` folder will
   contain real student response data (FERPA). If you store data outside the
   repo, public is fine.
2. Go to https://share.streamlit.io and connect the repo. Set the entry point
   to `Interpretation_Framework.py`.
3. In the app settings, open the **Secrets** panel and paste the contents of
   your `.streamlit/secrets.toml`. This is how the deployed app reads the
   cookie key.
4. Commit `credentials.yaml` to the repo **only if the repo is private**. If
   public, instead store the credentials inside Streamlit secrets and adapt
   `auth.py` to read from `st.secrets` (one extra branch).
5. Deploy. Streamlit Cloud redeploys on every push to the configured branch.

## Adding a new instructor

1. Generate a hash for their password:

   ```bash
   python scripts/hash_password.py
   ```

2. Add an entry to `credentials.yaml`:

   ```yaml
   credentials:
     usernames:
       newuser:
         name: First Last
         email: their@email.edu
         password: <hash from step 1>
         data_path: data/newuser_term.xlsx
         institution: Their Institution
         cohort_label: Term Year Course Name
   ```

3. Drop their Excel file at the path you specified.
4. Commit (private repo) or update Streamlit secrets (public repo).

## Data file format

Each instructor's Excel file should contain one row per student and the
columns:

- `Q1` ... `Q38` — the answer choice the student selected (1-indexed)
- `QA1` ... `QA38` — the student's confidence rating for that item (1 to 5)

Anything else is ignored. See `data.py:load_real_data` for the exact mapping.

## Security notes

- `credentials.yaml`, `.streamlit/secrets.toml`, and everything under `data/`
  are listed in `.gitignore`. Verify nothing sensitive is staged before your
  first push (`git status`).
- Passwords are stored as bcrypt hashes, not plaintext.
- The cookie key (`secrets.toml`) signs the auth cookie. Rotate it if you
  suspect it has leaked; doing so signs everyone out.
- Each instructor only ever sees the file at their own `data_path`. There is
  no file picker.

## Why this tool exists

Instructors can usually identify gaps in student understanding from
assessment data. The harder step is moving from *what to notice* to *what to
do next*. This dashboard is built around that step. The tailored resources
on the Alternate Conceptions page connect each prominent pattern in your
data to a specific evidence-based instructional move.
