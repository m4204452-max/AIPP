#!/usr/bin/env python3
"""Read a CSV and print mean, min, max for numeric columns.

This script will create a default `data.csv` in the same folder as the
script (Name,Age,Score) if the file doesn't exist. It then reads the
CSV and prints mean, min and max for each numeric column.
"""

import csv
import os
import sys
from statistics import mean
from typing import Dict, Any


def write_sample_csv(path: str) -> None:
    """Write a small default CSV (overwrites if exists)."""
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    rows = [
        ['Name', 'Age', 'Score'],
        ['Alice', '23', '88'],
        ['Bob', '30', '75'],
        ['Carlos', '19', '92'],
        ['Dana', '27', '85'],
        ['Eve', '22', '90'],
        ['Frank', '35', '67'],
        ['Grace', '29', '78'],
        ['Hannah', '21', '95'],
    ]
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def read_csv_stats(path: str) -> Dict[str, Dict[str, float]]:
    """Return mean/min/max for numeric columns in the CSV at `path`.

    Non-numeric cells are ignored.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    numeric: Dict[str, list[float]] = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                if v is None:
                    continue
                s = v.strip()
                if s == '':
                    continue
                try:
                    val = float(s)
                except ValueError:
                    continue
                numeric.setdefault(k, []).append(val)

    stats: Dict[str, Dict[str, float]] = {}
    for col, vals in numeric.items():
        if not vals:
            continue
        stats[col] = {
            'mean': mean(vals),
            'min': min(vals),
            'max': max(vals),
        }
    return stats


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'data.csv')

    if not os.path.exists(csv_path):
        write_sample_csv(csv_path)
        print(f'Wrote sample CSV to: {csv_path}')

    try:
        stats = read_csv_stats(csv_path)
    except Exception as e:
        print('Error reading CSV:', e, file=sys.stderr)
        return 1

    if not stats:
        print('No numeric columns found in', csv_path)
        return 0

    # Print mean, min, max for each numeric column
    for col, s in stats.items():
        print(f"{col}: mean={s['mean']:.2f}, min={s['min']:.2f}, max={s['max']:.2f}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())