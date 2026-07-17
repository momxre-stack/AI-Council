# AI Council — Project State

## Project Goal

Build a robust multi-model decision system that produces more reliable answers than a single-model workflow.

The system combines multiple providers, independent evaluation, debate when justified, consensus generation, reliability measurement, and historical reliability analysis.

---

## Repository

Repository:

`momxre-stack/AI-Council`

Branch:

`main`

Baseline verified before this project-state refresh:

`143a6bf — Measure authoritative answer availability rate`

---

## Stable Baseline

* Main branch clean
* Origin synchronized
* All commits pushed
* 225 passing tests
* GitHub Actions CI
* Stable production behavior

---

## Current Providers

Production Council providers:

1. Gemini
2. DeepSeek

Gemini uses the REST provider implementation with a 60-second request timeout.

An OpenAI provider module exists but is not integrated into the production Council registry.

Provider expansion remains planned but has not been selected as the next implementation phase.

Its priority must be evaluated against reliability, observability, and operational improvements before implementation begins.

---

## Current Council Flow

Question

↓

Gemini + DeepSeek

↓

Gemini Judge + DeepSeek Judge

↓

Independent Judge vote and diagnostics

↓

Dual Judge production decision policy

↓

Debate when justified

↓

Debate consensus when debate succeeds

↓

Conditional Council-owned authoritative answer on the qualified path

↓

Reliability assessment

↓

Stress and historical reliability measurements

In parallel, the provider-only shadow debate decision records what the debate decision would have been without the Independent Judge vote.

The shadow decision is diagnostic only and does not change production behavior.

---

## Current Council Result Contract

The Council preserves its existing multi-artifact result and adds a Council-owned conditional authoritative-answer field:

```python
"authoritative_answer": {
    "available": bool,
    "answer": str | None,
    "provenance": str | None,
}
```

The only currently qualifying path is:

```text
both providers succeed
→ judgment succeeds
→ debate is required
→ debate succeeds
→ debate["consensus_answer"] becomes authoritative
```

All non-qualifying paths explicitly report:

```python
"authoritative_answer": {
    "available": False,
    "answer": None,
    "provenance": None,
}
```

Stress observability now includes:

* `authoritative_answer_available_count`
* `authoritative_answer_availability_rate`

Availability measures only whether an authoritative answer was explicitly reported.

It does not measure factual correctness, answer quality, consensus strength, debate quality, semantic agreement, or reliability confidence.

---

## Current Judge Architecture

The current architecture includes:

* Gemini Judge
* DeepSeek Judge
* Independent Judge
* Dual Judge vote diagnostics
* Winner-disagreement protection
* Significant score-gap protection
* Debate vote threshold protection
* Provider-only shadow debate decisions

The Independent Judge is deterministic, reproducible, provider-independent, and primarily lexical.

It remains useful for measurement, diagnostics, auditing, and semantic-gap observation.

Current evidence does not justify provider-independent deterministic semantic decision authority.

The existing production vote policy remains unchanged; provider-only debate decisions are currently measured in shadow mode.

The permanent architectural boundaries are documented in:

`docs/PROVIDER_INDEPENDENT_REASONING_BOUNDARIES.md`

---

## Reliability and Fault Tolerance

Implemented:

* Provider retries
* Provider timeout handling
* Provider failure handling
* Judge failure handling
* Debate failure handling
* Degraded mode
* JSON recovery
* Malformed JSON rejection
* Quota-aware error handling
* Provider error redaction
* API key redaction
* Stress testing
* Reliability scoring
* Reliability confidence
* Reliability trends
* Historical analytics
* Long-run measurements

---

## Provider-Independent Reasoning Investigation

Milestones #16.6–#16.14 investigated whether a deterministic provider-independent component could become a reliable semantic decision-maker.

The investigation included:

* Semantic Judge design
* Deterministic concept matching
* Lexical normalization
* Independent Judge benchmark characterization
* Semantic validation
* Authority auditing
* Dissent Auditor characterization
* Shadow instrumentation
* Provider-only shadow decisions
* Repository history inspection
* Production observations
* Independent architectural reviews

Final architectural conclusion:

Deterministic provider-independent techniques provide demonstrated value for measurement, auditing, structural validation, historical analysis, and observability.

Current evidence does not justify deterministic provider-independent semantic decision authority.

This investigation is closed under the current architectural constraints unless fundamentally new evidence becomes available.

---

## Engineering Principles

* Reliability before features
* Evidence before implementation
* Stability before speed
* Observability before expansion
* Small commits over large rewrites
* Minimal diffs
* Backward compatibility
* No speculative refactors
* Tests before confidence
* Protect the main branch
* Preserve clean stopping points
* Do not grant decision authority without measured reliability evidence

---

## Current Documentation

Primary architectural and project references:

* `docs/ROADMAP.md`
* `docs/PROJECT_STATE.md`
* `docs/SEMANTIC_JUDGE_DESIGN.md`
* `docs/SEMANTIC_JUDGE_VALIDATION.md`
* `docs/DISSENT_AUDITOR.md`
* `docs/PROVIDER_INDEPENDENT_REASONING_BOUNDARIES.md`
* `docs/MILESTONE_19_COUNCIL_RESULT_CONTRACT.md`
* `docs/MILESTONE_20_CONSENSUS_ARCHITECTURE.md`
* `docs/MILESTONE_21_COUNCIL_AUTHORITATIVE_ANSWER_DECISION.md`

---

## Current Stable State

* Main branch clean
* Origin synchronized
* 225 passing tests
* Latest verified implementation commit: `143a6bf`
* Gemini REST provider stable
* DeepSeek provider stable
* Provider-only shadow decision implemented
* Provider error redaction implemented
* Provider-independent reasoning ADR accepted
* Milestones #17–#24 completed
* Conditional Council-owned authoritative answer contract implemented
* Authoritative-answer availability count and rate implemented

---

## Next Phase

The next development phase has not yet been selected.

Candidate directions must be evaluated by expected reliability value rather than roadmap order alone.

Potential directions include:

* further reliability quality improvements;
* debate quality improvements supported by new evidence;
* scheduler or automation work;
* operational observability improvements;
* provider expansion, only if justified by evidence.

No candidate is an approved implementation milestone until scope, evidence, risks, and validation criteria are defined.

---

## Guiding Principle

პატარა ნაბიჯებით დიდი მიზნისკენ.
