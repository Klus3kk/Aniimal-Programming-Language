#!/usr/bin/env python3
import csv
import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
BENCH_DIR = ROOT / "benchmarks"
CPP_DIR = BENCH_DIR / "cpp"
PY_DIR = BENCH_DIR / "python"
ANIMAL_DIR = BENCH_DIR / "animal"
OUT_DIR = BENCH_DIR / "results"
BIN_DIR = BENCH_DIR / "bin"
DOCS_STATIC_DIR = ROOT / "docs" / "_static" / "benchmarks"


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (BIN_DIR / "cpp").mkdir(parents=True, exist_ok=True)
    DOCS_STATIC_DIR.mkdir(parents=True, exist_ok=True)


def compile_cpp() -> List[Tuple[str, Path]]:
    targets = [
        ("bubble_sort", CPP_DIR / "bubble_sort.cpp"),
        ("fibonacci", CPP_DIR / "fibonacci.cpp"),
        ("prime_factor", CPP_DIR / "prime_factor.cpp"),
    ]
    binaries: List[Tuple[str, Path]] = []

    cxx = which("g++") or which("clang++")
    if not cxx:
        print("[warn] No C++ compiler (g++/clang++) found in PATH. Skipping C++ compile.")
        return binaries

    for name, src in targets:
        out = BIN_DIR / "cpp" / (name + (".exe" if os.name == "nt" else ""))
        cmd = [cxx, "-O3", str(src), "-o", str(out)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            binaries.append((name, out))
        except subprocess.CalledProcessError as e:
            print(f"[warn] Failed to compile {src.name}: {e}")
    return binaries


def get_python_cmd() -> List[str]:
    # Prefer current interpreter for consistency
    return [sys.executable]


def get_animal_cmd() -> Optional[str]:
    # Expect an 'animal' CLI in PATH; user can build with: go build -o animal ./cmd/animal
    return which("animal")


def measure_process(cmd: List[str], timeout: Optional[float] = None) -> Tuple[float, Optional[int], int]:
    """Run a command and return (elapsed_seconds, peak_memory_bytes or None, returncode).

    On Windows, tracks Peak Working Set via polling the process working set.
    On other OSes, returns None for memory unless psutil or similar is added later.
    """
    start = time.perf_counter()

    if os.name == "nt":
        peak = _measure_process_win(cmd, timeout)
        elapsed = time.perf_counter() - start
        return elapsed, peak[0], peak[1]
    else:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        elapsed = time.perf_counter() - start
        # Best-effort: memory not measured cross-platform without extra deps
        return elapsed, None, proc.returncode


def _measure_process_win(cmd: List[str], timeout: Optional[float]) -> Tuple[Optional[int], int]:
    """Windows-specific runner that samples WorkingSetSize to approximate peak.

    Returns (peak_bytes or None, returncode).
    """
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    psapi = ctypes.WinDLL('psapi', use_last_error=True)

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    GetProcessMemoryInfo = psapi.GetProcessMemoryInfo
    GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESS_MEMORY_COUNTERS), wintypes.DWORD]
    GetProcessMemoryInfo.restype = wintypes.BOOL

    OpenProcess = kernel32.OpenProcess
    OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    OpenProcess.restype = wintypes.HANDLE

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = [wintypes.HANDLE]
    CloseHandle.restype = wintypes.BOOL

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    peak = 0
    try:
        handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, proc.pid)
        if handle:
            try:
                counters = PROCESS_MEMORY_COUNTERS()
                counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
                # Poll until process exit or timeout
                start = time.perf_counter()
                while True:
                    # Update working set to approximate peak during runtime
                    if GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                        if counters.WorkingSetSize > peak:
                            peak = int(counters.WorkingSetSize)
                    # Check exit / timeout
                    ret = proc.poll()
                    if ret is not None:
                        # One final read for PeakWorkingSetSize if available
                        if GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                            peak = max(peak, int(counters.PeakWorkingSetSize))
                        break
                    if timeout is not None and (time.perf_counter() - start) > timeout:
                        proc.kill()
                        proc.wait()
                        break
                    time.sleep(0.005)
            finally:
                CloseHandle(handle)
        else:
            # Fallback: wait without memory
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait()
    finally:
        return peak or None, proc.returncode


