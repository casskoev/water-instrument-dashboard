# A gentle tour of the back end

Welcome. This document is for someone who is new to the research group and
also new to code, GitHub, deployed websites, and the rest of the technical
infrastructure that makes the Water Instrument Dashboard run. You do not
need to know any programming to read or follow this guide. The goal is to
get you oriented enough to find your way around, read the existing docs,
and ask good questions.

Plan to read this in one or two sittings. Nothing in here requires you to
do anything irreversible, so feel free to click around and explore as you
go.

## What you're looking at

The Water Instrument Dashboard is a website that helps general chemistry
instructors interpret data from a research-based assessment. When an
instructor visits the dashboard URL and signs in, they see charts and
tables built specifically for their cohort.

The website itself is what people in software call the **front end**. It is
the part that humans interact with. Behind the front end is everything else
that makes the website possible: the code that decides what to show, the
files that hold the questions and resources, the configuration that
controls who can log in. That is the **back end**, and that is what this
document is about.

The back end is not magical. It is a collection of files, mostly text,
organized into folders. The whole project lives in a folder on a
researcher's computer (Cas, currently), and a copy of that same folder
lives in two other places online. You will learn what those places are
below.

## The three places the project lives

Imagine a single shared Google Doc, but instead of one document, it is a
whole folder of files. There is one canonical version, and copies that
sync to it. The Water Instrument Dashboard works the same way, with three
locations that talk to each other:

**1. The local copy.** This lives on the project lead's laptop. It is a
folder you can open in Finder (or Windows Explorer) and look at. When
someone wants to make a change, they edit the files in this folder, save,
and then push the change up to GitHub.

**2. GitHub.** This is the canonical online version. GitHub is a website
that hosts software projects. Each project there is called a "repository"
or "repo." Our repo is private, meaning only people who are explicitly
given access can see it. The URL looks like
`https://github.com/casskoev/water-instrument-dashboard`.

When someone makes a change locally and pushes it, the new version of the
file appears on GitHub. Everyone with access can see it. This is also
where all the documentation files live, including the one you are reading
now.

**3. Streamlit Cloud.** This is the company that hosts the live website
that instructors use. Whenever a change is pushed to GitHub, Streamlit
Cloud notices, downloads the latest version, and rebuilds the website
from it within about a minute. The instructor URL is
`https://waterinstrumentdashboard.streamlit.app`.

So when an instructor sees a chart on the dashboard, the chain of events
that produced it is: someone wrote code, someone (or the same person)
saved that code in their local folder, someone pushed it to GitHub, and
Streamlit Cloud built the live site from GitHub.

## Vocabulary you will keep hearing

You do not need to memorize these. You will pick them up by encountering
them in context. The list is here so you can come back when a word feels
foreign.

**Repository (or "repo")**: the project as a folder of files, including
all of its history. Our repo is on GitHub.

**Commit**: a saved snapshot of changes. When someone edits a file and
"makes a commit," they are recording, "here is what I changed and why,"
with a short note describing the change. The history of all commits is
preserved forever, which means we can always look back at how the project
evolved.

**Push**: send commits from a local computer up to GitHub. Without
pushing, your changes only exist on your machine.

**Pull**: download new commits from GitHub to a local computer. If
multiple people are working on the project, you pull to get caught up
before you start editing.

**Branch**: a parallel version of the project. The default branch is
called `main`. People sometimes work on a branch to test an idea without
disturbing the main version. For our project, almost everything happens
on `main` directly because there is one maintainer.

**Deploy**: make a new version of the website live. For us this happens
automatically when someone pushes to GitHub.

**Markdown**: a simple way to format text in plain text files. The `.md`
extension on files like `COLLABORATORS.md` and `MAINTENANCE.md` means
they are markdown. You can read them as plain text in any editor, and
GitHub renders them as formatted documents in the browser.

**Python**: the programming language the dashboard is written in. The
files ending in `.py` are Python code. You do not need to know Python to
read the documentation; if you are curious about what code looks like,
opening any `.py` file in a text editor will show you, and a lot of it is
human-readable English organized into structured chunks.

**Streamlit**: the framework that turns the Python code into a working
web app. We use it because it is designed to make data-heavy dashboards
easy to build without needing a separate front-end developer.

