# AI Council Roadmap

## Current Status

Stable baseline:

* Triple Judge architecture
* Majority Vote
* Structured Debate
* Provider retries
* Provider failure handling
* Judge failure handling
* Debate failure handling
* GitHub Actions CI
* 17 passing tests

Latest stable commit:

ae6076f

---

## Priority 1

### Malformed Judge JSON Test

Goal:

Add tests for malformed judge output.

Expected result:

* Judge malformed JSON is detected.
* Failure path is tested.
* Council remains stable.

Status:

Planned.

---

## Priority 2

### JSON Recovery Layer

Goal:

Recover from partially malformed LLM JSON.

Examples:

Current:

LLM returns invalid JSON
↓
Exception

Future:

LLM returns almost-valid JSON
↓
Recovery attempt
↓
Parse
↓
Continue

Potential techniques:

* Remove markdown fences
* Extract JSON blocks
* Strip wrapper text
* Normalize output before parsing

Status:

Planned.

---

## Priority 3

### Quota-Aware Handling

Goal:

Handle provider quota exhaustion more gracefully.

Observed issue:

429 RESOURCE_EXHAUSTED

Future behavior:

* Detect quota errors
* Return degraded mode
* Avoid hard failures

Status:

Planned.

---

## Priority 4

### Stress Testing

Goal:

Measure real-world reliability.

Targets:

* 20 requests
* 50 requests
* 100 requests

Metrics:

* Success rate
* Degraded rate
* Failure rate
* Debate rate
* Average response time

Status:

Planned.

---

## Future Council Expansion

Only after stability work is complete.

Potential additions:

* GPT
* Claude
* Grok

Strategy:

Do not expand model count until the core architecture is highly stable.

---

## Long-Term Vision

Question
↓
Multiple Providers
↓
Multiple Judges
↓
Majority Vote
↓
Debate
↓
Consensus Answer
↓
Reliable AI Council

Goal:

Create a robust multi-model decision system rather than a simple wrapper around a single LLM.
