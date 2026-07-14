# AI Council

# Milestone #19

## Council Result Contract Characterization

Status:

Completed.

Implementation:

None.

Production behavior changes:

None.

Tests at verified baseline:

217/217 passing.

---

## 1. Verified Baseline

Milestone #19 began from the following verified repository state:

* Branch: `main`
* Working tree: clean
* `origin/main`: synchronized
* Tests: 217/217 passing
* Milestone #18 completion commit present at `HEAD`

Verified commit:

`f5164c5 — Complete Milestone #18 execution path evidence audit`

Commands executed:

```cmd
git status
python -m pytest
git log --oneline -5
```

Observed baseline result:

* `main` was clean.
* `main` was synchronized with `origin/main`.
* All 217 tests passed.
* `f5164c5` was present at `HEAD`.

No files were modified before this baseline was confirmed.

---

## 2. Milestone Objective

The objective of Milestone #19 was to characterize the current AI Council result contract.

The investigation asked:

> Does AI Council currently function as a multi-artifact analysis system, a single-answer consensus system, or an incompletely specified combination of both?

This milestone was limited to contract characterization.

It did not attempt to:

* add a final-answer field;
* select a provider response;
* select a judge answer;
* change debate behavior;
* change the Web interface;
* change stress or reliability behavior;
* modify production code;
* modify tests.

---

## 3. Inspection Scope

The investigation used the smallest repository scope necessary to characterize the result contract.

Files directly inspected included:

```text
README.md
docs/PROJECT_STATE.md
docs/MILESTONE_18_EXECUTION_PATH_EVIDENCE_AUDIT.md

agent/council.py
agent/dual_judge.py
agent/debate.py
web.py

tests/test_council.py
```

Repository-wide symbol search was also used to locate consumers and tests referencing:

```text
ask_council(
final_answer
consensus_answer
```

Additional historical context was reviewed only to clarify whether the current result shape had previously been established as an intentional public contract.

No broad implementation exploration was performed.

---

## 4. Commands Executed

The following commands were used during the investigation:

```cmd
git status
python -m pytest
git log --oneline -5

type agent\council.py
type tests\test_council.py

findstr /S /N /I /C:"ask_council(" /C:"final_answer" /C:"consensus_answer" *.py

type agent\dual_judge.py
type agent\debate.py
type web.py

type README.md
type docs\PROJECT_STATE.md
type docs\MILESTONE_18_EXECUTION_PATH_EVIDENCE_AUDIT.md
```

No live provider execution was required.

No stress run was required.

Static repository inspection and existing deterministic tests were sufficient to characterize the implemented result shape.

---

## 5. Current Successful-Result Contract

### Observed

During a successful execution, `ask_council()` returns a dictionary containing:

```text
question
responses
provider_errors
quota_errors
status
degraded_reason
assessment
judgment
judgment_error
debate
debate_error
semantic_validation
```

The nested `responses` object contains exactly:

```text
responses.gemini
responses.deepseek
```

The `judgment` object contains the result returned by `run_dual_judgment()`.

That object includes:

```text
judgment.gemini_judge
judgment.deepseek_judge
judgment.independent_judge
judgment.debate_vote_count
judgment.provider_debate_vote_count
judgment.independent_debate_vote
judgment.final_needs_debate
judgment.provider_only_final_needs_debate
```

When debate is not required:

```text
debate = None
debate_error = None
status = "ok"
degraded_reason = None
```

When debate succeeds:

```text
debate = {
    "gemini_strengths": ...,
    "deepseek_strengths": ...,
    "criticisms": ...,
    "consensus_answer": ...,
}
debate_error = None
status = "ok"
degraded_reason = None
```

### Observed

The successful result does not contain a top-level:

```text
final_answer
consensus_answer
authoritative_answer
```

### Observed

`ask_council()` does not copy any nested judge `final_answer` or debate `consensus_answer` into a common result field.

### Inferred

A caller receiving a successful Council result must inspect and interpret nested artifacts directly.

The current implementation does not provide a single field that tells the caller which answer should be treated as the effective Council answer.

---

## 6. Degraded-Result Contracts

The result shape is not fully stable across every execution path.

### 6.1 One Provider Fails

When either Gemini or DeepSeek fails, returns an invalid type, or returns an empty response, `ask_council()` returns:

```text
question
responses
provider_errors
quota_errors
status
degraded_reason
assessment
judgment
judgment_error
debate
debate_error
```

Values include:

