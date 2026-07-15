# AI Council

## Milestone #21: Council Authoritative Answer Decision

**Status:** Final Architectural Decision

---

## Objective

Determine whether the AI Council architecture should define an authoritative Council answer, and if so, identify the most appropriate architectural contract while preserving reliability, observability, provenance, failure honesty, and backward compatibility.

This milestone is architecture-only.

No production code, public API, runtime behavior, or implementation is modified.

---

## Scope

This milestone evaluates architectural alternatives for Council answer authority.

It does not introduce implementation changes.

It does not modify provider behavior, judgment behavior, debate behavior, semantic validation, reliability assessment, or public interfaces.

Any implementation resulting from this decision is explicitly deferred to a future milestone.

---

## Verified Baseline

Repository baseline verified before investigation:

- Working tree clean.
- Branch synchronized with origin/main.
- 217 / 217 tests passing.
- No production changes introduced during this milestone.

The architectural baseline established by Milestones #18–#20 is treated as verified input for this decision.


## Candidate Evaluation

### Candidate A — Preserve Multi-Artifact Contract


Observed:

The current Council returns a structured multi-artifact result containing provider responses, judgment artifacts, optional debate output, reliability assessment, semantic validation, execution status, and failure diagnostics.

No provider response, judge final_answer, or debate consensus_answer is declared to be the authoritative Council answer.

The current contract preserves completed artifacts across successful and degraded execution paths where possible.

The Web interface currently displays provider responses separately rather than selecting one Council answer.

Measured:

The verified baseline contains 217 passing tests.

Existing deterministic tests confirm the current successful and degraded result behavior.

Repository inspection confirms that no Council-level answer-selection rule exists.

Existing tests do not validate one authoritative Council answer or selected-answer quality.

Inferred:

Candidate A is internally coherent because it intentionally defines the Council as an observable multi-artifact analysis system rather than a single-answer system.

It provides strong observability, failure honesty, provenance preservation, and backward compatibility.

However, it transfers answer selection to each consumer.

Two compliant consumers may select different final answers from the same Council Result.

This can create inconsistent behavior between Python/API consumers, Web, CLI, scheduler, and automation consumers.

The absence of one selected Council answer also prevents consistent measurement of Council-level answer quality, because the system does not define which textual artifact represents the Council’s official output.

Candidate A is therefore suitable as an internal diagnostic and observability contract, but insufficient as the complete public answer contract for a consensus-oriented decision system.

Recommended:

Preserve the existing multi-artifact result as the diagnostic and backward-compatible foundation.

Do not preserve consumer-owned answer selection as the final Council architecture.

A future contract should add explicit Council-level answer authority while retaining all current artifacts and failure diagnostics.

Conclusion:

Internally coherent, but not sufficient as the final AI Council architecture.


### Candidate B — Universal Authoritative Council Answer


Observed:

The current repository does not implement a universal authoritative Council answer.

No execution path currently guarantees that exactly one textual artifact is designated as the official Council response.

Successful execution, answer availability, and reliability confidence are separate concepts in the current architecture.

Measured:

Repository inspection confirms that no deterministic answer-selection rule currently exists for all successful execution paths.

No existing test validates the presence of one authoritative Council answer across no-debate, debate, and degraded executions.

Inferred:

A universal authoritative answer would provide a single, consistent response for every successful execution.

This would simplify API consumers, Web presentation, CLI behavior, automation, and future downstream integrations.

However, a universal contract requires one deterministic rule that remains coherent across:

* successful no-debate execution;
* successful debate execution;
* provider degradation;
* judge failure;
* debate failure.

Current repository evidence does not identify such a rule.

Selecting a provider response, a judge final_answer, or debate consensus_answer as universally authoritative would require architectural assumptions that are not supported by the current implementation.

A universal contract is therefore attractive from a consumer perspective but cannot currently be justified without defining new Council-owned authority rules.

Recommended:

Do not adopt a universal authoritative-answer contract unless one deterministic, provider-neutral, failure-honest, and fully specified selection rule can be defined for every successful execution path.

Conclusion:

