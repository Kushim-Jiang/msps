from pathlib import Path

import pathspec

repo_dir = Path(__file__).parent.parent


def load_gitignore_patterns() -> pathspec.PathSpec:
    """Load patterns from .gitignore."""
    gitignore_path = repo_dir / ".gitignore"
    if not gitignore_path.exists():
        return None
    with gitignore_path.open("r") as f:
        return pathspec.PathSpec.from_lines("gitwildmatch", f)


def clean_directory(directory: Path, spec: pathspec.PathSpec) -> None:
    """Remove files in the directory matching .gitignore patterns, except .pdf files."""
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix != ".pdf":
            relative_path = file_path.relative_to(Path.cwd())
            if spec.match_file(str(relative_path)):
                file_path.unlink()


def main() -> None:
    slides_dir = repo_dir / "slides"
    if not slides_dir.exists():
        print(f"Directory {slides_dir} does not exist.")
        return

    spec = load_gitignore_patterns()
    if spec is None:
        return

    clean_directory(slides_dir, spec)


if __name__ == "__main__":
    main()