```text
status = "degraded"
degraded_reason = "provider_failure"
assessment = None
judgment = None
debate = None
```

The successful provider response remains available under:

```text
responses.gemini
```

or:

```text
responses.deepseek
```

### Observed

The remaining provider answer is usable as raw output.

### Observed

The result does not identify that remaining provider answer as authoritative.

### Observed

`semantic_validation` is not added on this early-return path.

---

### 6.2 Both Providers Fail

When both providers fail, `ask_council()` raises `RuntimeError`.

It does not return a structured degraded result.

### Observed

No usable answer remains.

### Observed

This execution path has a different external contract from the other degraded paths because it raises instead of returning a result dictionary.

---

### 6.3 Judgment Fails

When `run_dual_judgment()` raises an exception, `ask_council()` returns:

```text
status = "degraded"
degraded_reason = "judge_failure"
assessment = None
judgment = None
judgment_error = <error text>
debate = None
debate_error = None
```

Both provider responses remain present.

### Observed

Two usable provider artifacts remain.

### Observed

The result does not identify either provider response as the effective Council answer.

### Observed

No judge final answer or debate consensus is available.

### Observed

`semantic_validation` is not added on this early-return path.

---

### 6.4 Debate Fails

When judgment requires debate but `run_debate()` fails, `ask_council()` returns:

```text
status = "degraded"
degraded_reason = "debate_failure"
judgment = <completed judgment>
debate = None
debate_error = <error text>
assessment = <computed assessment>
semantic_validation = <computed validation>
```

Both provider responses and all completed judgment artifacts remain available.

### Observed

The result does not select one of those remaining artifacts as authoritative.

---

## 7. Field Producer and Consumer Trace

| Field                                       | Producer                                  | Meaning in current code                                        | Validation                                             | Known consumer                                                   | Consumed                                              | User-visible     | Authoritative                            |
| ------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------- | ---------------- | ---------------------------------------- |
| `responses.gemini`                          | Gemini provider through `ask_council()`   | Raw Gemini answer                                              | Must be a non-empty string                             | Web, tests, stress pipeline                                      | Yes                                                   | Yes, in Web      | No explicit evidence                     |
| `responses.deepseek`                        | DeepSeek provider through `ask_council()` | Raw DeepSeek answer                                            | Must be a non-empty string                             | Web, tests, stress pipeline                                      | Yes                                                   | Yes, in Web      | No explicit evidence                     |
| `judgment.gemini_judge.final_answer`        | Gemini-based judge                        | Judge-generated combined answer                                | Structured judge parsing                               | Returned inside judgment                                         | No downstream selection found                         | No               | No                                       |
| `judgment.deepseek_judge.final_answer`      | DeepSeek-based judge                      | Judge-generated combined answer                                | Structured judge parsing                               | Returned inside judgment                                         | No downstream selection found                         | No               | No                                       |
| `judgment.independent_judge.final_answer`   | Independent Judge                         | Present as an empty field in current deterministic output      | Deterministic implementation                           | Semantic diagnostics indirectly inspect scores, not final answer | No                                                    | No               | No                                       |
| `judgment.final_needs_debate`               | Dual Judge policy                         | Production debate decision                                     | Explicit vote, winner-disagreement and score-gap rules | `ask_council()`                                                  | Yes                                                   | Not directly     | Authoritative only for debate activation |
| `judgment.provider_only_final_needs_debate` | Dual Judge policy                         | Diagnostic shadow decision without Independent Judge authority | Explicit provider-only rules                           | Returned as diagnostic data                                      | No production decision use found                      | No               | No                                       |
| `debate.consensus_answer`                   | Debate stage                              | Debate-generated combined answer                               | Required, string, non-empty, minimum length            | Returned inside `debate`; stress data checks debate presence     | Structurally consumed, not selected as Council answer | No               | No explicit evidence                     |
| `assessment`                                | Reliability trends module                 | Reliability confidence and signals                             | Existing reliability logic and tests                   | Returned to callers                                              | Yes as metadata                                       | No               | Not an answer                            |
| `semantic_validation`                       | Semantic validation module                | Diagnostic comparison record                                   | Existing validation logic and tests                    | Returned to callers                                              | Yes as metadata                                       | No               | Not an answer                            |
| `status`                                    | `ask_council()`                           | Execution health state                                         | Existing tests                                         | Web, stress metrics, callers                                     | Yes                                                   | Yes              | Authoritative for execution status       |
| `degraded_reason`                           | `ask_council()`                           | Failure-stage classification                                   | Existing tests                                         | Web and callers                                                  | Yes                                                   | Yes when present | Authoritative for degradation reason     |