Internally coherent as a possible future architecture, but not supported by sufficient repository evidence for adoption in the current architecture.


### Candidate C — Conditional Authoritative Council Answer


Observed:

The current repository does not implement a conditional authoritative Council answer.

Current successful and degraded execution paths expose multiple artifacts without defining which execution paths, if any, produce an authoritative Council response.

Measured:

Repository inspection confirms that successful no-debate execution, successful debate execution, provider degradation, judge failure, and debate failure all return different combinations of artifacts.

No existing test defines which of these execution paths should qualify for an authoritative Council answer.

Inferred:

A conditional contract explicitly distinguishes between execution success and answer availability.

Unlike a universal contract, it allows the architecture to state that an authoritative Council answer exists only when clearly defined conditions are satisfied.

This approach provides greater failure honesty because the Council is not required to claim answer authority on execution paths where sufficient evidence or processing is unavailable.

However, the architecture must define qualifying and non-qualifying execution paths precisely.

Without explicit qualification rules, different consumers could still interpret answer availability differently.

A conditional contract therefore reduces ambiguity only if the qualification criteria are deterministic, observable, and consistent across all consumers.

Recommended:

A conditional authoritative-answer contract is architecturally plausible and aligns well with failure transparency.

It should be considered further only if the qualifying execution paths can be defined unambiguously while preserving backward compatibility and clear provenance.

Conclusion:

Internally coherent as a possible future architecture; adoption depends on explicit qualification rules.


### Candidate D — Debate Consensus Is Authoritative


Observed:

The current repository generates `debate["consensus_answer"]` only after successful debate execution.

The field is structurally validated and returned only within the nested debate object.

The current Council does not promote this field to a Council-level authoritative answer.

Measured:

Repository inspection confirms that `debate["consensus_answer"]` exists only when:

* both providers succeed;
* judgment completes successfully;
* debate is required;
* debate executes successfully.

No debate consensus exists for successful no-debate execution or for degraded execution paths.

Existing tests validate the structure of the field but do not establish its authority.

Inferred:

Making Debate Consensus authoritative would provide a natural answer source whenever debate succeeds.

However, this candidate does not define a coherent answer contract for:

* successful no-debate execution;
* provider degradation;
* judge failure;
* debate failure.

A second answer-selection policy would still be required for those execution paths.

Therefore, Candidate D does not define a complete Council-wide answer contract by itself.

Recommended:

Debate Consensus should continue to be treated as a debate-stage artifact unless a broader Council-owned answer contract defines how all remaining execution paths are handled.

Conclusion:

Internally coherent for successful debate execution only; insufficient as a complete Council-level answer contract.



### Candidate E — Judge Answer Is Authoritative


Observed:

The current repository includes `final_answer` fields produced by the provider judges.

These fields remain nested within the judgment object.

The current Council does not compare competing judge answers or promote any judge-generated answer to Council-level authority.

Measured:

Repository inspection confirms that judge `final_answer` fields are generated independently by each provider-based judge.

The Independent Judge currently does not provide a meaningful authoritative textual answer.

Existing tests validate the structure of judge outputs but do not establish authority for any judge-generated answer.

Inferred:

Selecting one judge-generated `final_answer` as the official Council response would require the architecture to grant answer authority to a specific judge or define a deterministic conflict-resolution rule between judges.

Neither rule exists in the current repository.

Such a decision would also blur the separation between the judgment stage and the Council stage, because judges currently evaluate responses rather than own the public Council answer.

This candidate therefore weakens architectural separation of responsibilities and introduces additional authority assumptions that are not supported by current evidence.

Recommended:

Judge-generated `final_answer` fields should remain judgment artifacts.

Council-level answer authority, if introduced in the future, should not be owned directly by an individual judge.

Conclusion:

Not recommended as a Council-level architecture due to unclear ownership and responsibility boundaries.



### Candidate F — Council-Owned Selection Contract


Observed:

The current repository aggregates provider responses, judgment artifacts, debate artifacts, reliability assessment, and semantic validation into a single Council Result.

However, the Council does not currently own or expose an authoritative answer-selection contract.

Measured:

Repository inspection confirms that no existing production component defines:

* answer ownership;
* answer-selection precedence;
* answer availability rules;
* authoritative answer provenance.

Current tests validate the presence and structure of individual artifacts but not Council-level answer authority.

Inferred:

A Council-owned selection contract preserves the existing architecture while assigning responsibility for answer authority to the Council itself rather than to providers, judges, debate, or consumers.

Under this model, existing artifacts remain available and unchanged, but the Council becomes the architectural owner of the public answer contract.

This preserves separation of responsibilities:

* Providers generate responses.
* Judges evaluate responses.
* Debate synthesizes responses when required.
* Reliability measures execution quality.
* The Council owns the public response contract.

This approach is compatible with future provider expansion because answer ownership remains independent of any individual provider or judge.

Implementation details remain intentionally undefined during this milestone.

Recommended:

If a future authoritative-answer contract is approved, ownership should belong to the Council layer while preserving all existing artifacts, provenance information, execution diagnostics, and backward compatibility.

Conclusion:

Internally coherent and architecturally consistent as a future Council-level contract.



## Execution-Path Matrix

### Execution-Path Matrix Legend

Answer Source
- None
- Provider Response
- Judge final_answer
- Debate consensus_answer
- Council-selected artifact

Answer Available
- Yes
- No

Answer Authoritative
- Yes
- No

Consumer Behavior
- Use authoritative answer
- Interpret artifacts
- No authoritative answer available
- Handle degraded execution
- Handle execution failure


| Execution Path | Candidate A | Candidate B | Candidate C | Candidate D | Candidate E | Candidate F |
|----------------|-------------|-------------|-------------|-------------|-------------|-------------|
| Both providers succeed; debate not required | No authoritative answer. Consumer interprets returned artifacts. | One authoritative answer required. Source undefined by current evidence. | Depends on qualification rules. | No debate consensus exists; therefore no authoritative answer. | Judge final_answer becomes authoritative. | Council selects an authoritative answer according to a Council-owned contract. |
| Both providers succeed; debate succeeds | Consumer interprets provider and debate artifacts. | One authoritative answer required. Debate or another source must be selected. | Depends on qualification rules. | debate["consensus_answer"] becomes authoritative. | Judge final_answer remains authoritative. | Council selects the authoritative answer while preserving debate provenance. |
| Gemini fails; DeepSeek succeeds | Remaining provider response available. No authoritative answer. | Universal contract requires one authoritative answer, but current evidence does not define the rule. | May or may not qualify depending on future contract. | Debate unavailable. No authoritative answer. | Judge answer unavailable or incomplete. | Council decides whether authority exists under explicit degraded-path rules. |
| DeepSeek fails; Gemini succeeds | Remaining provider response available. No authoritative answer. | Universal contract requires one authoritative answer, but current evidence does not define the rule. | May or may not qualify depending on future contract. | Debate unavailable. No authoritative answer. | Judge answer unavailable or incomplete. | Council decides whether authority exists under explicit degraded-path rules. |
| Both providers fail | Execution fails. No answer available. | No coherent universal answer possible. | No authoritative answer available. | No debate possible. | No judge answer possible. | No Council answer available. Execution failure is reported. |
| Judgment fails | Provider responses remain. Consumer interprets artifacts. | Universal answer cannot be determined consistently. | Usually non-qualifying unless future rules specify otherwise. | Debate cannot execute. | Judge authority unavailable. | Council applies explicit failure contract. |
| Debate required; debate fails | Provider and judgment artifacts remain. No authoritative answer. | Universal answer requires a fallback rule. | Depends on qualification rules. | Debate consensus unavailable. | Judge answer remains candidate if this architecture is adopted. | Council determines whether answer authority is unavailable or falls back according to future contract. |
| Low reliability confidence | Reliability metadata only. Does not change answer authority. | Reliability does not automatically remove authority. | Qualification rules may ignore reliability or treat it as metadata. | Debate consensus remains authoritative if available. | Judge answer remains authoritative. | Reliability remains separate from answer authority unless future contract specifies otherwise. |
| Large semantic validation gap | Diagnostic information only. Consumer interprets it. | Does not automatically invalidate the authoritative answer. | May influence qualification rules if explicitly defined. | Does not automatically invalidate debate consensus. | Does not automatically invalidate judge answer. | Semantic validation remains diagnostic unless a future Council contract explicitly incorporates it. |


