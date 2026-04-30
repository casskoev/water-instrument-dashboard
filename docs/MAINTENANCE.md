# Maintenance and Updates SOP

This document covers the day-to-day workflows for keeping the Water
Instrument Dashboard up to date: editing items, adding tailored resources,
adjusting vocabulary notes, and getting changes deployed.

The audience is the project maintainer or anyone they hand the keys to. 
Following this SOP keeps the local repository, the deployed app, and
the item bank in sync.

## Other documentation

If you are an instructor using the dashboard rather than maintaining it,
[COLLABORATORS.md](COLLABORATORS.md) is the right doc. If you are completely
new to code and deployed apps and want a gentler tour before diving into
SOPs, start with [ONBOARDING.md](ONBOARDING.md).

## Where things live

- `data.py` is the single source of truth for the item bank, the tailored
  resources library, and the correct answer key. If you are changing any
  of those, you are editing this file.
- `pages/1_Anchoring_Concepts_Trends.py` and the other page files render the
  data; they don't usually need editing for content updates.
- `theme.py` defines colors, fonts, and shared CSS. Edit only when changing
  visual style.
- `credentials.yaml` (local) and the Streamlit Cloud Secrets panel
  (deployed) hold user accounts. Edit when adding or removing instructors.

For any content change, the workflow is roughly the same: edit the file,
test locally, commit, push. Streamlit Cloud auto-redeploys on push.

## The item bank

In `data.py`, every assessment item is a key in the `ITEMS` dict. A typical
entry looks like this:

```python
17: {
    "text": "Which of the following best describes the phase change of water boiling at 100°C?",
    "correct_choice": "H₂O molecules gain energy resulting in a phase change to gas, and temperature remains constant.",
    "correct_conception": "Temperature remains constant during a phase change",
    "alternate_conceptions": [
        "At boiling point, temperature continues to increase prior to phase change",
        "Temperature increases beyond the boiling point during process of evaporation",
    ],
    "vocab_note": "Heating curve diagrams are frequently used but students may misread the plateau as 'nothing happening.'",
},
```

Field-by-field:

- `text`: the question stem as students saw it.
- `correct_choice`: the exact wording of the correct answer choice as it
  appeared on the instrument. Mostly used for documentation; the dashboard
  itself does not display this field.
- `correct_conception`: a short label describing what understanding produces
  the correct answer. This is what shows up in the green pill.
- `alternate_conceptions`: a list of short labels for each wrong-answer
  conception. **Order matters**: position in this list maps to choice number
  in the order wrong choices appear after skipping the correct one. See the
  next section for details.
- `vocab_note`: optional. A note about vocabulary that may have caused
  students to choose a wrong answer. Shown only when the item is flagged.

### How alternate_conceptions order maps to A/B/C/D

The dashboard reads raw answer choice numbers (1, 2, 3, 4) from your data
file. To know which conception text to display next to each wrong choice,
it walks the wrong choices in numerical order and pairs them up with the
`alternate_conceptions` list in order.

Example: if `correct_choice` for an item is C (choice 3), the wrong choices
in numerical order are A, B, D (1, 2, 4). The mapping is:

- A (choice 1) → `alternate_conceptions[0]`
- B (choice 2) → `alternate_conceptions[1]`
- D (choice 4) → `alternate_conceptions[2]`

When you write or edit a list, double-check that the entries are in the
order of the wrong-answer choices in the original instrument, not in some
other order (for example, by frequency or by importance). Otherwise the
text in the inline pill and the bar in the chart will refer to different
conceptions.

### CORRECT_ANSWERS

`CORRECT_ANSWERS` is a flat dict mapping item ID to choice number (1, 2, 3,
or 4). Keep this in sync with the instrument's official answer key. If you
change `correct_choice` on an item, also change the corresponding entry in
`CORRECT_ANSWERS`.

## Adding or editing tailored resources

In `data.py`, the `RESOURCES` dict maps item ID to a list of resource
records. Each resource is a dict with six fields:

```python
17: [
    {
        "ac": "At boiling point, temperature continues to increase prior to phase change",
        "title": "Roles of Terminology, Experience, and Energy Concepts in Student Conceptions of Freezing and Boiling",
        "type": "Research Article",
        "url": "https://pubs.acs.org/doi/10.1021/ed2007668",
        "description": "Investigates how students reason about the temperature-energy relationship during phase changes, including the plateau misconception.",
        "asset_note": "Students understand that heating a substance changes something. Scaffold toward distinguishing temperature (average kinetic energy) from energy input, which goes into breaking IMFs during a phase change.",
    },
],
```

