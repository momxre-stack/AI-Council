# AI Council — Milestone #17

## Next-Phase Evidence Review and Selection

### Status

Completed.

### Outcome

Outcome B — Insufficient Evidence for Immediate Production Implementation.

---

## Purpose

Milestone #17 evaluated the next possible AI Council engineering directions using the same evidence standard.

The milestone did not assume that an older roadmap item should automatically become the next implementation milestone.

Each candidate was evaluated using:

* repository inspection;
* current documentation;
* existing tests;
* measured project evidence;
* implementation complexity;
* architectural risk;
* expected reliability value;
* missing evidence;
* smallest safe next step.

No production code was changed during this milestone.

---

## Verified Baseline

At the beginning of Milestone #17:

* `main` was clean;
* `origin/main` was synchronized;
* all commits were pushed;
* `217 / 217` tests passed;
* Gemini REST provider was stable;
* DeepSeek provider was stable;
* provider error and API key redaction were implemented;
* Dual Judge vote diagnostics were implemented;
* provider-only shadow debate decisions were implemented;
* the provider-independent reasoning investigation was complete;
* the provider-independent reasoning Architecture Decision Record was accepted.

The repository remained stable throughout the review.

---

## Evidence Classification

### Observed

The current repository contains:

* Gemini and DeepSeek production Council execution;
* an OpenAI provider registered in the provider registry but not used by `ask_council()`;
* Council logic explicitly executing Gemini and DeepSeek;
* Dual Judge logic designed around two provider judges;
* provider, judge, and debate failure handling;
* degraded execution paths;
* provider error and API key redaction;
* stress execution;
* reliability scoring;
* reliability confidence;
* reliability trends;
* historical analytics;
* provider-only shadow debate diagnostics;
* a local web interface foundation.

### Measured

The verified test baseline is:

`217 / 217` passing tests.

No new benchmark, stress report, production failure pattern, or repeated operational defect was identified during Milestone #17 that independently justified immediate production implementation.

Previous provider-independent reasoning measurements remain valid, but they do not demonstrate a new implementation requirement for the candidates evaluated in this milestone.

### Inferred

The repository supports several possible future directions, but possibility alone does not establish priority.

Provider expansion would affect more than provider registration because the current Council and Dual Judge decision architecture is explicitly designed around two providers.

Automation may become useful, but no repeated manual workflow or unattended execution requirement has yet been measured.

Operational observability is already substantial, but no concrete diagnostic question has yet been shown to be unanswerable using current outputs.

Reliability and debate improvements remain important categories, but neither currently identifies one demonstrated defect narrow enough to justify implementation.

### Recommended

Do not begin a new production implementation milestone yet.

Preserve the stable baseline and perform a bounded evidence-collection milestone using existing infrastructure.

---

## Candidate A — Provider Expansion

### Current Evidence

The provider registry contains Gemini, DeepSeek, and OpenAI.

Production Council execution still uses only Gemini and DeepSeek.

Dual Judge behavior is explicitly designed around Gemini and DeepSeek judgments, two-provider winner comparison, two-provider score-gap comparison, and two-provider shadow voting.

### Missing Evidence

No current evidence demonstrates that two providers create a specific system reliability limitation.

No benchmark demonstrates that a third provider improves overall Council reliability.

No three-provider judge, consensus, or debate policy has been justified.

### Expected Benefit

A third provider could potentially improve diversity or resilience.

That benefit remains hypothetical under current evidence.

### Risks

Provider expansion could require changes to:

* Council execution;
* judge architecture;
* consensus rules;
* debate voting;
* reliability metrics;
* degraded behavior;
* tests;
* operational cost.

### Recommendation

Defer.

### Reconsideration Criteria

Reconsider provider expansion when:

* a reproducible two-provider reliability limitation is demonstrated;
* a third provider produces measured system-wide improvement;
* three-provider consensus and judge policies are defined before implementation;
* operational cost and failure handling are explicitly validated.