## Decision Criteria


| Criterion | Candidate A | Candidate B | Candidate C | Candidate D | Candidate E | Candidate F |
|-----------|-------------|-------------|-------------|-------------|-------------|-------------|
| Mission alignment | Partial | Strong | Strong | Partial | Partial | Strong |
| Architectural clarity | Moderate | Strong | Strong | Moderate | Weak | Strong |
| Reliability value | Moderate | Strong | Strong | Moderate | Weak | Strong |
| Failure honesty | Strong | Moderate | Strong | Moderate | Weak | Strong |
| Consumer simplicity | Weak | Strong | Moderate | Moderate | Moderate | Strong |
| Consumer consistency | Weak | Strong | Strong | Weak | Moderate | Strong |
| Backward compatibility | Strong | Moderate | Strong | Strong | Moderate | Strong |
| Observability | Strong | Strong | Strong | Strong | Moderate | Strong |
| Provenance clarity | Strong | Moderate | Strong | Moderate | Weak | Strong |
| Testability | Strong | Moderate | Strong | Moderate | Moderate | Strong |
| Determinism | Strong | Moderate | Strong | Moderate | Moderate | Strong |
| Judge neutrality | Strong | Moderate | Strong | Weak | Weak | Strong |
| Debate compatibility | Strong | Strong | Strong | Strong | Weak | Strong |
| No-debate coherence | Strong | Moderate | Strong | Weak | Moderate | Strong |
| Degraded-path coherence | Strong | Weak | Strong | Weak | Weak | Strong |
| Web usability | Moderate | Strong | Strong | Moderate | Moderate | Strong |
| CLI / Automation usability | Moderate | Strong | Strong | Weak | Moderate | Strong |
| Reliability-measurement alignment | Moderate | Strong | Strong | Moderate | Weak | Strong |
| Future provider compatibility | Strong | Strong | Strong | Moderate | Weak | Strong |
| Implementation risk | None (no changes) | High | Medium | Medium | High | Medium |
| Migration risk | None | Medium | Medium | Medium | High | Medium |


## Candidate Comparison


| Candidate | Main Strength | Main Risk | No-Debate Coherence | Debate Coherence | Degraded Coherence | Consumer Clarity | Backward Compatibility | Reliability Alignment |
|-----------|---------------|-----------|---------------------|------------------|--------------------|------------------|------------------------|----------------------|
| Candidate A | Preserves the current architecture and maximum observability | No Council-owned answer authority | Strong | Strong | Strong | Weak | Strong | Moderate |
| Candidate B | Simple consumer experience through one universal answer | No deterministic rule for every execution path | Moderate | Strong | Weak | Strong | Moderate | Strong |
| Candidate C | Honest distinction between answer availability and execution success | Requires explicit qualification rules | Strong | Strong | Strong | Strong | Strong | Strong |
| Candidate D | Natural use of debate consensus | Covers only successful debate execution | Weak | Strong | Weak | Moderate | Strong | Moderate |
| Candidate E | Reuses existing judge answer artifacts | Blurs ownership between Judge and Council | Moderate | Weak | Weak | Moderate | Moderate | Weak |
| Candidate F | Clear Council ownership with preserved provenance and diagnostics | Requires a future Council-owned selection contract | Strong | Strong | Strong | Strong | Strong | Strong |

Observations:

- Candidate A best preserves the current implementation.
- Candidate B improves consumer simplicity but lacks a repository-supported universal rule.
- Candidate C provides strong architectural honesty through explicit answer qualification.
- Candidate D is limited to successful debate execution.
- Candidate E weakens separation of architectural responsibilities.
- Candidate F provides the clearest ownership model while preserving existing artifacts.


## Reliability Alignment


Observed:

The current repository measures execution reliability rather than answer correctness.

Existing reliability components evaluate:

- execution status;
- provider success and failure;
- debate execution;
- reliability assessment;
- semantic validation;
- stress metrics.

No existing metric determines whether one authoritative Council answer is correct.

Measured:

Repository inspection confirms that:

- execution success is measured;
- degraded execution is measured;
- debate usage is measured;
- debate success is measured;
- reliability confidence is measured;
- semantic validation is measured.

Current tests do not measure:

- authoritative answer quality;
- authoritative answer correctness;
- selected-answer consistency across consumers.

Inferred:

Execution success, answer availability, answer authority, reliability confidence, semantic support, and factual correctness represent different architectural concepts.

These concepts should remain independent.

A successful execution does not automatically imply:

- an authoritative answer exists;
- the answer is factually correct;
- the answer is highly reliable.

Likewise, low reliability confidence should not automatically remove answer authority unless a future architecture explicitly defines that behavior.

Recommended:

Future architecture should preserve the separation between:

- Execution Success
- Answer Availability
- Answer Authority
- Reliability Confidence
- Semantic Validation
- Factual Correctness

Reliability should remain metadata describing confidence rather than implicitly determining answer authority.


## Consumer Analysis


| Consumer | Needs One Official Answer? | Can Use Current Multi-Artifact Contract? | Risk of Independent Answer Selection | Provenance Visibility Required |
|----------|-----------------------------|------------------------------------------|--------------------------------------|-------------------------------|
| Python / API | Usually yes | Yes | High | High |
| Web Interface | Yes | Partially | High | Medium |
| Future CLI | Yes | Partially | High | High |
| Future Scheduler | Yes | No | High | High |
| Future Automation | Yes | No | High | High |
| Stress and Historical Reporting | No | Yes | Low | Medium |

Observed:

The current repository exposes a multi-artifact Council Result that can be consumed by different interfaces.

Existing consumers primarily use provider responses and execution metadata.

Measured:

No current production consumer is required by the repository to interpret one authoritative Council answer.

The Web interface currently displays provider responses separately.

Inferred:

Diagnostic and analytical consumers benefit from preserving all artifacts.

User-facing and automation-oriented consumers benefit from receiving one clearly defined Council response.

If answer authority remains undefined, different consumers may legitimately present different final answers from the same Council Result.

Recommended:

Future architecture should preserve the complete multi-artifact result while defining one Council-owned answer contract for consumers that require an official response.

Provenance should remain visible regardless of which answer contract is adopted.


## Final Architectural Decision


### Selected Decision

Decision C — Define a Conditional Authoritative Council Answer

### Decision Summary

The current multi-artifact Council Result should be preserved in its entirety.

A future architecture should define an authoritative Council answer only on explicitly qualified execution paths.

Answer authority must be owned by the Council rather than by providers, judges, debate, or consumers.

Execution success, answer availability, answer authority, and reliability confidence remain separate architectural concepts.

Existing provider responses, judgment artifacts, debate artifacts, reliability assessment, semantic validation, execution status, and degradation information remain part of the public Council Result for backward compatibility.

### Decision Rationale

Candidate A preserves the current architecture but leaves answer authority entirely to consumers.

Candidate B requires one universal answer without a deterministic and failure-honest rule supported by current repository evidence.

Candidate C provides the clearest separation between execution success and answer authority while preserving failure honesty.

Candidate D applies only to successful debate execution and does not define a complete Council-wide contract.

Candidate E assigns authority to judges, weakening the architectural separation between judgment and Council responsibilities.

Candidate F provides the strongest ownership model and is adopted as the architectural ownership principle supporting Decision C.

### Final Outcome

Outcome A — Contract Architecture Established.

Milestone #21 establishes a documentation-only architectural contract.

No production implementation, API change, result-field change, or behavioral modification is approved during this milestone.

Any implementation must occur in a separate future milestone after architectural approval.

### Closing Statement

Milestone #21 concludes the architectural investigation initiated in Milestones #17–#20 regarding Council answer authority.

Future work should focus on implementing and validating the approved architecture through incremental, test-driven development, consistent with the project's engineering principles, rather than further architectural characterization unless new evidence requires reopening this decision.
