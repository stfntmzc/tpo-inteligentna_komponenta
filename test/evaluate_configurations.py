import argparse
import subprocess
import sys
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
CONFIG_LIST_FILE = TEST_DIR / "configurations_to_evaluate.txt"
OUTPUT_FILE = TEST_DIR / "configurations_evaluation_result.txt"
EVALUATE_SCRIPT = TEST_DIR / "evaluate_config.py"


def read_configs() -> list[str]:
    if not CONFIG_LIST_FILE.exists():
        raise FileNotFoundError(f"Manjka datoteka: {CONFIG_LIST_FILE}")

    return [
        line.strip()
        for line in CONFIG_LIST_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def extract_accuracy(output: str) -> str:
    for line in output.splitlines():
        if line.startswith("Accuracy:"):
            return line.split(":", 1)[1].strip()

    raise ValueError("V outputu evaluate_config.py nisem našel vrstice 'Accuracy:'.")


def main():
    parser = argparse.ArgumentParser(
        description="Run evaluate_config.py for all configurations listed in configurations_to_evaluate.txt."
    )

    parser.add_argument(
        "dataset",
        help="Ime dataseta, npr. inappropriate1 ali appropriate"
    )

    args = parser.parse_args()

    configs = read_configs()
    results = []

    for config in configs:
        print(f"Testing {config} on dataset {args.dataset} ... ", end="", flush=True)

        completed = subprocess.run(
            [
                sys.executable,
                str(EVALUATE_SCRIPT),
                config,
                args.dataset,
            ],
            cwd=TEST_DIR.parent,
            text=True,
            capture_output=True,
        )

        if completed.returncode != 0:
            print("ERROR")
            print(completed.stderr)
            results.append("ERROR")
            continue

        try:
            accuracy = extract_accuracy(completed.stdout)
            print(accuracy)
            results.append(accuracy)
        except Exception as e:
            print("ERROR")
            print(e)
            results.append("ERROR")

    OUTPUT_FILE.write_text("\n".join(results) + "\n", encoding="utf-8")

    print()
    print(f"Rezultati zapisani v: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()