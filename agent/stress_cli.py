import sys

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


def run_stress_cli_from_args(
    args: list[str],
    runner=run_real_stress_test,
) -> str:
    return run_stress_cli(
        request_count=parse_request_count(args),
        runner=runner,
    )


if __name__ == "__main__":
    print(run_stress_cli_from_args(sys.argv[1:]))