### Inferred

The repository contains several fields that are authoritative within narrow subcontracts:

* `final_needs_debate` is authoritative for deciding whether debate runs.
* `status` is authoritative for execution status.
* `degraded_reason` identifies the classified failure stage.

No repository evidence establishes an answer field as authoritative for the complete Council result.

---

## 8. No-Debate Result Behavior

When:

```text
judgment.final_needs_debate = False
```

the Council:

1. preserves both provider responses;
2. preserves all judge artifacts;
3. does not run debate;
4. sets `debate` to `None`;
5. computes reliability assessment;
6. computes semantic validation;
7. returns the structured result.

### Observed

Neither provider response is promoted to an authoritative answer.

### Observed

Neither judge `final_answer` is promoted to an authoritative answer.

### Observed

Judge `more_complete_response` may exist inside provider judge output, but `ask_council()` does not use it to select a response.

### Observed

No combined no-debate answer is created at the Council layer.

### Inferred

The current no-debate result behaves as a multi-artifact return object without an answer-selection contract.

---

## 9. Debate Result Behavior

When:

```text
judgment.final_needs_debate = True
```

the Council calls `run_debate()`.

A successful debate returns:

```text
gemini_strengths
deepseek_strengths
criticisms
consensus_answer
```

### Observed

`consensus_answer` is validated as a required, non-empty string.

### Observed

The debate prompt defines it as a combination of the strongest parts of both provider responses.

### Observed

After creation, `ask_council()` stores the complete debate object under:

```text
result["debate"]
```

### Observed

`debate["consensus_answer"]` is not:

* copied to a top-level result field;
* substituted for provider responses;
* displayed by the Web interface;
* identified through a Council-level answer-selection field.

### Inferred

Debate creates a semantically answer-like artifact, but the Council result contract does not establish that artifact as the public authoritative answer.

Its existence changes the returned result by adding a validated debate object and by influencing reliability metadata through `debate_used`.

It does not change the Council into a formally defined single-answer return contract.

---

## 10. Web Consumer Behavior

The `/ask` route calls `ask_council()` and displays:

```text
responses.gemini
responses.deepseek
status
degraded_reason
provider_errors
```

The page does not display:

```text
judgment.gemini_judge.final_answer
judgment.deepseek_judge.final_answer
judgment.independent_judge.final_answer
debate.consensus_answer
assessment
semantic_validation
```

### Observed

The Web interface presents provider answers separately.

### Observed

The page title is `Ask AI Council`, but the rendered answer area is explicitly divided into `Gemini` and `DeepSeek`.

### Observed

The page and home route describe the Web layer as:

```text
Web interface foundation
Ask page form foundation
```

### Inferred

The current Web interface is a foundation consumer of selected Council fields rather than evidence of a completed consensus-answer presentation contract.

### Recommended

Missing Web presentation should not be classified as a defect under Milestone #19 because current code and documentation explicitly characterize the Web layer as a foundation.

---

## 11. Stress and Measurement Behavior

Repository symbol search shows that stress tests and stress metrics commonly use results shaped like:

```text
{
    "status": "ok",
    "debate": {
        "consensus_answer": "final"
    }
}
```

### Observed

Current stress infrastructure recognizes successful execution status and the presence of debate output.

### Observed

Existing stress evidence does not establish that the semantic quality of `consensus_answer` is evaluated.

### Observed

No inspected evidence showed historical reports selecting, preserving, or comparing a single authoritative Council answer as a contract-level answer field.

### Inferred

Current stress and historical reliability systems primarily measure execution outcomes, failure behavior, debate use, and reliability signals.

They do not currently provide evidence that one nested answer is the official Council answer or that answer-selection quality is measured.

### Inferred

The current infrastructure cannot establish whether one answer-selection policy is more reliable than another without additional contract-specific quality criteria and measurements.

---

## 12. Documentation and Mission Alignment

`README.md` describes AI Council as:

```text
Multi-model AI debate agent.
```

This description does not define a result-field contract.

`docs/PROJECT_STATE.md` states that the project goal is:

> Build a robust multi-model decision system that produces more reliable answers than a single-model workflow.

It also describes the system as combining:

* multiple providers;
* independent evaluation;
* debate when justified;
* consensus generation;
* reliability measurement;
* historical reliability analysis.

