import sys
from pathlib import Path
import argparse
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from inteligent_component.config import load_config
from inteligent_component.moderation import moderate_image


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_expected(dataset_dir: Path) -> str:
    expected_path = dataset_dir / "expected.txt"

    if not expected_path.exists():
        raise FileNotFoundError(f"Manjka expected.txt: {expected_path}")

    expected = expected_path.read_text(encoding="utf-8").strip()

    allowed_values = {"ustrezno", "neustrezno", "neprepoznano"}

    if expected not in allowed_values:
        raise ValueError(
            f"Neveljavna expected vrednost: {expected}. "
            "Uporabi: ustrezno, neustrezno ali neprepoznano."
        )

    return expected


def get_top_reason(result: dict) -> tuple[str, float]:
    reasons = result.get("reasons", [])

    if not reasons:
        return "", 0.0

    top = reasons[0]
    return top.get("label", ""), float(top.get("score", 0.0))


def evaluate(config_name: str, dataset_name: str, configs_dir: Path, datasets_dir: Path) -> None:
    config_dir = configs_dir / config_name
    dataset_dir = datasets_dir / dataset_name
    images_dir = dataset_dir / "images"

    if not config_dir.exists():
        raise FileNotFoundError(f"Config mapa ne obstaja: {config_dir}")

    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset mapa ne obstaja: {dataset_dir}")

    if not images_dir.exists():
        raise FileNotFoundError(f"Images mapa ne obstaja: {images_dir}")

    config = load_config(config_dir)
    expected = load_expected(dataset_dir)

    result_path = dataset_dir / f"result_{config_name}.txt"

    images = sorted(
        [
            p for p in images_dir.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        ],
        key=lambda p: p.name
    )

    total = 0
    passed = 0
    failed = 0
    errors = 0

    with open(result_path, "w", encoding="utf-8") as out:
        out.write(f"config: {config_name}\n")
        out.write(f"dataset: {dataset_name}\n")
        out.write(f"expected: {expected}\n")
        out.write(f"unknown_threshold: {config.unknown_threshold}\n")
        out.write(f"unsuitable_threshold: {config.unsuitable_threshold}\n")
        out.write("\n")
        out.write("results:\n")

        for image_path in images:
            total += 1

            print(f"[{total}/{len(images)}] Testing {image_path.name} ... ", end="", flush=True)

            try:
                image = Image.open(image_path).convert("RGB")
                result = moderate_image(image, config)

                decision = result["decision"]
                top_label, top_score = get_top_reason(result)

                if decision == expected:
                    passed += 1
                    print("PASS")
                    out.write(f"{image_path.name}: PASS\n")
                else:
                    failed += 1
                    print("FAIL")
                    out.write("-------------\n")
                    out.write(f"{image_path.name}: FAIL\n")
                    out.write(f"result: {decision}\n")
                    out.write(f"expected: {expected}\n")
                    out.write(f"top label: \"{top_label}\"\n")
                    out.write(f"score: {top_score:.4f}\n")
                    out.write("-------------\n")

            except Exception as e:
                errors += 1
                print("ERROR")
                out.write("-------------\n")
                out.write(f"{image_path.name}: ERROR\n")
                out.write(f"error: {str(e)}\n")
                out.write("-------------\n")

        accuracy = passed / total if total > 0 else 0.0

        out.write("\n")
        out.write("summary:\n")
        out.write(f"total: {total}\n")
        out.write(f"passed: {passed}\n")
        out.write(f"failed: {failed}\n")
        out.write(f"errors: {errors}\n")
        out.write(f"accuracy: {accuracy:.4f}\n")

    print(f"Eval končan.")
    print(f"Config: {config_name}")
    print(f"Dataset: {dataset_name}")
    print(f"Expected: {expected}")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Result file: {result_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate AI moderation config on dataset."
    )

    parser.add_argument(
        "config_name",
        help="Ime konfiguracije v mapi configs, npr. config1"
    )

    parser.add_argument(
        "dataset_name",
        help="Ime dataseta v mapi datasets, npr. inappropriate1"
    )

    parser.add_argument(
        "--configs-dir",
        default="test/configs",
        help="Mapa s konfiguracijami. Default: test/configs"
    )

    parser.add_argument(
        "--datasets-dir",
        default="test/datasets",
        help="Mapa z dataseti. Default: test/datasets"
    )

    args = parser.parse_args()

    evaluate(
        config_name=args.config_name,
        dataset_name=args.dataset_name,
        configs_dir=Path(args.configs_dir),
        datasets_dir=Path(args.datasets_dir),
    )


if __name__ == "__main__":
    main()