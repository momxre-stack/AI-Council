# AI Council Dissent Auditor

## Milestone #16.13 — Diagnostic Contract Characterization

## Status

Design only.

No production behavior changes are included in this milestone.

---

## Purpose

The Dissent Auditor is a narrow architectural hypothesis.

Its purpose is not to replace the Independent Judge, become another judge, or make debate decisions.

Its purpose is to investigate whether strong dissent can be explained by concrete, auditable evidence.

The core question is:

Can a small diagnostic layer distinguish useful dissent from unsupported disagreement without becoming a semantic engine?

---

## Current Evidence

The current Independent Judge is deterministic, reproducible, provider-independent, and strongly lexical.

It can produce low agreement scores for semantically aligned answers.

Current benchmark examples produce agreement scores of:

* 29
* 27
* 32

These low scores are useful dissent signals, but they are not evidence that debate is necessary.

The current Semantic Validation layer already measures score gaps.

The current Dual Judge already contains:

* debate vote protection
* winner disagreement protection
* significant score-gap protection

The Dissent Auditor must not duplicate these mechanisms.

---

## Existing Differences Contract

The provider-based judges currently return:

* agreement_score
* needs_debate
* agreements
* differences
* more_complete_response
* final_answer

Historical inspection confirmed that `differences` was introduced with only this requirement:

`differences must be a list of short strings.`

The same loose requirement was later preserved for the DeepSeek Judge.

No repository evidence was found requiring `differences` to identify:

* a concrete contradictory claim
* the affected response
* a missed mandatory requirement
* a factual conflict
* a material omission
* a required format failure
* supporting excerpts
* severity
* confidence
* a machine-readable evidence type

Current tests also do not characterize the meaning or quality of non-empty `differences`.

Therefore:

The existing `differences` field may be useful as an explanatory hint.

It must not be treated as authoritative Dissent Auditor evidence.

---

## Diagnostic Boundary

A future Dissent Auditor must not answer:

“Is the score gap large?”

That question is already covered by Semantic Validation and Dual Judge protections.

A future Dissent Auditor may only investigate:

“Is there concrete, auditable evidence that explains the dissent?”

Potential evidence categories may include:

* direct contradiction
* missed mandatory requirement
* factual conflict
* material omission
* required format failure

These categories are not yet an implementation contract.

They are only candidate diagnostic categories that require evidence and validation.

---

## Authority Boundary

The Dissent Auditor has no production authority.

It must not:

* trigger debate
* cancel debate
* change vote counts
* override provider judges
* change score thresholds
* replace the Independent Judge
* become a third LLM judge

Any future authority must be earned through measured evidence.

---

## Current Conclusion

The existing `differences` field is not sufficiently defined to serve as authoritative Dissent Auditor input.

The next question is not how to implement a Dissent Auditor.

The next question is:

What is the smallest diagnostic evidence contract that can be objectively tested without changing production behavior?

If no small contract can demonstrate unique value, Dissent Auditor work should stop.

---

## Stop Conditions

Stop this direction if:

* useful auditing requires broad semantic understanding
* deterministic rules repeat the current lexical false-positive problem
* the design grows into dictionaries or special cases
* the auditor duplicates existing score-gap protections
* no objective benchmark can measure unique value
* the diagnostic layer cannot demonstrate value without decision authority

A negative result is acceptable.

The goal is not to save the Independent Judge.

The goal is to improve AI Council reliability.

---

## Diagnostic Benchmark Candidates

Before defining a diagnostic evidence contract, the Dissent Auditor direction should be tested against a small set of human-reviewed cases.

The purpose of these cases is not to prove an implementation.

The purpose is to determine whether useful dissent evidence can be defined narrowly and measured objectively.

Initial candidate case types:

### 1. Unsupported Lexical Dissent

Two responses express substantially the same answer using different wording.

The current Independent Judge may produce a low agreement score.

Expected diagnostic question:

Is there any concrete disagreement evidence beyond low lexical overlap?

Expected human assessment:

No concrete evidence.

This case should protect against treating a low score as proof of disagreement.

### 2. Direct Contradiction

Two responses make materially incompatible claims about the same relevant point.

Expected diagnostic question:

Can the conflicting claims be identified directly and specifically?

Expected human assessment:

Concrete contradiction evidence exists.

This case should test whether useful dissent can be tied to an explicit conflict rather than a general score.

### 3. Missed Mandatory Requirement

The question contains an explicit requirement or constraint, and one response fails to satisfy it.

Expected diagnostic question:

Can the missed requirement and affected response be identified?

Expected human assessment:

Concrete requirement-failure evidence exists.

This case should distinguish question-grounded failure from general answer differences.

### 4. Material Omission

One response omits information that is necessary to answer the core question, while the other addresses it.

Expected diagnostic question:

Can the necessary missing element be identified without requiring broad semantic judgment?

Expected human assessment:

Potential omission evidence exists.

This case is intentionally uncertain.

If material omission cannot be defined or evaluated narrowly, it should be removed from the first diagnostic benchmark.

---

These candidate cases do not define the final Dissent Auditor contract.

They do not grant authority.

They do not justify production implementation.

The next step is to determine whether each case can be expressed with:

* a clear human-reviewed expected result
* concrete evidence
* reproducible evaluation
* no dependence on score-gap duplication
* no open-ended semantic reasoning

Any case that fails these requirements should be removed rather than expanded with special rules.

---

## Guiding Principle

Dissent is a signal.

A low score is not evidence.

Authority must follow measured reliability, not architectural intention.

პატარა ნაბიჯებით დიდი მიზნისკენ.
