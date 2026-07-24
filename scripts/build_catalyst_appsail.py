from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIST = ROOT / "dist" / "catalyst-appsail"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Zoho Catalyst AppSail bundle.")
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST, help="Output directory for the AppSail bundle.")
    parser.add_argument(
        "--install-dependencies",
        action="store_true",
        help="Install Python dependencies into the bundle. Run this on Linux/WSL for Catalyst managed runtime deploys.",
    )
    parser.add_argument(
        "--include-local-database",
        action="store_true",
        help="Copy the local SQLite database into the bundle for AppSail demos that must use real local records.",
    )
    parser.add_argument(
        "--database-path",
        type=Path,
        default=ROOT / "data" / "secure_system.db",
        help="Local SQLite database to include when --include-local-database is set.",
    )
    parser.add_argument("--keep", action="store_true", help="Do not remove the existing output directory first.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dist = args.dist.resolve()
    if not _inside_root(dist):
        raise SystemExit(f"Refusing to write outside the project workspace: {dist}")

    if dist.exists() and not args.keep:
        shutil.rmtree(dist)
    dist.mkdir(parents=True, exist_ok=True)

    _copy_file(ROOT / "catalyst_app.py", dist / "catalyst_app.py")
    _copy_file(ROOT / "requirements.txt", dist / "requirements.txt")
    _copy_file(ROOT / "pyproject.toml", dist / "pyproject.toml")
    _copy_tree(ROOT / "src", dist / "src")
    if args.include_local_database:
        database_path = args.database_path.resolve()
        if not database_path.exists():
            raise SystemExit(f"Local database not found: {database_path}")
        if not _inside_root(database_path):
            raise SystemExit(f"Refusing to copy database outside the project workspace: {database_path}")
        _copy_file(database_path, dist / "data" / "secure_system.db")
        print(f"Included local database: {database_path}")

    if args.install_dependencies:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--target",
                str(dist),
                "-r",
                str(ROOT / "requirements.txt"),
            ]
        )

    print(f"Catalyst AppSail bundle ready: {dist}")


def _inside_root(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return False
    return True


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _copy_tree(source: Path, target: Path) -> None:
    shutil.copytree(
        source,
        target,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".pytest_cache"),
    )


if __name__ == "__main__":
    main()