## The tools you will use

You probably do not need most of these on day one. Install them as you
need them, not all at once.

**A web browser.** You already have one. You will use it to view the
dashboard, the GitHub repo, and the Streamlit Cloud admin panel. Chrome,
Safari, and Firefox all work fine.

**A text editor.** For reading and editing files, you want something
nicer than TextEdit. Visual Studio Code (VS Code) is free, runs on Mac
and Windows, and is the de facto standard. Download it from
`https://code.visualstudio.com`. You can also use Cursor or Sublime Text;
all three are similar.

**A GitHub account.** Free. Sign up at `https://github.com`. Once you
have an account, ask the project lead to add you as a collaborator on
the repo so you can see it.

**A terminal.** You may not need this for a long time. The terminal is
a text-based way to run commands on your computer. On Mac it is the
"Terminal" app. On Windows the equivalent is "PowerShell" or "Windows
Terminal." Most editing and reading does not require it. You only really
need a terminal when you are actively pushing changes to GitHub.

## Your first hands-on: a guided tour

This part has nothing to install. Just open your browser and follow
along. The point is to get a feel for where things are.

**Step 1: visit the GitHub repo.** Open
`https://github.com/casskoev/water-instrument-dashboard` (or whatever the
current repo URL is; ask the project lead if this one does not work).
Sign in to GitHub if asked. You should see a list of files and folders.

If you do not have access yet, you will see a 404 page. That just means
you have not been added as a collaborator. Ask Morgan or Cas to add you.

**Step 2: open the README.** At the top of the file list there will be
a link to `README.md`. GitHub also displays its rendered contents
automatically below the file list, so you can scroll down to see them. The
README is the "front door" of the project: a brief description of what
this is, links to the other docs, and instructions for setting things up
locally. Skim it.

**Step 3: open the docs folder.** In the file list, find the folder
named `docs/`. Click into it. You will see at least three files:

- `COLLABORATORS.md`: a one-pager for instructors who are using the
  dashboard. Read this if you ever need to explain to an instructor what
  the dashboard does and how to interpret it. Even if you will not be an
  instructor yourself, reading this is the fastest way to understand what
  the dashboard is for.
- `MAINTENANCE.md`: a step-by-step guide for the person maintaining the
  dashboard. Adding new instructors, editing the question bank, adding
  research resources to a flagged alternate conception, and pushing
  changes are all in here. You will refer to this once you start
  contributing.
- `ONBOARDING.md`: this document.

Click `COLLABORATORS.md` and read it. Then click `MAINTENANCE.md` and
read at least the first few sections. Do not worry about understanding
every detail; you are looking for the shape of the document and the
location of the key topics.

**Step 4: peek at the code.** Go back to the top of the repo and click
`data.py`. This is one of the larger files. Most of what you see is
either:

A. A long Python dictionary that holds the bank of assessment questions,
their correct answers, the alternate conceptions students might choose,
and short notes about each. You can read these like a structured outline.

B. Another dictionary that pairs prominent alternate conceptions with
research articles, simulations, or activities that address them.

You do not need to understand the syntax. Notice that the content (the
question text, the conception text, the URLs) is organized in a way you
could in principle edit by hand if you needed to add a resource or fix a
typo. The maintenance doc walks through how.

**Step 5: look at the deployed site.** Open the dashboard URL itself in
a separate tab and sign in (use credentials provided by the project
lead). Click around. The pages you see are produced by the code you
just looked at. The Anchoring Concept Trends page, for example, is built
by `pages/2_Anchoring_Concepts_Trends.py`, which reads from `data.py`
and renders charts. You do not need to know how, only that the
relationship exists.

That is the whole back end. Three places, a folder of files, a website
that pulls from GitHub.

## The shape of the project

Here is what each top-level file or folder does, in plain English. You
can come back to this list when something looks unfamiliar.

- `Interpretation_Framework.py`: the landing page of the dashboard. Where
  users arrive after signing in.
- `pages/`: the four data pages of the dashboard. The number prefix
  controls the order they appear in the sidebar.
- `data.py`: the assessment item bank, the answer key, the tailored
  resources library, and the function that loads instructor data.
- `auth.py`: the login machinery. Reads the list of users from
  configuration and decides whether someone can sign in.
