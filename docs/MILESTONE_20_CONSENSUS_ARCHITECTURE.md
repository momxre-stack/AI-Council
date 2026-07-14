# AI Council — Milestone #20

## Consensus Architecture Characterization

---

# Verified Baseline

Repository baseline verified before beginning this milestone.

Observed baseline:

* Branch: `main`
* Working tree: clean
* `origin/main` synchronized
* `217 / 217` tests passing
* Current HEAD:
  `458d9e9 — Complete Milestone #19 Council result contract characterization`

No production behavior had been modified before this investigation began.

---

# Milestone Objective

The purpose of this milestone is to determine what the term **Consensus** currently means within the AI Council architecture.

This investigation is limited to architectural characterization.

No production implementation, API redesign, answer-selection policy, or behavioral changes are performed during this milestone.

The investigation separates:

* mission terminology;
* architecture terminology;
* production behavior;
* runtime artifacts;
* judge behavior;
* debate behavior;
* Council behavior;
* reliability behavior;
* historical architectural intent.

The objective is to characterize the current repository rather than define future architecture.

---

# Inspection Scope

The investigation inspected only the repository components required to characterize the architectural meaning of Consensus.

Primary inspection included:

* README.md
* docs/PROJECT_STATE.md
* docs/ROADMAP.md
* docs/MILESTONE_18_EXECUTION_PATH_EVIDENCE_AUDIT.md
* docs/MILESTONE_19_COUNCIL_RESULT_CONTRACT.md
* agent/council.py
* agent/dual_judge.py
* agent/judge_v2.py
* agent/debate.py
* web.py
* tests/test_council.py
* tests/test_debate.py
* tests/test_stress_metrics.py

Repository inspection remained intentionally bounded.

No production implementation was modified.

No new tests were introduced.

---

# Commands Executed

Repository baseline:

```cmd
git status
python -m pytest
git log --oneline -5

findstr /S /N /I ^
 /C:"consensus" ^
 /C:"final_answer" ^
 /C:"final answer" ^
 /C:"agreement" ^
 /C:"decision" ^
 /C:"more_complete_response" ^
 *.py docs\*.md README.md

type README.md
type docs\PROJECT_STATE.md
type docs\ROADMAP.md
type agent\council.py
type agent\dual_judge.py
type agent\judge_v2.py
type agent\debate.py
type web.py
type tests\test_council.py
type tests\test_debate.py
type tests\test_stress_metrics.py

# Terminology Inventory

The repository uses several related terms throughout documentation, prompts, runtime structures, and production code.

Static inspection shows that these terms are not automatically interchangeable.

Each occurrence must therefore be evaluated within its own architectural context.

| Term | Primary Context | Initial Classification |
|------|-----------------|------------------------|
| Consensus | Mission and architecture wording | Conceptual architectural term |
| Consensus answer | Architecture documentation and debate output | Conceptual term and runtime field |
| final_answer | Judge output | Runtime field |
| more_complete_response | Judge output | Decision field |
| agreement_score | Judge output | Diagnostic measurement |
| final_needs_debate | Dual Judge | Production decision |
| provider_only_final_needs_debate | Dual Judge | Diagnostic shadow decision |
| agreement_rate | Reliability assessment | Measurement |
| status | Council result | Production execution state |
| degraded_reason | Council result | Production diagnostic |

Observed:

* Multiple repository components use the word "Consensus".
* The term appears in both documentation and runtime structures.
* Different components associate Consensus with different artifacts.
* Static inspection alone does not justify treating these meanings as identical.
* No repository evidence currently establishes that every occurrence of "Consensus" refers to one architectural concept.

# Mission-Level Consensus

## Observed

The repository mission consistently describes AI Council as a multi-model decision system intended to produce more reliable answers than a single-model workflow.

Project documentation repeatedly presents the long-term architecture as:

Question

↓

Multiple Providers

↓

Multiple Judges

↓

Debate

↓

Consensus Answer

↓

Reliability Measurement

↓

Reliability Trends

↓

Historical Analytics

↓

Reliable AI Council

This wording appears in project documentation, including `PROJECT_STATE.md` and `ROADMAP.md`.

The README describes AI Council as a "Multi-model AI debate agent" but does not define the meaning of Consensus.

## Measured

Static repository inspection consistently shows that the project mission is consensus-oriented.

No conflicting mission statement describing AI Council as a provider-selection system or a single-provider workflow was identified.

## Inferred

At the mission level, "Consensus" represents an architectural objective rather than a verified runtime contract.

The documentation establishes that Consensus is part of the intended system vision, but it does not specify:

* which runtime component owns Consensus;
* which field represents Consensus;
* whether Consensus always exists;
* whether Consensus exists only after debate;
* whether Consensus is required on every successful execution path.

Therefore, mission terminology alone does not establish production semantics.

# Architecture-Level Consensus

## Observed

The architectural documentation consistently presents Consensus as a distinct stage within the overall AI Council pipeline.

Current project documentation describes the high-level architecture as:

Question

↓

Multiple Providers

↓

Multiple Judges

↓

Debate

↓

Consensus Answer

↓

Reliability Assessment

↓

Historical Reliability Analysis

Consensus is therefore positioned as an architectural stage that follows debate and precedes reliability assessment.

Repository documentation consistently treats Consensus as part of the intended architecture rather than an optional concept.

## Measured

Static inspection identified no architecture document that formally defines:

* the producer responsible for Council-level Consensus;
* the consumer responsible for Council-level Consensus;
* the runtime object representing Council-level Consensus;
* the behavior when debate is skipped;
* the behavior when debate fails;
* whether Consensus is required for every successful Council execution.

No architecture document establishes a field-level contract connecting the architectural "Consensus Answer" stage to a specific runtime result.

## Inferred

At the architectural level, Consensus currently functions as a conceptual stage within the overall Council pipeline.

The repository documents where Consensus belongs in the architecture but does not formally define how that architectural stage is materialized within the production result returned by `ask_council()`.

The architectural pipeline is therefore more specific than the mission statement but still stops short of defining a production-level Consensus contract.

# Production-Level Consensus

## Observed

The production implementation is centered around the `ask_council()` function.

Successful execution returns a structured result containing multiple artifacts, including:

* provider responses;
* judgment results;
* debate results (when executed);
* reliability assessment;
* semantic validation;
* execution status;
* degraded metadata.

Static inspection confirms that `ask_council()` does not produce:

* a top-level `final_answer`;
* a top-level `consensus_answer`;
* a top-level `council_answer`.

The production result therefore remains a structured multi-artifact object.

## Measured

Repository inspection confirms that:

* provider responses are always returned on successful execution;
* judgment results are returned after successful judging;
* debate results are returned only when debate executes successfully;
* reliability assessment is generated independently of answer selection;
* semantic validation records diagnostic measurements rather than selecting an answer.

No production logic promotes any nested answer-like field into a single authoritative Council answer.

## Inferred

The production implementation currently exposes the outputs generated by individual architectural stages rather than materializing one Council-level Consensus artifact.

The runtime contract therefore represents the execution pipeline as multiple observable artifacts instead of one authoritative production answer.

This behavior is consistent across both successful and degraded execution paths inspected during this milestone.

# Judge-Level Consensus

## Observed

Each provider-based judge is instructed to return a structured JSON object containing:

* `agreement_score`
* `needs_debate`
* `agreements`
* `differences`
* `more_complete_response`
* `final_answer`

The Independent Judge produces a structurally similar result, including the same answer-related fields.

The Dual Judge combines the outputs of all judges to produce production decision fields including:

* `debate_vote_count`
* `provider_debate_vote_count`
* `independent_debate_vote`
* `final_needs_debate`
* `provider_only_final_needs_debate`

The production decision is therefore derived from judge votes and disagreement rules rather than from any judge's `final_answer`.

## Measured

Repository inspection shows that:

* every provider judge may generate a `final_answer`;
* every provider judge may identify a `more_complete_response`;
* these fields remain nested within the corresponding judge output;
* `run_dual_judgment()` does not compare competing `final_answer` values;
* `run_dual_judgment()` does not select one judge's answer as the Council answer;
* `run_dual_judgment()` uses only debate-vote signals and disagreement rules when determining whether debate should occur.

No production evidence shows that a judge `final_answer` becomes authoritative after it is generated.

## Inferred

Within the current architecture, judge `final_answer` fields are answer-generation artifacts rather than production result artifacts.

Judge decisions influence whether additional review is required, but they do not determine which textual answer the Council ultimately returns.

The judge layer therefore produces both:

* answer-like artifacts (`final_answer`);
* decision artifacts (`needs_debate`, `more_complete_response`, `agreement_score`);

Only the decision artifacts participate directly in the observed production decision process.

# Debate-Level Consensus

## Observed

The debate stage is the only production component that explicitly creates a runtime field named `consensus_answer`.

The `run_debate()` function requests a structured result containing:

* `gemini_strengths`;
* `deepseek_strengths`;
* `criticisms`;
* `consensus_answer`.

The debate prompt defines `consensus_answer` as a text that combines the strongest parts of both provider responses into one final answer.

The field is produced only when:

* both provider responses are available;
* judgment completes successfully;
* `judgment["final_needs_debate"]` is `True`;
* debate execution succeeds;
* debate output passes structural validation.

## Measured

Repository tests confirm that `consensus_answer`:

* must exist in the debate result;
* must be a string;
* must not be empty;
* must satisfy the configured minimum length;
* is trimmed before being returned;
* is rejected when malformed, missing, incorrectly typed, or too short.

The tests validate the structural integrity of the field.

They do not validate:

* factual correctness;
* semantic completeness;
* improvement over provider responses;
* consistency with judge conclusions;
* agreement with the original question;
* authority as the final Council answer.

Static inspection also confirms that:

* `ask_council()` stores the field only inside the nested `debate` object;
* `ask_council()` does not promote it to a top-level result field;
* the Web interface does not display it;
* stress metrics treat debate presence as an execution signal rather than evaluating answer content;
* no downstream selector marks it as authoritative.

## Inferred

At the debate level, Consensus has its clearest concrete runtime meaning.

It represents a debate-generated synthesized answer produced after the system determines that additional review is required.

However, repository evidence supports only the following narrow interpretation:

> `debate["consensus_answer"]` is the structured textual output of a successful debate stage.

Repository evidence does not establish that this field is equivalent to Council-level Consensus.

It is therefore a debate artifact with answer-like semantics, but without explicit Council-level authority.

The field is conditional rather than universal because it does not exist on successful no-debate paths and may be absent on degraded debate paths.

# No-Debate Consensus Behavior

## Observed

When `judgment["final_needs_debate"]` is `False`, the Council completes successfully without executing the debate stage.

In this execution path:

* provider responses are returned;
* judgment artifacts are returned;
* reliability assessment is produced;
* semantic validation is produced;
* no debate object is created;
* no `debate["consensus_answer"]` exists.

No additional Council component generates an alternative Consensus artifact for this execution path.

## Measured

Static inspection identified no production logic that:

* synthesizes provider responses when debate is skipped;
* selects one provider response as the Council answer;
* selects one judge `final_answer`;
* promotes `more_complete_response` into an answer;
* creates a substitute for `debate["consensus_answer"]`.

Repository tests also do not assert the existence of a no-debate Consensus artifact.

## Inferred

Repository evidence demonstrates that successful execution does not require a materialized Consensus answer.

Instead, the Council returns the available execution artifacts without creating an additional answer-level object.

Whether the absence of debate should itself be interpreted as Consensus cannot be determined from the current repository evidence.

Likewise, repository evidence does not support the opposite conclusion that no-debate execution implies the absence of Consensus.

The architectural meaning of Consensus on successful no-debate execution therefore remains unspecified.

# Degraded Consensus Behavior

## Observed

The Council supports multiple degraded execution paths, including:

* provider failure;
* judge failure;
* debate failure.

Depending on the failure point, the returned result may still contain usable execution artifacts.

For example:

* provider responses may be available when only one provider fails;
* judgment results may be available when debate fails;
* reliability metadata and execution status continue to describe the execution outcome.

No degraded execution path introduces a dedicated Council-level Consensus artifact.

## Measured

Repository inspection confirms that:

* provider failures prevent successful judgment and debate execution;
* judge failures prevent debate execution;
* debate failures preserve completed judgment results but omit debate output;
* no degraded path generates a replacement `consensus_answer`;
* no degraded path promotes another answer-like field into an authoritative Council answer.

Repository tests verify degraded execution behavior and returned artifacts, but do not establish an alternative Consensus contract.

## Inferred

The degraded execution model is designed to preserve as much useful information as possible while accurately reporting execution failures.

Repository evidence therefore distinguishes between:

* usable execution artifacts;
* successful execution;
* answer-level synthesis;
* execution degradation.

The current repository does not define how Consensus should be represented when execution becomes degraded.

Accordingly, degraded execution preserves observability rather than materializing a fallback Consensus.

# Reliability and Measurement Alignment

## Observed

The repository includes multiple reliability and measurement components, including:

* reliability assessment;
* semantic validation;
* stress metrics;
* historical reliability analysis.

These components measure various aspects of execution, including:

* provider success and failure;
* degraded execution;
* debate usage;
* debate success and failure;
* judge agreement and disagreement;
* debate vote counts;
* agreement rates;
* semantic validation metrics.

## Measured

Static inspection shows that the current measurement infrastructure records execution and decision-related signals rather than answer-selection outcomes.

Repository evidence confirms measurement of:

* execution status;
* debate occurrence;
* debate completion;
* provider agreement metrics;
* judge agreement metrics;
* reliability indicators.

Repository inspection did not identify measurement of:

* correctness of a selected Council answer;
* quality of a selected Consensus answer;
* consistency of a selected Consensus answer across consumers;
* semantic quality of `debate["consensus_answer"]`;
* successful materialization of a Council-level Consensus artifact.

## Inferred

The current measurement framework evaluates how the Council executes rather than whether it successfully produces a unified Consensus answer.

Consequently, repository evidence supports the conclusion that execution reliability and Consensus semantics are currently separate architectural concerns.

The existing measurement infrastructure is therefore capable of evaluating execution quality, but it does not objectively determine whether architectural Consensus has been achieved.

# Consensus Producer / Consumer Trace

| Producer / Source      | Artifact                           | Primary Meaning                     | Consumer                        | User Visible | Authority Evidence                                |
| ---------------------- | ---------------------------------- | ----------------------------------- | ------------------------------- | ------------ | ------------------------------------------------- |
| PROJECT_STATE.md       | Consensus answer                   | Architectural stage                 | Documentation                   | Yes          | Mission / architecture wording                    |
| ROADMAP.md             | Consensus Answer                   | Long-term architectural vision      | Documentation                   | Yes          | Mission / architecture wording                    |
| Provider Judges        | `final_answer`                     | Judge-generated combined answer     | Nested `judgment` object        | No           | No production selection observed                  |
| Provider Judges        | `more_complete_response`           | Comparative judgment                | Dual Judge                      | No           | Used only for debate decision                     |
| Provider Judges        | `agreement_score`                  | Agreement measurement               | Dual Judge, semantic validation | No           | Diagnostic measurement                            |
| Dual Judge             | `final_needs_debate`               | Production debate decision          | Council                         | No           | Production decision                               |
| Dual Judge             | `provider_only_final_needs_debate` | Shadow diagnostic decision          | Diagnostics                     | No           | Not used for production execution                 |
| Debate                 | `consensus_answer`                 | Debate-generated synthesized answer | Nested `debate` object          | No           | No Council-level promotion observed               |
| Council                | Structured result                  | Aggregated execution artifacts      | API / Web                       | Yes          | Multi-artifact production result                  |
| Reliability Assessment | `assessment`                       | Reliability evaluation              | Council result                  | Yes          | Post-decision measurement                         |
| Semantic Validation    | Validation record                  | Diagnostic measurements             | Council result                  | Yes          | Post-decision diagnostics                         |
| Web Interface          | Provider responses                 | Presentation layer                  | End user                        | Yes          | Displays provider responses rather than Consensus |

## Observed

Repository inspection identifies multiple producers of answer-like and decision-related artifacts.

Each producer has a clearly defined responsibility within the execution pipeline.

No inspected producer creates a Council-owned authoritative Consensus artifact.

No inspected consumer promotes an existing answer-like artifact into a Council-level Consensus after production execution.

## Measured

Producer and consumer relationships are traceable through static inspection and supported by repository tests.

The trace confirms that answer generation, decision making, reliability assessment, and presentation remain separate responsibilities within the current architecture.

## Inferred

Consensus currently exists across multiple architectural layers rather than as one universally consumed runtime artifact.

The producer/consumer trace therefore supports the conclusion that the repository contains multiple Consensus-related concepts, each with different responsibilities, but no single production contract unifying them.

# Observed Findings

Repository inspection established the following observations:

* The project mission consistently describes a consensus-oriented multi-model architecture.
* Architectural documentation presents Consensus as a distinct stage following Debate.
* Provider judges generate `final_answer` fields.
* Debate generates a `consensus_answer` field.
* The Council returns a structured multi-artifact result.
* The Council does not create a top-level `final_answer`.
* The Council does not create a top-level `consensus_answer`.
* The Council does not create a dedicated `council_answer`.
* The Web interface displays provider responses rather than a Consensus answer.
* Reliability and semantic validation operate as post-decision measurement layers.

No inspected production component explicitly materializes a Council-level Consensus artifact.

---

# Measured Findings

Repository inspection and existing automated tests demonstrate that:

* debate execution is governed by explicit production decision rules;
* debate output is structurally validated;
* judge outputs are structurally validated;
* degraded execution paths preserve observable artifacts where possible;
* stress metrics measure execution behavior, debate usage, and judge decisions;
* no repository test asserts the existence of an authoritative Council-level Consensus answer.

The current implementation therefore supports reproducible execution behavior without establishing a reproducible Council Consensus contract.

---

# Inferred Findings

The collected evidence supports several architectural interpretations.

Consensus exists at multiple layers of the repository:

* as a mission objective;
* as an architectural stage;
* as a debate-generated artifact;
* as answer-generation guidance for provider judges.

However, these meanings are not unified into one production-level definition.

The repository therefore distinguishes between:

* execution decisions;
* answer-generation artifacts;
* debate synthesis;
* reliability measurements;

without defining a single Council-owned Consensus artifact.

No repository evidence demonstrates that these meanings are intended to be identical.

---

# Recommended Findings

No production implementation changes are justified by this milestone alone.

Before any public result contract is implemented, the architecture should first explicitly define:

* whether Council-level Consensus is required;
* whether Consensus is always materialized;
* whether Debate Consensus is equivalent to Council Consensus;
* how successful no-debate execution represents Consensus;
* how degraded execution represents Consensus.

These questions require an explicit architectural decision rather than additional implementation.

# Final Classification

## Primary Classification

Repository evidence demonstrates that the term **Consensus** is currently used at multiple architectural levels with different meanings.

Observed repository usage includes:

* mission terminology;
* architectural pipeline terminology;
* judge output fields;
* debate output fields.

However, repository inspection did not identify a single production-level contract that unifies these meanings into one authoritative Council Consensus artifact.

## Architectural Classification

Current repository evidence supports the following characterization:

* Mission-level Consensus: **Specified**
* Architecture-level Consensus: **Specified**
* Judge-level Consensus: **Partially Specified**
* Debate-level Consensus: **Specified**
* Council-level Consensus: **Not Explicitly Specified**
* Production Consensus Contract: **Not Explicitly Specified**

## Evidence Assessment

The investigation found positive evidence for:

* the existence of multiple Consensus-related concepts;
* well-defined debate synthesis;
* well-defined judge-generated answer artifacts;
* well-defined production execution behavior.

The investigation did not find sufficient evidence to conclude that:

* judge `final_answer`;
* debate `consensus_answer`; or
* any other runtime artifact

constitutes the authoritative Council Consensus.

Accordingly, repository evidence is sufficient to characterize the current architecture but insufficient to establish a unified production Consensus contract.

# Final Outcome

Milestone #20 successfully characterized the architectural meaning of Consensus within the current AI Council repository.

The investigation established that Consensus is consistently present as an architectural concept but currently exists through multiple related artifacts rather than one explicitly defined production contract.

No production implementation changes were required.

No production behavior was modified.

The repository remained stable throughout the investigation.

---

# Explicit Exclusions

This milestone did not:

* modify production code;
* modify production behavior;
* redesign the Council result contract;
* introduce a Council answer-selection mechanism;
* redefine Debate;
* redefine Judge responsibilities;
* change reliability measurements;
* recommend a specific implementation strategy.

Its purpose was limited to architectural characterization.

---

# Reconsideration Criteria

The conclusions of this milestone should be reconsidered only if future repository evidence introduces:

* an explicit Council-level Consensus contract;
* a Council-owned authoritative answer artifact;
* new production consumers of Consensus;
* architectural documentation defining Consensus semantics more precisely;
* production behavior materially changing the current execution model.

Until such evidence exists, this characterization represents the repository's current observable architecture.

