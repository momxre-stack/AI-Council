from agent.stress_runner import export_stress_summary, run_real_stress_test


def parse_request_count(args: list[str]) -> int:
    if not args:
        return 1

    return int(args[0])


def run_stress_cli(
    request_count: int = 1,
    runner=run_real_stress_test,
) -> str:
    summary = runner(request_count=request_count)

    return export_stress_summary(summary)


if __name__ == "__main__":
    print(run_stress_cli())