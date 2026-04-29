# Welcome to the Water Instrument Dashboard

This is a short orientation for instructors and collaborators who are new to
the dashboard. If you have questions that are not answered here, contact
Cas Koevoets-Beach.

## What this tool does

The Water Instrument Dashboard helps general chemistry instructors make sense
of their students' responses to the Water Instrument, a research-based
assessment covering the eight ACS Anchoring Concepts. Rather than handing you
raw frequencies and asking you to interpret them, the dashboard surfaces:

- Where students landed on a different conception than the correct one,
  question by question.
- Which of those alternate conceptions were prominent (close to or exceeding
  the rate of the correct conception), so you can prioritize.
- Tailored, evidence-based instructional resources for the prominent patterns
  in your specific cohort.
- A side-by-side comparison of your predictions for student performance and
  what your students actually did.

The point is to bridge the gap between data interpretation and instructional
action: the tool is designed to make the move from "I see a pattern" to
"here is something I can try" as short as possible.

## How to log in

You will receive an account from Cas. Each instructor has their own
username, password, and data file. You only ever see your own cohort's data.

1. Open the dashboard URL Cas sent you. It looks like
   `https://your-app-name.streamlit.app`.
2. Enter your username and password on the sign-in screen.
3. The page header will greet you by name and show the cohort label and
   institution Cas configured for you, so you can confirm you are looking at
   the right dataset.

If you forget your password, contact Cas. Passwords are stored as one-way
hashes; they cannot be recovered, only reset.

## A tour of the pages

The sidebar lists four pages. Use them roughly in this order the first time:

### 1. Anchoring Concept Trends

This is the main page. For each of the eight ACS Anchoring Concepts, you see
your students' response distribution on every item in that concept. Each item
gets a small horizontal bar chart with one bar per answer choice (A through D).

- A green bar is the **correct** answer.
- A blue bar is a **prominent alternate conception**, meaning students chose it
  at a rate within 15 percentage points of the correct answer.
- A gray bar is an alternate conception students chose less often.
- A red triangle (▲) above an item title flags items where at least one
  alternate conception is prominent.

Next to each chart is a brief summary: the correct conception text, and any
prominent alternate conception text, both with their letter and percentage.
Below each chart is an expander labeled "Full detail and resources for Item N".
Open it to see the full question stem, every conception in A-to-D order, the
vocabulary note (when relevant), and the tailored pedagogical resources mapped
to the prominent alternate conception.

The filters at the top let you sort items within each concept (by number, by
flagged-first, or by lowest correct conception percentage), restrict to
flagged items only, or hide concepts you do not want to look at right now.

### 2. Predicted vs. Actual

Open this **before** you spend much time on the other pages. The page asks
you to predict your students' performance on each Anchoring Concept before
revealing actual results, and then visualizes the gap. Moments where your
prediction was off, in either direction, tend to be the most productive
starting points for new instructional ideas.

The page is sequenced first in the navigation specifically so other pages do
not spoil the prediction exercise.

### 3. Student Confidence

Looks at students' own confidence ratings alongside their actual performance.
The calibration map quadrants help identify concepts where students are
overconfident (high confidence with low performance), underconfident (low
confidence with high performance), well calibrated, or low engagement.

The interpretive blurbs under each chart call out the highest and lowest
extremes by name, so you can scan the page and pick out which concepts
deserve closer attention.

### 4. Demographic Trends

Shows how performance breaks down across student demographic groups, where
that data was collected. The framing is intentional: differences across
groups reflect structural and instructional factors, not student ability.
Use this page as a prompt to ask what about the course design, support
structures, or instruction is producing the patterns you see.

## Reading the colors and flags

Three colors carry the data semantics across every chart and pill:

- **Green** is the correct conception (the "Most Correct Conception").
- **Blue** is a prominent alternate conception.
- **Gray** is an alternate conception that students chose, but not at a rate
  that crosses the prominence threshold.

The red triangle (▲) and the red "Items with prominent ACs" stat at the top
of each page are a separate dimension: they flag items where at least one
alternate conception is prominent. A flagged item has at least one blue bar
in its chart.

In the expander, each conception is labeled with its role:

- "Most Correct Conception" (green pill) is what the instrument scores as
  correct.
- "Prominent Alternate Conception" (blue pill) is a wrong answer that
  students chose often enough to merit attention.
- "Alternate Conception" (gray pill) is a wrong answer that some students
  chose, but not at a high enough rate to be flagged.

## Where your data lives

Each instructor's response data lives in a private OneDrive file owned by
the project lead. The dashboard fetches your file each time you load a page,
so updates to your file appear within a few minutes.

The deployed application code is in a private GitHub repository. No data
files live there. The only thing in the repo is the application code itself
plus the item bank (questions, alternate conceptions, vocabulary notes,
research resources), which is the same content for everyone.

Your password is stored as a one-way bcrypt hash, not as plaintext, in the
deployed application's secrets manager. Cas can rotate it but cannot recover
the original.

The data files contain anonymous response data only (answer choices and
confidence ratings per question). They do not contain student names, student
IDs, or any other identifying information.

## How to give feedback or ask for help

Issues, feature requests, or "this number looks wrong" reports go to Cas at
cassiekoevoets@gmail.com. Especially welcome:

- Things that are confusing about how a chart is presented.
- Cases where the prominent-AC threshold flagged something you would not
  have flagged, or missed something you would have.
- Resources you think should be added (or removed) for a particular item.
- Pages or sections that you find yourself ignoring.

Honest feedback about what does and does not help your interpretation is
the single most useful thing you can do for the project, because the whole
point of the tool is to support instructional action, and we can only know
whether it does that by asking the people using it.