---

## Candidate B — CLI, Scheduler, or Automation

### Current Evidence

The repository already contains a stress CLI foundation and repeatable stress execution helpers.

No current evidence demonstrates a specific scheduling or unattended execution requirement.

### Missing Evidence

No measured repeated manual workflow, missed execution, duplicate-run issue, or unattended failure-handling requirement has been identified.

### Expected Benefit

Automation could reduce manual execution effort and improve consistency if a real recurring workflow exists.

### Risks

A combined CLI, scheduler, and automation milestone could create unnecessary operational complexity, configuration requirements, secret-handling risk, and maintenance burden.

### Recommendation

Defer.

### Reconsideration Criteria

Reconsider this candidate when:

* a repeated manual workflow is documented;
* its operational cost or reliability impact is measured;
* one independently useful component is selected;
* duplicate-run, persistence, failure, and secret-handling requirements are defined.

---

## Candidate C — Operational Observability

### Current Evidence

The repository already exposes:

* provider errors;
* quota classification;
* degraded reasons;
* judge results;
* debate decisions;
* vote diagnostics;
* provider-only shadow decisions;
* timing metrics;
* reliability summaries;
* reliability trends;
* historical reports.

### Missing Evidence

No concrete diagnostic question has been demonstrated that current outputs cannot answer.

### Expected Benefit

A narrow observability improvement could reduce diagnostic uncertainty if a specific blind spot is identified.

### Risks

Unjustified observability work could introduce dashboards, storage, tracing, or logging complexity without resolving a demonstrated problem.

### Recommendation

Gather more evidence first.

### Reconsideration Criteria

Reconsider this candidate when a concrete diagnostic question cannot be answered from existing data, such as:

* identifying a repeated provider failure cause;
* explaining production and shadow decision divergence;
* locating reliability degradation without manual reconstruction;
* distinguishing failure categories currently merged together.

---

## Candidate D — Reliability Quality Improvements

### Current Evidence

The repository already implements:

* provider retries;
* provider timeout handling;
* provider failure handling;
* judge failure handling;
* debate failure handling;
* degraded mode;
* JSON recovery;
* malformed output handling;
* quota-aware behavior;
* error redaction;
* reliability scoring;
* reliability confidence;
* reliability trends;
* historical analytics.

No specific unresolved reliability defect was demonstrated during this milestone.

### Missing Evidence

No reproducible example currently demonstrates:

* incorrect degraded classification;
* misleading reliability assessment;
* recurring unclassified failure;
* missing historical signal;
* incorrect production behavior;
* a reliability regression lacking test coverage.

### Expected Benefit

A narrow reliability fix could improve correctness and regression protection after a concrete defect is demonstrated.

### Risks

A broad reliability milestone could alter stable behavior, scoring semantics, historical comparability, or previously closed architectural decisions without sufficient evidence.

### Recommendation

Gather more evidence first.

### Reconsideration Criteria

Select a reliability implementation milestone only when:

* one concrete reliability failure is reproduced;
* the impact is measurable;
* current and expected behavior are clearly distinguishable;
* a narrow backward-compatible fix is possible;
* validation criteria exist before implementation.

---

## Candidate E — Debate Quality Improvements

### Current Evidence

Debate activation is controlled by:

* provider judge votes;
* Independent Judge vote;
* winner disagreement;
* significant score disagreement.

Debate output validation and debate failure handling already exist.

Debate usage and effectiveness metrics are already represented in the stress and reliability infrastructure.

No new debate defect was demonstrated during this milestone.

### Missing Evidence

No reproducible case currently shows:

* debate failing to activate when required;
* debate activating unnecessarily;
* debate worsening the final answer;
* debate effectiveness degrading over time;
* invalid debate output escaping current validation.

### Expected Benefit

A narrow debate fix could improve answer quality or decision accuracy after a specific failure is demonstrated.