- `theme.py`: the colors, fonts, and shared visual styling.
- `requirements.txt`: a list of Python libraries the app depends on.
  Streamlit Cloud reads this to set up the live environment.
- `README.md`: the project front door.
- `docs/`: the documentation folder, including this guide.
- `scripts/`: small utility scripts, including the password hasher.
- `.streamlit/`: configuration for Streamlit, including the dark theme.
- `data/`: where instructor Excel files would live if they were stored
  locally. Currently empty in the repo because real data files are kept
  in OneDrive (more on that in MAINTENANCE.md).
- `credentials.yaml`: the local list of usernames, password hashes, and
  data file paths. NOT in the GitHub repo for security reasons; only
  exists on the project lead's computer and inside Streamlit Cloud's
  secrets manager.
- `.gitignore`: a list of files git should never push to GitHub. Includes
  `credentials.yaml` and any data files.

If a name in the file list looks scary, find it in this list. There are
no stowaways; everything has a job.

## When to read which document

Different docs serve different purposes. As a new grad student, you will
mostly read, not write. Pick the right doc for the question you have:

- "What does this tool do, and how should an instructor read the
  charts?" Read `docs/COLLABORATORS.md`.
- "How do I add a new instructor / edit a question / add a research
  resource / push a change?" Read `docs/MAINTENANCE.md`.
- "I am totally new and I want to know what these words mean and what to
  click on first." That is this document.
- "How is the project organized as a folder?" The README and the file
  list above.

When you have a question that no document answers, that is also good
information. Add it to the list of things to ask, or improve the docs
later when you understand the answer.

## Reading code without panic

Code looks intimidating because it is unfamiliar, not because it is
inherently hard. A few tricks for getting comfortable:

Code is mostly text. Open any `.py` file in your editor or in GitHub.
Most of it is words, English-shaped phrases, and indentation. The
unfamiliar parts are the punctuation conventions, but you do not need to
deeply understand them to navigate.

Comments are everywhere. Lines starting with `#` are notes by the author
to a future reader. They explain what a section is doing, why a decision
was made, and what to do if you need to change it. Read those first.

Find the dictionaries. Most of the meaningful content in this project
lives in Python dictionaries: structured key-value pairs that look like:

```python
17: {
    "text": "Which of the following best describes the phase change of water boiling at 100°C?",
    "correct_choice": "H₂O molecules gain energy resulting in a phase change to gas, and temperature remains constant.",
    ...
}
```

That is item 17. The "text" field holds the question stem. You can read
this without knowing any Python; the structure is the same as a
spreadsheet, just laid out vertically.

When something does not make sense, write down the question and move on.
You will probably understand it in a week.

## Making your first edit (someday)

You will not make your first contribution today. When you do, the rough
sequence is:

1. The project lead grants you write access on GitHub.
2. You copy the project to your own computer ("clone the repo"), one
   command in the terminal.
3. You install the Python dependencies, one command, with help.
4. You make your edit in the editor of your choice.
5. You test that the dashboard still runs locally.
6. You commit and push your change.

The first time, sit down with someone who has done it before. The fifth
time, you will do it on your own.

## Where to ask for help

When you are stuck:

- Read the docs first. The maintenance doc, especially, has answers to
  most "how do I do X" questions.
- For research-side questions about the project (why does the dashboard
  do this, why are we collecting this data, what is the role of asset
  framing, etc.), ask Morgan, Cas, or another graduate student in the
  group.
- For technical questions about how to run something or fix an error,
  ask Cas.
- When you do ask, be specific. "I tried to do X, I expected Y, and I
  got Z" gets a much faster answer than "this isn't working." Even
  better: paste the exact error message you saw. Most error messages
  contain the answer if you know how to read them; sharing them lets
  someone help you read them.

## A note about the time it takes

Everything in this guide takes time to internalize. The first time you
clone a repo, you will probably do something out of order and panic.
That is the experience of literally every developer who has ever lived.
The fix is not to memorize more facts; it is to do the thing a few
times, slowly, with a more experienced person nearby, until it stops
being scary.

You are well-educated in your discipline, and that pattern of
"unfamiliar at first, comfortable after repetition" is exactly how
learning anything works. Code is no different.

Welcome to the project.
