from agent.independent_judge import independent_judge_responses


BENCHMARK_CASES = [
    {
        "question": (
            "Explain the difference between concurrency and parallelism "
            "in one concise paragraph."
        ),
        "gemini_response": (
            "Concurrency is about dealing with multiple tasks *at once*, managing "
            "their progress potentially by rapidly switching between them on a "
            "single processing unit. Parallelism, however, is the true "
            "*simultaneous execution* of multiple tasks *at the very same instant* "
            "across multiple distinct processing units. Therefore, while "
            "concurrency focuses on *managing* multiple ongoing tasks, parallelism "
            "specifically refers to *doing* multiple tasks simultaneously, requiring "
            "the appropriate hardware."
        ),
        "deepseek_response": (
            "Concurrency is about **dealing with multiple tasks at once**, managing "
            "their interleaved execution so they appear to progress simultaneously, "
            "even on a single-core processor. Parallelism, on the other hand, is "
            "about **doing multiple tasks at the literal same time**, requiring "
            "multiple cores or processors. In short, concurrency is a **structure** "
            "of handling tasks (like multitasking), while parallelism is an "
            "**execution** mechanism (like multiple workers working side-by-side)."
        ),
        "expected_agreement_score": 20,
    },
    {
        "question": (
            "Explain the difference between a process and a thread "
            "in one concise paragraph."
        ),
        "gemini_response": (
            "A **process** is an independent instance of a running program, each "
            "with its **own isolated memory space, resources (like file handles), "
            "and system state**, making it a heavyweight execution unit. In contrast, "
            "a **thread** is a lightweight unit of execution *within* a process, "
            "sharing that process's **memory space and resources** but maintaining "
            "its **own program counter, stack, and registers**. Therefore, a single "
            "process can contain multiple threads, allowing for concurrent execution "
            "within the same shared environment."
        ),
        "deepseek_response": (
            "A process is an independent program running in its own isolated memory "
            "space, while a thread is a smaller unit of execution within a process "
            "that shares that same memory space and resources. Processes are "
            "heavyweight, requiring more overhead to create and manage due to "
            "separate address spaces, whereas threads are lightweight and allow "
            "efficient communication and context switching because they share data "
            "directly. This means a crash in one process doesn't affect other "
            "processes, but a fault in one thread can crash the entire containing "
            "process."
        ),
        "expected_agreement_score": 23,
    },
    {
        "question": (
            "Explain the difference between normalization and denormalization "
            "in database design in one concise paragraph."
        ),
        "gemini_response": (
            "**Normalization** is the process of structuring a database to reduce "
            "data redundancy and improve data integrity by organizing data into "
            "multiple, smaller, related tables, minimizing update anomalies. "
            "**Denormalization**, conversely, is the process of intentionally "
            "introducing controlled redundancy—often by combining tables or "
            "duplicating data—to optimize query performance, typically by minimizing "
            "the need for complex joins, though this can increase storage and the "
            "risk of update inconsistencies."
        ),
        "deepseek_response": (
            "Normalization organizes data into multiple related tables to minimize "
            "redundancy and ensure data integrity by eliminating duplicate information "
            "(e.g., splitting customer and order data into separate tables linked by "
            "IDs). Denormalization intentionally combines those tables or adds "
            "redundant data to optimize read performance by reducing the number of "
            "joins required, often at the cost of increased storage and potential "
            "update anomalies."
        ),
        "expected_agreement_score": 21,
    },
]


def test_independent_judge_offline_benchmark_cases_are_auditable():
    for case in BENCHMARK_CASES:
        result = independent_judge_responses(
            question=case["question"],
            gemini_response=case["gemini_response"],
            deepseek_response=case["deepseek_response"],
        )

        assert result["judge_type"] == "independent_rule_based"
        assert "diagnostics" in result
        assert result["diagnostics"]["total_count"] > 0
        assert result["diagnostics"]["overlap_count"] >= 0
        assert result["agreement_score"] == case["expected_agreement_score"]