def run_language_cmds(algorithm: str, cpp_bin_map: dict, iterations: int) -> List[dict]:
    results: List[dict] = []

    # Build commands per language
    cmds = []

    # C++
    cpp_bin = cpp_bin_map.get(algorithm)
    if cpp_bin and cpp_bin.exists():
        cmds.append(("cpp", [str(cpp_bin)]))
    else:
        print(f"[warn] Skipping C++ for {algorithm} (no binary)")

    # Python
    py_cmd = get_python_cmd()
    py_script = PY_DIR / f"{algorithm}.py"
    if py_script.exists():
        cmds.append(("python", py_cmd + [str(py_script)]))
    else:
        print(f"[warn] Missing Python script for {algorithm}")

    # Animal
    animal_cli = get_animal_cmd()
    animal_prog = ANIMAL_DIR / f"{algorithm}.anml"
    if animal_cli and animal_prog.exists():
        cmds.append(("animal", [animal_cli, str(animal_prog)]))
    else:
        if not animal_cli:
            print("[warn] 'animal' CLI not found in PATH. Skipping Animal benchmarks.")
        elif not animal_prog.exists():
            print(f"[warn] Missing Animal program for {algorithm}")

    # Execute each command N iterations
    for lang, cmd in cmds:
        total_elapsed = 0.0
        peak_mem = 0
        all_ok = True
        for _ in range(iterations):
            elapsed, mem, rc = measure_process(cmd)
            total_elapsed += elapsed
            if mem:
                peak_mem = max(peak_mem, mem)
            if rc != 0:
                all_ok = False
        avg_ms = (total_elapsed / iterations) * 1000.0
        results.append({
            "algorithm": algorithm,
            "language": lang,
            "iterations": iterations,
            "avg_time_ms": f"{avg_ms:.3f}",
            "total_time_ms": f"{total_elapsed*1000.0:.3f}",
            "peak_memory_bytes": str(peak_mem) if peak_mem else "",
            "success": str(all_ok),
        })
    return results