Its conceptual flow includes:

```text
Debate when justified
↓
Consensus answer
↓
Reliability assessment
```

### Observed

The documentation describes a consensus-oriented architecture.

### Observed

The documentation does not define:

* the exact producer of the effective Council answer;
* the exact public field path;
* the no-debate answer-selection rule;
* the degraded answer-selection rule;
* whether callers should receive only one answer;
* whether the multi-artifact object is the final intentional public contract.

Milestone #18 recorded that the absence of a top-level authoritative answer was an architectural question, not a demonstrated reliability defect.

Historical architectural context confirmed that:

* consensus-oriented output was part of the project direction;
* the exact single-answer versus multi-artifact public result contract had not been formally decided;
* `Consensus answer` in project documentation was conceptual wording rather than a field-level guarantee.

### Inferred

The implemented system is currently multi-artifact in shape and consensus-oriented in mission.

The relationship between those two properties is incompletely specified.

---

## 13. Evidence Classification

### Observed

* `ask_council()` returns a structured result containing provider, judgment, debate, status, assessment, and validation artifacts.
* No top-level authoritative answer field exists.
* Judge components produce `final_answer` fields.
* Debate produces `consensus_answer`.
* No Council-level selection rule chooses among those answer-like fields.
* The no-debate path returns artifacts without answer selection.
* The debate path stores consensus only inside the debate object.
* Provider-failure and judge-failure paths preserve usable provider answers without marking one authoritative.
* Both-provider failure raises instead of returning a result object.
* The Web interface displays provider answers, status, degradation reason, and provider errors.
* Existing Council tests do not establish one authoritative answer field.
* Project documentation describes a consensus-oriented flow but does not define a precise field-level result contract.

### Measured

* The baseline test suite passed 217/217 tests.
* Existing deterministic tests verify successful, degraded, provider-failure, judge-failure, debate-failure, malformed-response, quota-error, and registry behavior.
* Existing tests confirm the current result behavior but do not test authoritative answer selection.

### Inferred

* The production implementation currently functions as a multi-artifact result system.
* The project mission remains consensus-oriented.
* Repository evidence does not prove that the multi-artifact shape is the intentionally finalized public contract.
* Repository evidence also does not prove that one authoritative answer is already an objectively required public contract.
* The current state is therefore an incompletely specified combination of multi-artifact implementation and consensus-oriented architectural intent.

### Recommended

* Preserve current production behavior.
* Do not add or select an authoritative answer during this milestone.
* Do not classify the absence of a top-level answer as a reproducible defect.
* Any future answer-selection work must begin with an explicit architecture decision defining the intended public result contract.
* That decision must define successful, no-debate, debate, provider-degraded, judge-degraded, debate-degraded, and total-failure behavior before implementation.

---

## 14. Contract Ambiguities

The following questions remain unspecified:

1. What exact field represents the effective Council answer?
2. Does the no-debate path require a combined answer?
3. Should one provider response be selected when judges agree?
4. Should one provider judge’s `final_answer` be preferred?
5. If provider judges produce different `final_answer` values, how should selection occur?
6. Is `debate["consensus_answer"]` authoritative when debate succeeds?
7. What is the effective answer when debate fails?
8. What is the effective answer when judgment fails but both provider responses remain?
9. What is the effective answer when only one provider succeeds?
10. Should all successful and degraded paths share one stable result shape?
11. Is the current multi-artifact object an internal diagnostic format, a public API contract, or both?
12. Should reliability assessment evaluate the selected answer rather than only execution signals?

These ambiguities are real but are not, by themselves, proof of a defect.

---

## 15. Reproducibility Findings

The following behavior is reproducible through source inspection and existing tests:

* successful execution returns structured artifacts without a top-level answer;
* no-debate execution does not select an answer;
* debate execution preserves consensus only inside the debate object;
* provider degradation leaves one answer available without authority metadata;
* judge degradation leaves two answers available without authority metadata;
* debate degradation leaves provider and judgment artifacts available without answer selection;
* both-provider failure raises an exception;
* Web output displays providers rather than consensus;
* tests do not define an authoritative result answer.

What is not reproducibly demonstrated:

* that current callers require one authoritative answer;
* that current callers interpret different nested fields inconsistently;
* that answer reliability is reduced by the existing result shape;
* that the project previously approved one mandatory answer-selection policy;
* that the current multi-artifact return was intentionally approved as the final public contract.

