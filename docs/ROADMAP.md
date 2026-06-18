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
* JSON recovery layer
* Quota-aware handling
* GitHub Actions CI
* Stress testing foundation
* Stress metrics utilities
* Stress runner summary module
* 39 passing tests

Latest stable commit:

a39e7c0

---

## Priority 1

### Malformed Judge JSON Test

Goal:

Add tests for malformed judge output.

Result:

* Judge malformed JSON is detected.
* Failure path is tested.
* Council remains stable.

Status:

Completed.

---

## Priority 2

### JSON Recovery Layer

Goal:

Recover from partially malformed LLM JSON.

Implemented:

* Markdown fence removal
* JSON extraction from wrapper text
* Shared JSON parsing utility
* Recovery tests

Status:

Completed.

---

## Priority 3

### Quota-Aware Handling

Goal:

Handle provider quota exhaustion more gracefully.

Implemented:

* Quota error detection
* Quota metadata in council results
* Provider failure coverage
* Both-provider failure coverage

Status:

Completed.

---

## Priority 4

### Stress Testing

Goal:

Measure system reliability.

Completed:

* Stress test baseline
* Repeated council execution test
* Judge execution verification
* Stress metrics foundation
* Stress metrics counting test
* 20 request stress simulation
* 50 request stress simulation
* 100 request stress simulation
* Success-rate reporting
* Degraded-rate reporting
* Failure-rate reporting
* Debate-rate reporting
* Stress report builder
* Human-readable stress report formatting
* Stress runner summary module

Remaining:

* Real stress runner
* Real-world reliability measurements

Status:

In Progress.

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
→
Multiple Providers
→
Multiple Judges
→
Majority Vote
→
Debate
→
Consensus Answer
→
Reliable AI Council

Goal:

Create a robust multi-model decision system rather than a simple wrapper around a single LLM.