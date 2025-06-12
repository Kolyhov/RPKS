"""Benchmark random distance computations."""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path
from typing import Iterable

import numpy as np

from .coords.conversion import spherical_to_cart


def _benchmark_cartesian2d(n: int) -> float:
    x1, y1 = np.random.random((2, n)) * 100
    x2, y2 = np.random.random((2, n)) * 100
    start = time.perf_counter()
    np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    end = time.perf_counter()
    return (end - start) * 1000


def _benchmark_polar(n: int) -> float:
    r1 = np.random.random(n) * 100
    th1 = np.random.random(n) * 2 * np.pi - np.pi
    r2 = np.random.random(n) * 100
    th2 = np.random.random(n) * 2 * np.pi - np.pi
    start = time.perf_counter()
    np.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * np.cos(th1 - th2))
    end = time.perf_counter()
    return (end - start) * 1000


def _benchmark_cartesian3d(n: int) -> float:
    xyz1 = np.random.random((3, n)) * 100
    xyz2 = np.random.random((3, n)) * 100
    start = time.perf_counter()
    np.sqrt(((xyz2 - xyz1) ** 2).sum(axis=0))
    end = time.perf_counter()
    return (end - start) * 1000


def _benchmark_spherical_direct(n: int) -> float:
    r1 = np.random.random(n) * 100
    th1 = np.random.random(n) * 2 * np.pi - np.pi
    ph1 = np.random.random(n) * np.pi - np.pi / 2
    r2 = np.random.random(n) * 100
    th2 = np.random.random(n) * 2 * np.pi - np.pi
    ph2 = np.random.random(n) * np.pi - np.pi / 2
    x1 = r1 * np.cos(ph1) * np.cos(th1)
    y1 = r1 * np.cos(ph1) * np.sin(th1)
    z1 = r1 * np.sin(ph1)
    x2 = r2 * np.cos(ph2) * np.cos(th2)
    y2 = r2 * np.cos(ph2) * np.sin(th2)
    z2 = r2 * np.sin(ph2)
    start = time.perf_counter()
    np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    end = time.perf_counter()
    return (end - start) * 1000


def _benchmark_spherical_surface(n: int) -> float:
    r1 = np.random.random(n) * 100 + 1
    th1 = np.random.random(n) * 2 * np.pi - np.pi
    ph1 = np.random.random(n) * np.pi - np.pi / 2
    r2 = np.random.random(n) * 100 + 1
    th2 = np.random.random(n) * 2 * np.pi - np.pi
    ph2 = np.random.random(n) * np.pi - np.pi / 2
    R = (r1 + r2) / 2
    start = time.perf_counter()
    np.arccos(
        np.sin(ph1) * np.sin(ph2) + np.cos(ph1) * np.cos(ph2) * np.cos(th1 - th2)
    ) * R
    end = time.perf_counter()
    return (end - start) * 1000


BENCH_FUNCS = {
    "cartesian2d": _benchmark_cartesian2d,
    "polar": _benchmark_polar,
    "cartesian3d": _benchmark_cartesian3d,
    "spherical_direct": _benchmark_spherical_direct,
    "spherical_surface": _benchmark_spherical_surface,
}


def run_benchmark(systems: Iterable[str], n: int) -> list[tuple[str, str, int, float]]:
    results = []
    for sys in systems:
        func = BENCH_FUNCS[sys]
        elapsed = func(n)
        calc_type = "direct" if "surface" not in sys else "surface"
        results.append((sys, calc_type, n, elapsed))
    return results


def save_csv(rows: list[tuple[str, str, int, float]], path: Path) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["system", "calc_type", "N", "elapsed_ms"])
        writer.writerows(rows)


def plot_results(rows: list[tuple[str, str, int, float]], path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    labels = [r[0] for r in rows]
    values = [r[3] for r in rows]
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("ms")
    ax.set_title("Benchmark")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=50000)
    parser.add_argument("--out", type=Path, default=Path("results/bench.csv"))
    parser.add_argument("--plot", action="store_true")
    parser.add_argument(
        "--systems",
        nargs="*",
        choices=list(BENCH_FUNCS.keys()),
        default=list(BENCH_FUNCS.keys()),
    )
    args = parser.parse_args(argv)

    rows = run_benchmark(args.systems, args.n)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    save_csv(rows, args.out)
    if args.plot:
        plot_results(rows, args.out.with_suffix(".png"))

    for r in rows:
        print(f"{r[0]:16s} {r[3]:.2f} ms")


if __name__ == "__main__":
    main()