Field guide:

- `ac`: the exact text of the alternate conception this resource addresses.
  Copy it verbatim from `alternate_conceptions` so the link is unambiguous.
- `title`: full title of the article, simulation, or activity, exactly as
  the source uses it.
- `type`: one of "Research Article", "Simulation", "Classroom Activity",
  "Research Chapter". If you need a new type, add it consistently across
  resources.
- `url`: a direct link to the resource. Prefer the publisher's DOI or
  permanent URL over a temporary one.
- `description`: one or two sentences describing what the resource shows
  or offers, framed in a way that helps the instructor decide whether to
  click through.
- `asset_note`: this is the most important field. Frame the alternate
  conception as something students do understand, then describe how to
  build forward from there. The dashboard's whole pedagogical logic is
  asset-based; resources framed as "students are wrong about X, here's how
  to fix it" undermine that. Lead with what students get right, then
  redirect.

### Adding a new resource to an existing item

1. Open `data.py`. Find the entry for that item ID in `RESOURCES`.
2. Add a new dict to the list, following the format above.
3. If the item ID is not yet a key in `RESOURCES`, add it as a new key with
   a list of one entry.
4. Save, test, commit, push (see the deployment section below).

### Editing or removing an existing resource

Find the entry in `RESOURCES[item_id]` and edit the dict in place, or remove
it from the list. Resources are not used anywhere else in the codebase, so
edits are safe.

## Updating an item's question text or conceptions

If the instrument itself was revised:

1. Update `text`, `correct_choice`, `correct_conception`, and
   `alternate_conceptions` in the `ITEMS[N]` entry as needed.
2. If the correct choice changed, update `CORRECT_ANSWERS[N]`.
3. If the number of choices changed, the dashboard adapts automatically;
   items with three valid choices simply show a blank D bar.
4. If you reordered the alternate conceptions, double-check the order
   matches wrong-choice number order, as described above.
5. Update any tailored resources in `RESOURCES[N]` whose `ac` field no
   longer matches the new alternate conception text. The matching is by
   exact string, so a typo or capitalization difference will break the
   pairing.

## Adding a brand new item

Less common, but the procedure is:

1. Add the item ID to the appropriate Anchoring Concept's `items` list in
   `ANCHORING_CONCEPTS`.
2. Add `ITEMS[N]` with all required fields.
3. Add `CORRECT_ANSWERS[N]`.
4. Update each instructor's data file to include `Q{N}` and `QA{N}`
   columns in OneDrive. Without these columns, the new item will be
   silently skipped at load time.
5. Optionally add `RESOURCES[N]` with one or more resources.
6. Test locally, commit, push.

## Vocabulary notes

The `vocab_note` field on an item is shown only when the item is flagged
(at least one alternate conception is prominent). Notes are most useful
when they identify a specific term or phrase that may have steered students
toward a wrong answer. Concrete examples are better than general
admonitions.

If you want to remove a vocabulary note, set `vocab_note` to `None` (not
an empty string), or omit the field entirely.

## Testing locally before pushing

Always test changes locally before pushing to GitHub. The local server
gives you immediate feedback, and you can revert without involving git if
something looks wrong.

```bash
cd "/Users/balabanoffcer/Documents/Claude/Projects/Assessment Data Dashboard"
python3 -m streamlit run Interpretation_Framework.py
```

