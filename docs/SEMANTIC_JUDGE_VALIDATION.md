# Semantic Judge Validation

## Status

Validation only.

No production implementation is included here.

## Purpose

This document collects deterministic validation examples for the future Semantic Judge prototype.

The goal is to evaluate whether concept matching reduces false disagreements without creating false agreements.

## Validation Cases

### Positive semantic agreement: artificial intelligence

Expected behavior:

- agreement should not be treated as low
- debate should not be required

Text A:

Artificial intelligence is a field of computer science focused on machines performing tasks that require human intelligence.

Text B:

AI is an area of computing that creates systems capable of learning, reasoning, and solving problems.

### Positive semantic agreement: Python

Expected behavior:

- agreement should not be treated as low
- debate should not be required

Text A:

Python is a programming language used for automation, web development, and data analysis.

Text B:

Python is a coding language commonly used to build websites, automate tasks, and analyze data.

### Negative semantic agreement: unrelated answer

Expected behavior:

- agreement should remain low
- debate should be required

Text A:

Artificial intelligence is a field of computer science focused on machines performing tasks that require human intelligence.

Text B:

Bananas are yellow fruits that contain potassium and are commonly eaten as a snack.

## Validation Principle

A prototype should only be accepted if it improves positive semantic agreement cases without increasing agreement for unrelated answers.

## Acceptance Criteria

A deterministic prototype should only be accepted if it demonstrates all of the following:

- Improves agreement for multiple semantic paraphrases.
- Does not increase agreement for unrelated answers.
- Preserves deterministic behavior.
- Remains provider-independent.
- Requires no changes to Council, Debate, or Providers.
- Passes the complete test suite.
- Demonstrates improvement on multiple validation examples rather than a single hand-crafted example.

## Future Validation

This document is expected to grow as additional real AI Council outputs are collected.

Implementation should be driven by recurring evidence from real Council executions rather than isolated examples.
