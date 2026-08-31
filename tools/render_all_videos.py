#!/usr/bin/env python3
"""
tools/render_all_videos.py — Batch video rendering orchestrator executing TermReel record across workshop scenario manifests.
"""

import argparse
import glob
import os
import pathlib
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios"
VIDEO_DIR = REPO_ROOT / "video"
DOCS_ASSETS_DIR = REPO_ROOT / "docs" / "assets" / "videos"

TERMREEL = shutil.which("termreel") or os.path.expanduser("~/.local/bin/termreel")
FFMPEG = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/usr/bin/ffprobe"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(DOCS_ASSETS_DIR, exist_ok=True)


def render_scenario(scenario_path: pathlib.Path) -> Tuple[str, bool, str]:
    name = scenario_path.name
    start_t = time.time()
    print(f"🎬 [START] {name}")

    cmd = [TERMREEL, "record", str(scenario_path)]
    res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)

    elapsed = time.time() - start_t
    if res.returncode == 0:
        print(f"✅ [DONE] {name} ({elapsed:.1f}s)")
        return (name, True, res.stdout)
    else:
        print(f"❌ [FAIL] {name} ({elapsed:.1f}s)\n{res.stderr}\n{res.stdout}")
        return (name, False, res.stderr)


def get_video_duration(video_path: pathlib.Path) -> float:
    """Gets video duration using ffprobe."""
    try:
        cmd = [
            FFPROBE, "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return float(res.stdout.strip())
    except Exception:
        pass
    return 30.0


def extract_posters_and_sync() -> None:
    print("📸 Generating poster thumbnails and syncing video assets...")
    for mp4_file in sorted(VIDEO_DIR.glob("*.mp4")):
        base = mp4_file.name
        stem = mp4_file.stem

        # Sync MP4 to docs/assets/videos/
        dst_mp4 = DOCS_ASSETS_DIR / base
        shutil.copy2(mp4_file, dst_mp4)

        # Generate poster thumbnail
        poster_stem = stem
        if stem.startswith("module_01"):
            poster_stem = "module_01"
        elif stem.startswith("module_02"):
            poster_stem = "module_02"
        elif stem.startswith("module_03"):
            poster_stem = "module_03"
        elif stem.startswith("module_04"):
            poster_stem = "module_04"
        elif stem.startswith("module_05"):
            poster_stem = "module_05"
        elif stem.startswith("ex"):
            poster_stem = stem.split("_")[0]

        poster_dst = DOCS_ASSETS_DIR / f"{poster_stem}_poster.png"

        # Choose safe poster timestamp (8s or midpoint for shorter videos)
        duration = get_video_duration(mp4_file)
        poster_time = min(8.0, max(1.0, duration / 2.0))
        ts_str = f"00:00:{int(poster_time):02d}"

        cmd = [
            FFMPEG, "-y", "-ss", ts_str, "-i", str(mp4_file),
            "-vframes", "1", "-q:v", "2", str(poster_dst)
        ]
        subprocess.run(cmd, capture_output=True)
        print(f"  • {base} -> {poster_dst} ({mp4_file.stat().st_size / 1024:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="Render and synchronize workshop walkthrough videos.")
    parser.add_argument("scenarios", nargs="*", help="Specific scenario names or YAML files to render")
    parser.add_argument("--all", action="store_true", help="Render all scenarios in scenarios/")
    parser.add_argument("--verify", action="store_true", help="Run Gemini multimodal verification loop after rendering")
    parser.add_argument("--dry-run-verify", action="store_true", help="Run verification loop in dry-run mode")
    parser.add_argument("--model", default="gemini-3.1-pro-preview", help="Gemini model for multimodal verification")
    parser.add_argument("--parallel", type=int, default=2, help="Number of parallel rendering workers")
    args = parser.parse_args()

    scenario_files: List[pathlib.Path] = []
    if args.scenarios:
        for s in args.scenarios:
            p = pathlib.Path(s)
            if p.exists() and p.is_file():
                scenario_files.append(p)
            elif (SCENARIOS_DIR / s).exists():
                scenario_files.append(SCENARIOS_DIR / s)
            elif (SCENARIOS_DIR / f"{s}.yaml").exists():
                scenario_files.append(SCENARIOS_DIR / f"{s}.yaml")
            else:
                matches = list(SCENARIOS_DIR.glob(f"*{s}*.yaml"))
                if matches:
                    scenario_files.extend(matches)
                else:
                    print(f"⚠️ Could not find scenario matching '{s}' in {SCENARIOS_DIR}")
    elif args.all or not args.scenarios:
        scenario_files = sorted(SCENARIOS_DIR.glob("*.yaml"))

    if not scenario_files:
        print(f"❌ No scenario manifests found to render in {SCENARIOS_DIR}")
        sys.exit(1)

    print(f"Found {len(scenario_files)} scenarios to render using TermReel.")

    results = []
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = {executor.submit(render_scenario, s): s for s in scenario_files}
        for future in as_completed(futures):
            results.append(future.result())

    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n🏁 Rendering Summary: {passed} passed, {failed} failed out of {len(scenario_files)}")

    extract_posters_and_sync()
    print("🎉 All video assets generated and synchronized!")

    if args.verify or args.dry_run_verify:
        print("\n🔍 Initiating Multimodal Video Verification Loop...")
        verify_script = REPO_ROOT / "tools" / "verify_videos.py"
        verify_cmd = [sys.executable, str(verify_script), "--all", "--model", args.model]
        if args.dry_run_verify:
            verify_cmd.append("--dry-run")
        subprocess.run(verify_cmd)


if __name__ == "__main__":
    main()
