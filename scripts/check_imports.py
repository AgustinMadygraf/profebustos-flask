"""
Lightweight import rule checks for Clean Architecture boundaries.
"""

from pathlib import Path

FORBIDDEN_IMPORTS = (
    "flask",
    "pymysql",
    "dotenv",
)


def scan_file(path: Path) -> list[str]:
    hits = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for needle in FORBIDDEN_IMPORTS:
        if f"import {needle}" in text or f"from {needle}" in text:
            hits.append(needle)
    return hits


def scan_tree(root: Path) -> list[str]:
    violations = []
    for py_file in root.rglob("*.py"):
        hits = scan_file(py_file)
        for hit in hits:
            violations.append(f"{py_file}: forbidden import '{hit}'")
    return violations


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    domain_root = repo_root / "src" / "entities"
    application_root = repo_root / "src" / "application"

    violations = []
    for root in (domain_root, application_root):
        if root.exists():
            violations.extend(scan_tree(root))

    if violations:
        print("Import rule violations:")
        for item in violations:
            print(f"- {item}")
        return 1
    print("Import rule checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