Open the URL Streamlit prints (usually http://localhost:8501), log in, and
navigate to the page that displays the change. For an item or resource
edit, that is Anchoring Concept Trends → expand the item → check the new
text. For a vocabulary note, check that it appears in the expander when
the item is flagged.

If the dashboard loads but your change does not appear, check that you
saved the file. Streamlit auto-reloads on file save, but only if it can
parse the file. A syntax error in `data.py` (missing comma, mismatched
quote) will leave the previous version in memory.

## Deploying changes to the live app

Once a change looks good locally, push it to GitHub.

```bash
cd "/Users/balabanoffcer/Documents/Claude/Projects/Assessment Data Dashboard"
git status
```

This shows you which files changed. Confirm the list matches what you
expect (usually just `data.py`). If `credentials.yaml`, `.streamlit/secrets.toml`,
or any data file appears in the list, stop. The `.gitignore` should be
excluding them, but if anything sensitive is staged, run `git restore --staged <file>`
to unstage it before committing.

When the staged changes look right:

```bash
git add data.py
git commit -m "Brief description of the change"
git push origin main
```

A useful commit message names what changed and why, in one short line.
Examples:

- "Add tailored resource for item 23 (bond energy)"
- "Update vocabulary note for item 17 (boiling temperature plateau)"
- "Fix typo in correct conception for item 8"

After the push, Streamlit Cloud detects the change and redeploys
automatically. The deployed app is usually back up within thirty to ninety
seconds. Refresh the live URL to confirm the change appears.

## Adding a new instructor

Per-user accounts live in two places: your local `credentials.yaml` and
the Streamlit Cloud Secrets panel for the deployed app. Both must be
updated when adding or removing a user. The local file is for development
and testing; the deployed app reads from Secrets.

1. **Generate a password hash for the new user.**

   ```bash
   python3 scripts/hash_password.py "their_password_here"
   ```

   Copy the hash that prints (starts with `$2b$12$`).

2. **Set up their data file in OneDrive.** Place their data Excel in your
   OneDrive (or have them place it in theirs and share the file with you).
   Right-click the file, choose Share, set to "Anyone with the link can
   view", and confirm "Block download" is OFF. Copy the share URL.

3. **Add them to local `credentials.yaml`** under `usernames:`:

   ```yaml
   newuser:
     name: First Last
     email: their@email.edu
     password: '$2b$12$paste_their_hash_here'
     data_path: 'https://...sharepoint.com/.../paste_their_share_url'
     institution: Their Institution
     cohort_label: Term Year Course Section
   ```

   Note the single quotes around the bcrypt hash and the URL. Both
   contain characters YAML treats as special; the quotes prevent
   misparsing.

4. **Mirror the same entry in Streamlit Cloud Secrets.** Open
   share.streamlit.io, navigate to your app, then Settings → Secrets.
   Find the `credentials_yaml = """ ... """` block and add the new user
   in the same format inside the triple-quoted YAML. Save.

5. **Tell the new user.** Share the deployed app URL, their username, and
   the plaintext password. Ask them to change it the first time they log
   in (you would need to regenerate a new hash for them and update both
   places again, since the dashboard does not yet have a self-serve
   password change UI).

No code change or git push is needed for adding users. Streamlit Cloud
applies Secrets changes immediately.

## Removing an instructor

Same two places. Delete the entry from your local `credentials.yaml` and
from the Streamlit Cloud Secrets `credentials_yaml` block. Save. The user
will no longer be able to sign in.

If you want to be extra careful, also rotate the cookie key
(`[auth] cookie_key` in Streamlit Secrets) so any active session for that
user is also invalidated. Note that rotating the cookie key signs everyone
out, not just the removed user.

## Common pitfalls

- **Updating local but forgetting to push.** Local changes do not propagate
  to the deployed app until you push. After any content change, always run
  `git status`, `git add`, `git commit`, `git push`.

- **Updating local credentials.yaml but not Streamlit Cloud Secrets.** The
  two are independent stores. New instructors must be added to both;
  password changes must be made in both.

- **Quoting in YAML.** bcrypt hashes contain `$` and OneDrive URLs contain
  `:`. Both characters are interpreted by YAML if not quoted. Wrap them
  in single quotes: `password: '$2b$12$...'` and `data_path: 'https://...'`.

- **alternate_conceptions list order.** The list must be in wrong-choice
  numerical order, not in any other order. Otherwise pill text will not
  match the chart bar above it.

- **Editing data while a Streamlit page is open.** Streamlit caches data
  for five minutes per the `@_maybe_streamlit_cache(ttl=300)` on the
  fetch helper. If you update the OneDrive Excel file, the dashboard may
  not pick it up for up to five minutes. To force an immediate refresh,
  reboot the deployed app (Settings → Reboot).

- **Forgetting that `credentials.yaml` and `.streamlit/secrets.toml` and
  the `data/` folder are gitignored.** This is by design; they should
  never be committed. If you need to back them up, do so outside of git
  (a personal note, password manager, or encrypted archive).

## Quick reference: most common workflow

For a typical "add a research article to the resources for item N" task:

```bash
# 1. Edit data.py and add the new dict to RESOURCES[N].

# 2. Test locally
cd "/Users/balabanoffcer/Documents/Claude/Projects/Assessment Data Dashboard"
python3 -m streamlit run Interpretation_Framework.py
# verify the resource appears in the expander for item N

# 3. Push
git status
git add data.py
git commit -m "Add resource for item N: <short title>"
git push origin main
```

Refresh the live app after about a minute. Done.
