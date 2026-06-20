# AI Council Roadmap

## Current Status

Stable baseline:

* Gemini provider
* DeepSeek provider
* Council engine
* Dual Judge architecture
* Independent Judge
* Debate engine
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
* Reliability trend comparison helper
* Reliability trend summary helper
* Reliability trend summary formatting
* 64 passing tests

Latest stable commit:

cbb4d55

---

## Priority 1

### Malformed Judge JSON Test

Status:

Completed.

Implemented:

* Judge malformed JSON detection
* Failure-path coverage
* Council stability verification

---

## Priority 2

### JSON Recovery Layer

Status:

Completed.

Implemented:

* Markdown fence removal
* JSON extraction from wrapper text
* Shared JSON parsing utility
* Recovery tests

---

## Priority 3

### Quota-Aware Handling

Status:

Completed.

Implemented:

* Quota error detection
* Quota metadata in council results
* Provider failure coverage
* Both-provider failure coverage

---

## Priority 4

### Stress Testing and Reliability Reporting

Status:

Completed.

Implemented:

* Stress test baseline
* Repeated council execution test
* Judge execution verification
* Stress metrics foundation
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

---

## Priority 5

### Reliability Trend Tracking Foundation

Status:

Completed.

Implemented:

* Reliability report comparison helper
* Reliability metric delta calculation
* Reliability trend direction detection
* Human-readable trend formatting
* Trend helper test coverage

Implemented commits:

* 39ddb0c - Add reliability trend comparison helper
* 700921e - Add reliability trend summary helper
* cbb4d55 - Add reliability trend summary formatting

---

## Next Milestone

### Optional Stress Report Persistence

Goal:

Allow stress and reliability reports to be saved for later comparison.

Planned scope:

* Persistence helpers only
* No dashboards
* No databases
* No provider changes
* No council architecture changes

Status:

Planned.

---

## Future Milestones

### Historical Reliability Reporting

Potential capabilities:

* Multi-run comparisons
* Long-term reliability history
* Historical summaries

Status:

Planned.

### Optional Stress Runner CLI

Potential capabilities:

* Manual execution commands
* Human-friendly report output

Status:

Planned.

---

## Future Council Expansion

Only after reliability and observability work is mature.

Potential additions:

* GPT
* Claude
* Grok

Strategy:

Do not expand provider count until reliability and observability foundations are complete.

---

## Long-Term Vision

Question
->
Multiple Providers
->
Multiple Judges
->
Debate
->
Consensus Answer
->
Reliability Measurement
->
Reliability Trends
->
Reliable AI Council

Goal:

Create a robust multi-model decision system that helps produce safer, more reliable decisions than a single-model workflow.