def write_csv(rows: List[dict], path: Path) -> None:
    if not rows:
        return
    fieldnames = [
        "algorithm",
        "language",
        "iterations",
        "avg_time_ms",
        "total_time_ms",
        "peak_memory_bytes",
        "success",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    rows: List[dict] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def generate_svg_charts(csv_path: Path, out_dir: Path) -> List[Path]:
    """Create simple SVG bar charts for time and memory per algorithm without extra deps."""
    rows = parse_csv(csv_path)
    # Group by algorithm
    algos = {}
    for r in rows:
        algos.setdefault(r["algorithm"], []).append(r)

    generated: List[Path] = []
    for algo, entries in algos.items():
        # Time chart
        time_svg = out_dir / f"{algo}_time.svg"
        _write_bar_svg(
            time_svg,
            title=f"{algo} - Average Time (ms)",
            series=[(e["language"], float(e["avg_time_ms"])) for e in entries],
            unit="ms",
        )
        generated.append(time_svg)

        # Memory chart (if any memory present)
        mem_values = []
        for e in entries:
            v = e.get("peak_memory_bytes") or ""
            if v:
                mem_values.append((e["language"], int(v) / (1024*1024)))
        if mem_values:
            mem_svg = out_dir / f"{algo}_memory.svg"
            _write_bar_svg(
                mem_svg,
                title=f"{algo} - Peak Memory (MB)",
                series=mem_values,
                unit="MB",
            )
            generated.append(mem_svg)
    return generated


def _write_bar_svg(path: Path, title: str, series: List[Tuple[str, float]], unit: str) -> None:
    width, height = 640, 360
    margin = 60
    bar_gap = 20
    bar_width = 60
    label_gap = 8
    max_val = max((v for _, v in series), default=1.0)
    chart_w = width - 2*margin
    chart_h = height - 2*margin

    # Scale function
    def y(val: float) -> float:
        if max_val == 0:
            return height - margin
        return height - margin - (val / max_val) * chart_h

    # Compute bar positions
    total_bars = len(series)
    if total_bars == 0:
        return
    total_w = total_bars * bar_width + (total_bars - 1) * bar_gap
    start_x = (width - total_w) / 2

    # SVG assembly
    lines = []
    lines.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>")
    lines.append(f"<style> .title{{font: bold 16px sans-serif}} .axis{{stroke:#333;stroke-width:1}} .bar{{fill:#4C78A8}} .label{{font: 12px sans-serif; fill:#333}} .value{{font: 11px sans-serif; fill:#111}} </style>")
    lines.append(f"<text x='{width/2}' y='{margin/2}' text-anchor='middle' class='title'>{title}</text>")

    # Axes
    lines.append(f"<line class='axis' x1='{margin}' y1='{height-margin}' x2='{width-margin}' y2='{height-margin}' />")
    lines.append(f"<line class='axis' x1='{margin}' y1='{margin}' x2='{margin}' y2='{height-margin}' />")

    # Bars
    for i, (label, value) in enumerate(series):
        x = start_x + i * (bar_width + bar_gap)
        top = y(value)
        bar_h = height - margin - top
        lines.append(f"<rect class='bar' x='{x}' y='{top}' width='{bar_width}' height='{bar_h}' />")
        lines.append(f"<text class='label' x='{x + bar_width/2}' y='{height - margin + label_gap + 12}' text-anchor='middle'>{label}</text>")
        lines.append(f"<text class='value' x='{x + bar_width/2}' y='{top - 4}' text-anchor='middle'>{value:.3f} {unit}</text>")

    # Max value marker
    lines.append(f"<text class='label' x='{margin - 8}' y='{margin + 12}' text-anchor='end'>{max_val:.3f} {unit}</text>")

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def generate_png_charts(csv_path: Path, out_dir: Path) -> List[Path]:
    """Create cartoon-styled PNG bar charts using Pillow (if installed)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        print("[warn] Pillow (PIL) not available. Skipping PNG chart generation.\n"
              "       Install with: python -m pip install pillow")
        return []

    rows = parse_csv(csv_path)
    algos = {}
    for r in rows:
        algos.setdefault(r["algorithm"], []).append(r)

    generated: List[Path] = []
    for algo, entries in algos.items():
        time_series = [(e["language"], float(e["avg_time_ms"])) for e in entries]
        mem_values = []
        for e in entries:
            v = e.get("peak_memory_bytes") or ""
            if v:
                mem_values.append((e["language"], int(v) / (1024*1024)))

        if time_series:
            p = out_dir / f"{algo}_time.png"
            _draw_cartoon_png(
                p,
                title=f"{algo} — Average Time (ms)",
                series=time_series,
                unit="ms",
            )
            generated.append(p)

        if mem_values:
            p = out_dir / f"{algo}_memory.png"
            _draw_cartoon_png(
                p,
                title=f"{algo} — Peak Memory (MB)",
                series=mem_values,
                unit="MB",
            )
            generated.append(p)
    return generated


def _draw_cartoon_png(path: Path, title: str, series: List[Tuple[str, float]], unit: str) -> None:
    # Lazy import to keep top-level clean
    from PIL import Image, ImageDraw, ImageFont
    import random

    random.seed(42)
    width, height = 900, 520
    margin = 80
    bar_gap = 40
    bar_width = 90
    chart_w = width - 2 * margin
    chart_h = height - 2 * margin
    bg = (250, 247, 240)
    ink = (40, 40, 40)
    grid = (210, 205, 195)
    shadow = (120, 120, 120, 90)

    # Color palette per language
    palette = {
        "cpp": (76, 120, 168),
        "python": (255, 170, 51),
        "animal": (120, 190, 125),
    }

    # Prep image and drawing context
    img = Image.new("RGBA", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Fonts (fallback to default if custom not available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        label_font = ImageFont.truetype("arial.ttf", 16)
        value_font = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        value_font = ImageFont.load_default()

    # Title
    tw, th = draw.textbbox((0, 0), title, font=title_font)[2:]
    draw.text(((width - tw) / 2, 20), title, font=title_font, fill=ink)

    # Axes area
    xmin, ymin = margin, margin
    xmax, ymax = width - margin, height - margin

    # Grid lines
    max_val = max((v for _, v in series), default=1.0)
    for i in range(6):
        y = ymax - i * (chart_h / 5)
        draw.line([(xmin, y), (xmax, y)], fill=grid, width=1)
        val = max_val * i / 5
        label = f"{val:.1f} {unit}"
        lb = draw.textbbox((0, 0), label, font=label_font)
        draw.text((xmin - lb[2] - 10, y - 8), label, font=label_font, fill=ink)

    # Cartoon axes (hand-drawn wobble)
    def wobble_line(x1, y1, x2, y2, k=3, n=12):
        import math
        for _ in range(2):
            pts = []
            for i in range(n + 1):
                t = i / n
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                x += random.uniform(-k, k)
                y += random.uniform(-k, k)
                pts.append((x, y))
            draw.line(pts, fill=ink, width=2)

    wobble_line(xmin, ymax, xmax, ymax)
    wobble_line(xmin, ymin, xmin, ymax)

    # Bars
    total_bars = len(series)
    total_w = total_bars * bar_width + (total_bars - 1) * bar_gap
    start_x = xmin + (chart_w - total_w) / 2

    def y(val: float) -> float:
        if max_val == 0:
            return ymax
        return ymax - (val / max_val) * chart_h

    for i, (label, value) in enumerate(series):
        cx = start_x + i * (bar_width + bar_gap)
        top = y(value)
        bar_rect = [cx, top, cx + bar_width, ymax]

        # Drop shadow
        shadow_offset = (6, 6)
        shadow_rect = [bar_rect[0] + shadow_offset[0], bar_rect[1] + shadow_offset[1], bar_rect[2] + shadow_offset[0], bar_rect[3] + shadow_offset[1]]
        draw.rectangle(shadow_rect, fill=shadow)

        # Main fill
        color = palette.get(label.lower(), (150, 150, 220))
        draw.rectangle(bar_rect, fill=color)

        # Cartoon outline (multi-pass wobbly)
        for _ in range(2):
            k = 2.5
            outline = [
                (bar_rect[0] + random.uniform(-k, k), bar_rect[1] + random.uniform(-k, k)),
                (bar_rect[2] + random.uniform(-k, k), bar_rect[1] + random.uniform(-k, k)),
                (bar_rect[2] + random.uniform(-k, k), bar_rect[3] + random.uniform(-k, k)),
                (bar_rect[0] + random.uniform(-k, k), bar_rect[3] + random.uniform(-k, k)),
                (bar_rect[0] + random.uniform(-k, k), bar_rect[1] + random.uniform(-k, k)),
            ]
            draw.line(outline, fill=ink, width=2, joint="curve")

        # Value label above bar
        val_text = f"{value:.3f} {unit}"
        vb = draw.textbbox((0, 0), val_text, font=value_font)
        draw.text((cx + bar_width / 2 - (vb[2] / 2), top - 22), val_text, font=value_font, fill=ink)

        # X label
        lb = draw.textbbox((0, 0), label, font=label_font)
        draw.text((cx + bar_width / 2 - (lb[2] / 2), ymax + 10), label, font=label_font, fill=ink)

    # Save as PNG
    img.convert("RGB").save(path, format="PNG", optimize=True)


def main(argv: List[str]) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Run Animal vs Python vs C++ benchmarks")
    parser.add_argument("--iterations", type=int, default=50, help="How many process runs per language")
    parser.add_argument("--no-cpp", action="store_true", help="Skip compiling/running C++")
    parser.add_argument("--no-animal", action="store_true", help="Skip Animal benchmarks")
    parser.add_argument("--csv", type=str, default=str(OUT_DIR / "benchmarks.csv"), help="Output CSV path")
    parser.add_argument("--charts", action="store_true", help="Generate SVG charts into docs/_static/benchmarks")
    parser.add_argument("--png-charts", action="store_true", help="Generate PNG charts into docs/_static/benchmarks (requires Pillow)")
    args = parser.parse_args(argv)

    ensure_dirs()

    cpp_bins = {}
    if not args.no_cpp:
        for name, path in compile_cpp():
            cpp_bins[name] = path

    algorithms = ["bubble_sort", "fibonacci", "prime_factor"]
    rows: List[dict] = []
    for algo in algorithms:
        rows.extend(run_language_cmds(algo, cpp_bins, iterations=args.iterations))

    csv_path = Path(args.csv)
    write_csv(rows, csv_path)
    print(f"[ok] Wrote CSV: {csv_path}")

    if args.charts:
        generated = generate_svg_charts(csv_path, DOCS_STATIC_DIR)
        for p in generated:
            print(f"[ok] Wrote chart: {p}")

    if args.png_charts:
        generated_png = generate_png_charts(csv_path, DOCS_STATIC_DIR)
        for p in generated_png:
            print(f"[ok] Wrote PNG chart: {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
