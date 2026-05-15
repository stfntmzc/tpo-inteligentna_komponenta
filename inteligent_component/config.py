from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModerationConfig:
    labels: list[str]
    risk_labels: set[str]
    unknown_threshold: float
    unsuitable_threshold: float
    config_name: str


def load_lines(path: Path) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def load_thresholds(path: Path) -> tuple[float, float]:
    values = load_lines(path)

    if len(values) != 2:
        raise ValueError(
            f"threshold.txt mora vsebovati točno 2 vrstici: unknown_threshold in unsuitable_threshold. Datoteka: {path}"
        )

    unknown_threshold = float(values[0])
    unsuitable_threshold = float(values[1])

    if unknown_threshold >= unsuitable_threshold:
        raise ValueError(
            "unknown_threshold mora biti manjši od unsuitable_threshold."
        )

    return unknown_threshold, unsuitable_threshold


def load_config(config_dir: str | Path) -> ModerationConfig:
    config_dir = Path(config_dir)

    if not config_dir.exists():
        raise FileNotFoundError(f"Config mapa ne obstaja: {config_dir}")

    labels_path = config_dir / "labels.txt"
    risk_labels_path = config_dir / "risk_labels.txt"
    threshold_path = config_dir / "threshold.txt"

    labels = load_lines(labels_path)
    risk_labels = set(load_lines(risk_labels_path))
    unknown_threshold, unsuitable_threshold = load_thresholds(threshold_path)

    return ModerationConfig(
        labels=labels,
        risk_labels=risk_labels,
        unknown_threshold=unknown_threshold,
        unsuitable_threshold=unsuitable_threshold,
        config_name=config_dir.name,
    )