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
* Categorized benchmark questions
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
* Stress report persistence
* Latest report path helper
* Latest report loading
* Latest report comparison
* Latest report summaries
* Summary formatting
* Summary generation
* Summary save helper
* Summary load helper
* Summary existence checks
* Stress report summary module
* Reliability quality improvements
* Debate quality improvements
* Evaluation and benchmark improvements
* 144 passing tests

Latest stable commit:

697e856

---

## Priority 1

### Malformed Judge JSON Test

Status:

Completed.

---

## Priority 2

### JSON Recovery Layer

Status:

Completed.

---

## Priority 3

### Quota-Aware Handling

Status:

Completed.

---

## Priority 4

### Stress Testing and Reliability Reporting

Status:

Completed.

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

---

## Priority 6

### Real-World Long-Run Measurements

Status:

Completed.

Implemented:

* Stress report persistence
* Latest report path helper
* Latest report loading
* Latest report comparison
* Latest report summaries
* Summary formatting
* Summary generation
* Summary save helper
* Summary load helper
* Summary existence checks
* Summary module extraction
* Cleanup duplicated tests

---

## Future Milestones

### Optional Stress Runner CLI

Status:

Completed.

Implemented:

* Stress CLI helper wrapper
* Request count support
* Executable module entry point
* Basic request count argument parsing
* CLI request count validation
* CLI regression coverage

### Reliability Quality Improvements

Status:

Completed.

Implemented:

* Missing trend direction fallback
* None trend deltas fallback
* Missing summary fields fallback
* None summary deltas fallback
* Missing reliability status fallback
* Missing stress result status fallback
* Parent directory creation
* Reject non-positive request counts
* Reject non-positive real stress request counts
* Reject empty question lists
* Additional regression coverage

### Debate Quality Improvements

Status:

Completed.

Implemented:

* Required debate field validation
* Debate string type validation
* Empty debate field rejection
* Unexpected debate field rejection
* Empty question rejection
* Empty Gemini response rejection
* Empty DeepSeek response rejection
* Identical response rejection
* Minimum debate field length checks
* Debate input trimming
* Debate output trimming
* Debate validation helper extraction
* Debate prompt template extraction
* Stable debate output field order
* Additional debate regression coverage

### Provider Reliability Hardening

Status:

Completed.

Implemented:

* Retry recovery coverage
* Retry exhaustion coverage
* Gemini API error retries
* Gemini unknown response retries
* DeepSeek API error retries
* DeepSeek rate limit retries
* DeepSeek connection retries
* Provider timeout configuration
* Provider degraded reasons
* Judge degraded reasons
* Debate degraded reasons
* Successful flow degraded reason coverage
* Additional provider regression coverage

### Gemini REST Provider Migration

Status:

Completed.

Implemented:

* Replaced Gemini SDK execution path with REST implementation
* Preserved public provider contract
* Added Gemini REST request helper
* Added Gemini REST response parser
* Migrated Gemini provider tests to REST-based mocks
* Preserved retry behavior
* Preserved graceful provider failure behavior
* Removed unused Gemini SDK imports
* Verified manual Gemini REST smoke test
* Verified browser /ask
* Verified full test suite: 197 passing tests

Notes:

* Gemini SDK SSL handshake timeout is resolved.
* Remaining provider limitation is HTTP 429 rate limiting.

### Semantic Judge Design

Status:

Completed.

Implemented:

* Analyzed Independent Judge limitations
* Documented lexical overlap limitation
* Defined semantic agreement direction
* Compared rejected and acceptable approaches
* Selected smallest safe prototype direction
* Added Semantic Judge design document

Notes:

* No production behavior changed.
* Council, Debate, and Providers remain unchanged.
* Semantic Engine implementation is intentionally postponed.

### Evaluation / Benchmark Improvements

Status:

Completed.

Implemented:

* Debate usage rate coverage
* Debate vote metrics
* Judge agreement metrics
* Judge disagreement metrics
* Debate success metrics
* Debate failure metrics
* Debate effectiveness rate
* Judge agreement rate
* Judge disagreement rate
* Stress question categories
* Category coverage metrics
* Improved benchmark question set
* Judge usefulness metrics

Note:

* Debate usefulness is covered by debate effectiveness rate.

### Historical Analytics

Status:

Completed.

Implemented:

* Historical reliability history
* Trend comparisons across saved runs
* Reliability degradation detection
* Historical comparison reports
* Historical reliability summaries
* Historical report generation
* Empty historical report handling
* Single-report historical coverage
* Additional regression coverage

### Reliability Confidence

Status:

Completed.

Implemented:

* Reliability confidence helper
* Reliability assessment helper
* Council reliability assessment integration
* Judgment agreement rate integration
* Reliability assessment reasons
* Confidence boundary regression coverage
* Assessment regression coverage

### Provider Expansion

Status:

Planned.

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
Historical Analytics
->
Reliable AI Council

Goal:

Create a robust multi-model decision system that helps produce safer, more reliable decisions than a single-model workflow.