### Risks

Prompt or logic changes without measured evidence could encode subjective preferences, alter historical comparability, and destabilize currently tested behavior.

### Recommendation

Gather more evidence first.

### Reconsideration Criteria

Reconsider debate changes when a repeatable debate failure is observed and an objective before-and-after validation can be defined.

---

## Candidate F — No Immediate Implementation

### Current Evidence

The repository is stable.

All tests pass.

Existing reliability, stress, historical, failure-handling, and diagnostic infrastructure is substantial.

No candidate currently has both:

* a demonstrated concrete problem;
* a justified narrow production implementation.

### Expected Benefit

Selecting no immediate implementation protects:

* production stability;
* backward compatibility;
* historical metric comparability;
* architectural simplicity;
* the evidence-first engineering process.

### Risk

A real problem could remain undiscovered if the project stops collecting operational evidence.

Therefore, this outcome must lead to a bounded measurement milestone rather than indefinite inactivity.

### Recommendation

Outcome B is selected because no implementation candidate currently satisfies the project's evidence standard.

---

## Final Decision

Milestone #17 selects:

**Outcome B — Insufficient Evidence for Immediate Production Implementation**

This decision is based on the strongest currently available repository inspection and measured evidence rather than the historical roadmap ordering.

No production feature milestone is currently justified by the strongest available evidence.

The next milestone should collect operational reliability evidence using existing infrastructure.

It must not assume that a defect exists.

It must attempt to determine whether a reproducible reliability, observability, provider, or debate limitation can be demonstrated.

---

## Recommended Next Milestone

### Milestone #18 — Operational Reliability Evidence Collection

### Goal

Use existing stress, reliability, historical, and shadow-decision infrastructure to identify whether one reproducible system-level reliability problem currently exists.

### Scope

The milestone may:

* run existing real stress tests;
* save existing reports;
* inspect reliability summaries;
* inspect timing results;
* inspect degraded outcomes;
* inspect provider failures;
* inspect judge and debate decisions;
* inspect provider-only shadow decision differences;
* compare repeated runs;
* document recurring patterns.

### Explicit Exclusions

Do not:

* modify Council;
* modify Dual Judge;
* modify Debate;
* modify Independent Judge;
* modify providers;
* add providers;
* change thresholds;
* change prompts;
* change reliability formulas;
* add a scheduler;
* add a dashboard;
* add a database;
* add runtime dependencies;
* reopen provider-independent semantic reasoning;
* implement a fix before reproducing a concrete defect.

### Validation Criteria

Milestone #18 must end with one of two results.

#### Result A — Reproducible Problem Found

Document:

* exact input or conditions;
* observed behavior;
* expected behavior;
* reproduction steps;
* frequency;
* reliability impact;
* smallest safe implementation scope;
* regression test requirements;
* stop conditions.

#### Result B — No Reproducible Problem Found

Document:

* tests and measurements performed;
* evidence collected;
* why no implementation is justified;
* which uncertainties remain;
* whether another measurement step is justified.

### Stop Conditions

Stop immediately if:

* the work begins changing production behavior;
* the scope expands into multiple unrelated problems;
* conclusions depend only on one isolated non-reproducible result;
* provider-independent semantic reasoning is restarted;
* a preferred implementation is selected before evidence is collected.

---

## Milestone #17 Closeout Criteria

Milestone #17 is complete when:

* this decision document is reviewed;
* production behavior remains unchanged;
* all tests remain green;
* the working tree is clean after the approved documentation commit;
* the documentation commit is pushed;
* Milestone #18 begins from the recorded decision rather than from an assumed feature priority.

---

## Final Principle

The project will not change stable production architecture merely because a possible improvement exists.

The next implementation will begin only after a concrete problem is demonstrated and the smallest safe solution is defined.

პატარა ნაბიჯებით დიდი მიზნისკენ.