---

## 16. Reliability Impact

A stable result contract matters because callers should interpret equivalent executions consistently.

The current lack of an explicit answer-selection contract creates potential future risks:

* different consumers could select different nested answers;
* no-debate and debate paths could be interpreted differently;
* degraded paths could produce inconsistent fallback choices;
* reliability measurements could assess execution success without assessing the answer actually shown to users.

### Inferred

These are plausible architectural risks.

### Observed

No current repository evidence demonstrates that these risks have produced a concrete reliability failure.

### Recommended

Potential impact should not be converted into a production defect without an affected caller, a reproducible inconsistency, and an objectively defined expected answer-selection policy.

---

## 17. Final Contract Classification

# Classification D — Insufficient Evidence

Repository evidence is sufficient to describe the implemented result behavior but insufficient to establish the intended final public contract.

The evidence does not support Classification A because the repository does not explicitly establish the multi-artifact result as an intentional and final public contract.

The evidence does not support Classification B because no existing field or selection rule is established as the authoritative Council answer.

The evidence does not support Classification C because the project does not yet objectively define a mandatory single-answer public contract, affected callers are not shown to be failing, and no concrete answer-selection reliability defect has been reproduced.

The most accurate characterization is:

> AI Council currently implements a multi-artifact result object within a consensus-oriented architecture, but the exact public answer-selection contract remains incompletely specified.

---

## 18. Final Outcome

# Outcome B — No Contract Problem Demonstrated

Milestone #19 did not demonstrate a reproducible contract problem requiring production implementation.

The investigation established:

* the exact current result behavior;
* successful and degraded result differences;
* producer and consumer relationships;
* no-debate behavior;
* debate behavior;
* Web behavior;
* documentation alignment;
* remaining contract ambiguities.

The absence of a top-level authoritative answer is reproducible.

However, repository evidence does not establish an objective expected contract against which that behavior can be classified as a defect.

Production behavior should therefore remain unchanged.

---

## 19. Smallest Safe Next Milestone

A bounded follow-up milestone is justified only if the project chooses to resolve the open architectural question.

The smallest safe next milestone would be a documentation-only architecture decision:

```text
AI Council Public Result Contract Decision
```

Its goal would be to define, without implementation:

* whether the public contract is single-answer, multi-artifact, or both;
* the authoritative answer path during no-debate success;
* the authoritative answer path during debate success;
* fallback behavior for each degraded path;
* whether the existing result object remains backward-compatible;
* which consumer is the initial contract owner;
* what quality and reliability evidence would validate the chosen design.

No production implementation should begin until that decision is approved.

---

## 20. Explicit Exclusions

Milestone #19 did not:

* modify production code;
* modify existing tests;
* add future-behavior tests;
* add a top-level `final_answer`;
* add a top-level `consensus_answer`;
* select a judge answer;
* select a provider response;
* change debate output;
* change judge prompts;
* change Council result shape;
* change Web output;
* change stress metrics;
* change reliability formulas;
* modify Independent Judge;
* modify vote authority;
* add or remove providers;
* redesign the architecture;
* introduce compatibility adapters;
* implement a migration plan;
* commit runtime artifacts, logs, reports, caches, or secrets.

Only this documentation file is part of the Milestone #19 change.

---

## 21. Reconsideration Criteria

The classification should be reconsidered only if new evidence establishes one or more of the following:

* an approved public API contract requiring one authoritative answer;
* an existing caller that must select one answer but cannot do so consistently;
* contradictory consumer selection behavior;
* a reproducible user-facing reliability failure caused by answer ambiguity;
* historical design evidence explicitly approving the current multi-artifact contract;
* historical design evidence explicitly approving a single-answer contract;
* measured answer-quality differences between candidate selection policies;
* a formal requirement for stable successful and degraded result shapes.

Until such evidence exists, preserving current production behavior is the safest engineering decision.

---

## Final Conclusion

Milestone #19 successfully characterized the current AI Council result contract.

The implementation currently returns multiple structured artifacts rather than one explicitly authoritative Council answer.

The project remains conceptually consensus-oriented, but repository evidence does not define how that architectural goal maps to a stable public field-level contract.

No reproducible contract defect was demonstrated.

The final classification is:

**Classification D — Insufficient Evidence**

The final outcome is:

**Outcome B — No Contract Problem Demonstrated**

Production behavior remains unchanged.

პატარა ნაბიჯებით დიდი მიზნისკენ.
