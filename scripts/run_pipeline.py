from pathlib import Path
import subprocess
import sys
import time


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


PIPELINE_STEPS = [
    ("Generate sample CSV data", SCRIPTS_DIR / "generate_sample_data.py"),
    ("Load CSV data into SQLite", SCRIPTS_DIR / "load_csv_to_sqlite.py"),
    ("Validate SQLite database", SCRIPTS_DIR / "validate_database.py"),
    ("Generate CSV reports", SCRIPTS_DIR / "generate_reports.py"),
    ("Generate charts", SCRIPTS_DIR / "generate_charts.py"),
]


def run_step(step_name: str, script_path: Path) -> None:
    print(f"\n=== {step_name} ===")

    if not script_path.exists():
        raise FileNotFoundError(f"Missing script: {script_path}")

    start_time = time.time()

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
    )

    elapsed_time = time.time() - start_time

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline failed at step: {step_name}. "
            f"Exit code: {result.returncode}"
        )

    print(f"Completed: {step_name} ({elapsed_time:.2f}s)")


def main() -> None:
    print("Starting camping store data pipeline...")
    print(f"Project root: {PROJECT_ROOT}")

    for step_name, script_path in PIPELINE_STEPS:
        run_step(step_name, script_path)

    print("\nPipeline completed successfully.")
    print("Outputs should be available in:")
    print("- data/")
    print("- reports/")
    print("- reports/charts/")


if __name__ == "__main__":
    main()