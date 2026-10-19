# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

My community is r/MCFC (https://www.reddit.com/r/MCFC/). I chose it because I am a big Manchester City fan. While reading 30–40 posts, I noticed four distinctions:

1. Some posts contain a score or other numbers. These are usually sharing the result or stats of a recent match.
2. Some posts end with a question mark. These are usually asking the community for opinions.
3. Some posts make a clear judgment about a player or the club, often with words like "should", "sell", or "overrated". These are usually fan opinions.
4. Some posts contain emojis or lots of exclamation marks. These are usually memes or emotional reactions rather than serious discussion.

Note: many posts in this community rely on images. Since the model only sees text, I will skip posts that cannot be understood without the image.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `share`

**Definition:** Shares a match result, stats, or club news (press conference, transfer) with little or no personal opinion.

**Example 1:**
>[Post Match Thread] Man City 2 - 4 Paris Saint-Germain (UEFA Champions League, League Phase)

**Example 2:**
>Phil Foden has scored 111 goals for Manchester City, and none of them have been penalties

### `question`

**Definition:** Genuinely asks the community for information or their views.


**Example 1:**
>Which jersey do you like the most?

**Example 2:**
>What is something different you've seen in Enzo compared to Pep? What is something they have in common?

### `vent`

**Definition:** Mainly expresses emotion (anger, joy, frustration) without a claim others could argue with.


**Example 1:**
>Banana nanananaaa nanananaaa Cityyyy!!!

**Example 2:**
>Fuck the 114 charges The show must go on…

### `opinion`

**Definition:** Makes a clear judgment or recommendation about a player, the manager, or the club.


**Example 1:**
>Don’t get me wrong. Elliot was immense in the game, but this man got robbed not getting MOTM. Literally involved in every single goal and the red card. Best winger on the planet atm hands down.

**Example 2:**
>Iliman Ndiaye appreciation post. He’s had such an electric start to the season. I can’t imagine what we’d look like if we were still stuck with Savinho (no offence). What an upgrade!

### The hardest boundary

**Which two labels:** `opinion` vs `vent`

Both kinds of posts are emotional and often negative about the team, a player, or the manager. The difference is whether there is a claim someone could actually argue against.

Example borderline post:
> How can we compete against a state owned club like PSG??

**The decision rule I used every time:**
If the post contains a specific claim or recommendation that someone could disagree with (e.g. "we should sell him", "he's overrated", "Pep should start Foden"), it is `opinion`, even if the tone is angry. If it only expresses feeling, or uses a question just to complain, with no arguable claim, it is `vent`. Exaggerated complaints with no specific match, player, or decision named (e.g. "Why do refs ALWAYS give it against us???") are also `vent`.

Related rules for the other boundaries:
- `question` vs `opinion`: A question only counts as `question` if the poster actually wants answers from the community. If the question is just wrapping a clear claim (e.g. "Is it just me or has Rodri looked slow?", "We should start X. Who's with me?"), label it by the claim, which is usually `opinion`.
- `share` vs `opinion`: If the main point is a stat, result, or news item and any judgment is one short add-on (e.g. "OFFICIAL: X signs a new deal. Massive news!"), it is `share`. If the judgment is the main point and the stat is used as evidence for it, it is `opinion`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** The 400 newest posts on r/MCFC, pulled from the subreddit's RSS feed with `fetch_posts.py` (Reddit blocks the `.json` endpoint) into `raw_posts.csv`. I kept 266: posts that can't be understood without their image or video were removed, and so were exact duplicates (mostly the repeated Daily Discussion thread). Post text is not trimmed.

**How I labelled them:** AI pre-labeled the batch and I reviewed and corrected every row; the first 20 rows were labeled cold (by hand, before seeing any AI labels). Rows where the AI was unsure between two labels say why in the `note` column.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `share` | 147 | 55% |
| `opinion` | 51 | 19% |
| `question` | 37 | 14% |
| `vent` | 31 | 12% |
| **Total** | 266 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

*(Drafted during AI pre-labeling; every hard call is also written in that row's `note` column in labels.csv.)*

**1.**
> *The post:* "I am confident we are going to beat Liverpool! 🩵"
>
> *Could have been:* `vent` or `opinion`
>
> *I chose, because:* `opinion`. The AI pre-labeled it `vent` because it reads like pre-match hype, but I changed it. "We are going to beat Liverpool" is a claim about the club that someone could argue against, and my rule says an arguable claim makes a post `opinion` even when the tone is emotional.

**2.**
> *The post:* "Why is leaving a club a billion dollars in debt like United okay but investing in your club isn't? Anybody explain that to me?"
>
> *Could have been:* `question` or `opinion`
>
> *I chose, because:* `opinion`. The question is rhetorical: the poster isn't looking for an answer. It carries an arguable claim that critics of City's spending apply a double standard, so under my rule it is `opinion`, not `question`.

**3.**
> *The post:* "[BBC] worried about Man City being in next season's Champions League. BBC Sport has been told that there is no automatic mechanism to remove City from a European competition they qualify for on sporting merit. Even the Beeb is this biased..."
>
> *Could have been:* `share` or `opinion`
>
> *I chose, because:* `share`. Almost all of the post is the BBC news, with a one-line jab at the end. "Biased" is arguable, but it's aimed at the media rather than a player, the manager or the club, and it isn't the point of the post.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42. Trained on **cpu** (no GPU), torch 2.14.1+cpu.

**Anything I changed from the defaults, and why:** Nothing; all defaults.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

train 186 · val 40 · test 40 (stratified 70/15/15 by the notebook)

| Label | train | val | test |
|---|---|---|---|
| `share` | 103 | 22 | 22 |
| `question` | 26 | 6 | 5 |
| `vent` | 22 | 4 | 5 |
| `opinion` | 35 | 8 | 8 |

`question` and `vent` have only 5 test examples each (under ~8), so their F1 will swing a lot between seeds.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I had Claude pre-label rows 21–266 in labels.csv using my four labels and the decision rules in my README. I also asked it to leave a short reason in the note column whenever a post could fit two labels.
- *What came back:* It labeled all 246 rows: 131 share, 42 opinion, 40 vent, and 33 question. It marked 49 of them as "hard" and gave a one-line reason for each.
- *What I changed:* I went through every row and changed 12 labels. Nine of those were posts it called `vent` that I moved, mostly to `opinion`. The AI kept treating sarcasm and rhetorical complaints as pure emotion. But a post like the satirical "Official Guidelines for Conducting Yourself as a Manchester City Supporter," or "According to VAR Bruno does nothing to Foden...," still makes a point you could argue with (rival fans are hypocrites, the VAR call was wrong). By my own rule, that makes them `opinion`. I also moved "Congrats to Semenyo and his new wife" from `vent` to `share`, since it's club news and has nothing to do with frustration.

**Moment 2**

- *What I asked for:* After I wrote my five criteria, I asked Claude whether someone else could check each one without having to ask me what I meant. I told it not to suggest different numbers.
- *What came back:* It said criteria 1–4 were clear enough. Criterion 5, the one about agreeing with a second labeler, had three gaps. It didn't say how the 20 hard posts would be chosen out of the 49, whether cold rows could be included, or which rules the second person would follow.
- *What I changed:* I rewrote criterion 5 myself. The 20 posts are now picked at random with seed 42 from rows whose note contains "hard:", cold rows can be included, and the second labeler only gets the definitions in my README, not my labels or notes. I kept the 80% target.

**Pre-labelling disclosure:** AI pre-labeled the batch and I reviewed and corrected every row; the first 20 rows were labeled cold (by hand, before seeing any AI labels).

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
