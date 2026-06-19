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
* Stress runner execution helper
* Multi-question stress runner
* Configurable default stress questions
* Real stress runner entrypoint
* Stress timing metrics
* Timing metrics in formatted stress reports
* Stress report export helper
* Reliability scoring
* Reliability reporting
* Reliability details in exported stress summaries
* Reliability information in formatted stress reports
* 54 passing tests

Latest stable commit:

b95204c

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

### Stress Testing and Reliability Reporting

Goal:

Measure system reliability and expose reliability information.

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
* Reusable stress execution helper
* Failure-path stress runner coverage
* Degraded-path stress runner coverage
* Debate-path stress runner coverage
* Multi-question stress runner helper
* Stress runner request helper
* Configurable default stress questions
* Real stress runner entrypoint
* Stress timing metrics
* Timing metrics in formatted stress reports
* Stress report export helper
* Reliability summary helper
* Reliability summary integration in stress runner
* Reliability details in exported stress summaries
* Reliability information in formatted stress reports

Remaining:

* Real-world reliability measurements
* Optional stress runner CLI
* Optional stress report persistence
* Optional historical reliability tracking

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
->
Multiple Providers
->
Multiple Judges
->
Majority Vote
->
Debate
->
Consensus Answer
->
Reliability Reporting
->
Reliable AI Council

Goal:

Create a robust multi-model decision system rather than a simple wrapper around a single LLM.