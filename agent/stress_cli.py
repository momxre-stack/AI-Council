import sys

from agent.stress_runner import export_stress_summary, run_real_stress_test


def parse_request_count(args: list[str]) -> int:
    if not args:
        return 1

    try:
        request_count = int(args[0])
    except ValueError:
        raise ValueError("request_count must be a positive integer")

    if request_count <= 0:
        raise ValueError("request_count must be a positive integer")

    return request_count


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