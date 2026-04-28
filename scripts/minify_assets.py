#!/usr/bin/env python3
"""
Minify image assets to a target max size while preserving aspect ratio.

Usage examples:
  python3 scripts/minify_assets.py --dir assets --max-kb 500 --dry-run
  python3 scripts/minify_assets.py --dir assets --max-kb 500
  python3 scripts/minify_assets.py --dir assets --max-kb 500 --verify-only --recursive
  python3 scripts/minify_assets.py assets/1-vel-mark.png assets/5-vel-mark.png --max-kb 500
"""

from __future__ import annotations

import argparse
import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: python3 -m pip install Pillow"
    ) from exc

SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


@dataclass
class Candidate:
    data: bytes
    size_bytes: int
    width: int
    height: int
    scale: float
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reduce image sizes to fit under target kilobytes."
    )
    parser.add_argument("paths", nargs="*", help="Image files to process.")
    parser.add_argument(
        "--dir",
        default="assets",
        help="Directory to scan when no explicit paths are provided (default: assets).",
    )
    parser.add_argument(
        "--max-kb",
        type=int,
        default=500,
        help="Maximum allowed size in KB (default: 500).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing files.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan --dir for images.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Do not modify files; fail if any image is over --max-kb.",
    )
    return parser.parse_args()


def discover_images(paths: List[str], directory: str, recursive: bool) -> List[Path]:
    if paths:
        image_paths = [Path(p) for p in paths]
    else:
        root = Path(directory)
        pattern = "**/*" if recursive else "*"
        image_paths = [p for p in root.glob(pattern) if p.is_file()]

    valid = [p for p in image_paths if p.suffix.lower() in SUPPORTED_SUFFIXES]
    return sorted(valid)


def get_scales() -> List[float]:
    return [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4]


def iter_png_candidates(image: Image.Image, width: int, height: int, scale: float) -> Iterable[Candidate]:
    resized = image.resize((width, height), Image.Resampling.LANCZOS) if scale < 1.0 else image
    if resized.mode not in ("RGB", "RGBA", "P"):
        resized = resized.convert("RGBA")

    palette_steps = [256, 224, 192, 160, 128, 96, 64]
    for colors in palette_steps:
        quantized = resized.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors)
        buffer = io.BytesIO()
        quantized.save(buffer, format="PNG", optimize=True, compress_level=9)
        data = buffer.getvalue()
        yield Candidate(
            data=data,
            size_bytes=len(data),
            width=width,
            height=height,
            scale=scale,
            detail=f"png colors={colors}",
        )


def iter_jpeg_candidates(image: Image.Image, width: int, height: int, scale: float) -> Iterable[Candidate]:
    resized = image.resize((width, height), Image.Resampling.LANCZOS) if scale < 1.0 else image
    rgb = resized.convert("RGB")
    for quality in range(92, 44, -4):
        buffer = io.BytesIO()
        rgb.save(buffer, format="JPEG", optimize=True, progressive=True, quality=quality)
        data = buffer.getvalue()
        yield Candidate(
            data=data,
            size_bytes=len(data),
            width=width,
            height=height,
            scale=scale,
            detail=f"jpeg q={quality}",
        )


def iter_webp_candidates(image: Image.Image, width: int, height: int, scale: float) -> Iterable[Candidate]:
    resized = image.resize((width, height), Image.Resampling.LANCZOS) if scale < 1.0 else image
    rgb = resized.convert("RGB")
    for quality in range(92, 40, -4):
        buffer = io.BytesIO()
        rgb.save(buffer, format="WEBP", quality=quality, method=6)
        data = buffer.getvalue()
        yield Candidate(
            data=data,
            size_bytes=len(data),
            width=width,
            height=height,
            scale=scale,
            detail=f"webp q={quality}",
        )


def choose_candidate(path: Path, target_bytes: int) -> Optional[Candidate]:
    with Image.open(path) as image:
        width, height = image.size
        suffix = path.suffix.lower()
        best_under: Optional[Candidate] = None
        best_over: Optional[Candidate] = None

        for scale in get_scales():
            scaled_width = max(1, int(round(width * scale)))
            scaled_height = max(1, int(round(height * scale)))

            if suffix == ".png":
                candidates = iter_png_candidates(image, scaled_width, scaled_height, scale)
            elif suffix in {".jpg", ".jpeg"}:
                candidates = iter_jpeg_candidates(image, scaled_width, scaled_height, scale)
            elif suffix == ".webp":
                candidates = iter_webp_candidates(image, scaled_width, scaled_height, scale)
            else:
                continue

            for candidate in candidates:
                if candidate.size_bytes <= target_bytes:
                    if best_under is None or candidate.size_bytes > best_under.size_bytes:
                        best_under = candidate
                else:
                    if best_over is None or candidate.size_bytes < best_over.size_bytes:
                        best_over = candidate

            if best_under:
                break

        return best_under or best_over


def human_kb(size_bytes: int) -> str:
    return f"{size_bytes / 1024:.1f}KB"


def process_file(path: Path, target_bytes: int, dry_run: bool, verify_only: bool) -> bool:
    original_bytes = path.stat().st_size
    if original_bytes <= target_bytes:
        print(f"SKIP  {path} ({human_kb(original_bytes)})")
        return True

    if verify_only:
        print(f"FAIL  {path} ({human_kb(original_bytes)} > {human_kb(target_bytes)})")
        return False

    candidate = choose_candidate(path, target_bytes)
    if not candidate:
        print(f"FAIL  {path} (could not generate candidate)")
        return False

    outcome = (
        f"{human_kb(original_bytes)} -> {human_kb(candidate.size_bytes)} "
        f"[{candidate.width}x{candidate.height}, {candidate.detail}]"
    )
    if dry_run:
        print(f"PLAN  {path} {outcome}")
        return candidate.size_bytes <= target_bytes

    path.write_bytes(candidate.data)
    status = "OK" if candidate.size_bytes <= target_bytes else "WARN"
    print(f"{status:4}  {path} {outcome}")
    return True


def main() -> int:
    args = parse_args()
    target_bytes = args.max_kb * 1024
    image_paths = discover_images(args.paths, args.dir, args.recursive)

    if not image_paths:
        print("No supported images found.")
        return 1

    failures = 0
    for image_path in image_paths:
        try:
            success = process_file(
                image_path,
                target_bytes,
                args.dry_run,
                args.verify_only,
            )
        except Exception as exc:  # pragma: no cover
            success = False
            print(f"FAIL  {image_path} ({exc})")
        if not success:
            failures += 1

    print(f"\nProcessed {len(image_paths)} image(s), failures: {failures}.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
