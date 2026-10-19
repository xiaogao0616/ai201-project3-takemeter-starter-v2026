# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

The classifier must achieve at least 75% accuracy on the held-out test set for each of the three seeds.



**Why this number:**
My dataset has 266 posts, including 147 labeled share. Predicting share for everything would already achieve about 55% accuracy, so 75% requires a meaningful improvement over that baseline while allowing some mistakes on sarcastic and mixed-purpose posts.


---

## 2.

The classifier must achieve a macro-F1 of at least 0.65 on the held-out test set for each of the three seeds.



**Why this number:**
share accounts for more than half of my dataset, while vent has only 31 examples. A macro-F1 target of 0.65 requires useful performance across all four labels rather than allowing the largest label to dominate the result.


---

## 3.

The question label must achieve an F1 of at least 0.60 on the held-out test set for each of the three seeds.



**Why this number:**
I have only 37 question posts, so a 15% test split would contain roughly six of them. A few mistakes could change the score substantially, especially because genuine requests for answers must be distinguished from rhetorical questions expressing opinions or complaints.


---

## 4.

The classifier must achieve an F1 of at least 0.60 for opinion and 0.50 for vent on the held-out test set for each of the three seeds.



**Why this number:**
The distinction depends on whether a post contains an arguable claim, not whether it sounds angry or sarcastic. I have 51 opinion posts but only 31 vent posts, so I set a lower minimum for vent because its test score will be especially sensitive to individual mistakes across seeds.


---

## 5.

A second person must independently label 40 posts, including 20 marked as hard and 20 randomly selected from the remaining posts. Our labels must agree on at least 80% of those posts before discussing disagreements.



**Why this number:**
Half the sample deliberately tests difficult boundaries, including sarcasm, rhetorical questions, and news with added judgments. Agreement on at least 32 of 40 posts would provide evidence that my labeling rules are understandable and repeatable beyond the easiest examples.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
