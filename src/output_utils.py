from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

# Root location for generated artifacts. A "results" folder is created under
# this root to keep JSON outputs together.
DEFAULT_OUTPUT_ROOT = Path(__file__).resolve().parent.parent / "outputs"
DEFAULT_RESULTS_DIRNAME = "results"
STAGE_GENERATION = "generation"
STAGE_OPTIMIZATION = "optimization"


def ensure_dir(path: Path) -> Path:
    """Create the directory if it does not exist and return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_results_dir(output_dir: str | None = None) -> Path:
    """
    Resolve the root directory where JSON results are stored.

    If `output_dir` already ends with "results" it is used directly;
    otherwise a "results" subdirectory is placed under the supplied root
    (defaulting to `<repo>/outputs`).
    """
    root = Path(output_dir).expanduser() if output_dir else DEFAULT_OUTPUT_ROOT
    results_dir = root if root.name == DEFAULT_RESULTS_DIRNAME else root / DEFAULT_RESULTS_DIRNAME
    return ensure_dir(results_dir)


def resolve_stage_dir(stage: str, output_dir: str | None = None) -> Path:
    """Return the stage-specific directory (generation/optimization) under results."""
    return ensure_subdir(resolve_results_dir(output_dir), stage)


def ensure_subdir(base: Path, name: str) -> Path:
    """Return (and create) a named subdirectory under `base`."""
    return ensure_dir(base / name)


def result_path(
    dataset: str,
    model: str,
    stage_dir: Path,
    profiler: str = "none",
    epoch: int | None = None,
    suffix: str | None = None,
) -> Path:
    """
    Build the JSON filename for dataset/model with stage and profiler context.
    Layout: <results>/<stage>/<dataset>_<model>_<profiler>[ _suffix ][ _epoch ].json
    """
    parts = [dataset, model, profiler]
    if suffix:
        parts.append(str(suffix))
    if epoch is not None:
        parts.append(str(epoch))
    return stage_dir / f"{'_'.join(parts)}.json"


def overhead_path(
    dataset: str,
    model: str,
    stage_dir: Path,
    profiler: str = "none",
    suffix: str | None = None,
) -> Path:
    """Build the overhead metrics filename for a given dataset/model/profiler."""
    name_parts = [f"overhead", dataset, model, profiler]
    if suffix:
        name_parts.append(suffix)
    return stage_dir / f"{'_'.join(name_parts)}.json"


def write_json(data: Any, path: Path) -> None:
    """Persist data as pretty JSON, ensuring parent directories exist."""
    ensure_dir(path.parent)
    with path.open("w") as f:
        json.dump(data, f, indent=4)


def find_existing_result(
    dataset: str,
    model: str,
    stage_dir: Path,
    profiler: str | None = None,
    legacy_dirs: Iterable[Path] = (),
    legacy_filenames: Iterable[str] = (),
) -> Path | None:
    """
    Locate an existing result file for dataset/model.

    Checks stage_dir using current naming (with optional profiler), then any
    legacy directories and filenames. Returns None if nothing is found.
    """
    profilers_to_try: list[str] = []
    if profiler:
        profilers_to_try.append(profiler)
    profilers_to_try.append("none")

    for prof in profilers_to_try:
        candidate = result_path(dataset, model, stage_dir, profiler=prof)
        if candidate.exists():
            return candidate
    for legacy in legacy_dirs:
        for name in legacy_filenames:
            legacy_path = legacy / name
            if legacy_path.exists():
                return legacy_path
        legacy_candidate = legacy / f"{dataset}_{model}.json"
        if legacy_candidate.exists():
            return legacy_candidate
    return None
