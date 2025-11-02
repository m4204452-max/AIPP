#!/usr/bin/env python3
"""Calculate the sum of squares of numbers.

This program can work with:
  - A list of numbers provided via command-line arguments
  - Interactive input (entering numbers one by one)
  - A CSV file containing numeric columns
"""

import argparse
import csv
import os
import sys
from typing import List


def sum_of_squares(numbers: List[float]) -> float:
    """Calculate the sum of squares for a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        Sum of squares of all numbers
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate sum of squares: empty list")
    return sum(x * x for x in numbers)


def interactive_mode() -> int:
    """Interactive mode: prompt user for numbers."""
    print("Sum of Squares Calculator")
    print("Enter numbers one per line. Enter an empty line or 'q' to finish.\n")
    
    numbers = []
    try:
        while True:
            line = input("Enter a number (or press Enter/type 'q' to calculate): ").strip()
            if not line or line.lower() == 'q':
                break
            try:
                num = float(line)
                numbers.append(num)
            except ValueError:
                print(f"Invalid number: {line}. Please enter a valid number.")
    except (EOFError, KeyboardInterrupt):
        print()
    
    if not numbers:
        print("No numbers entered.")
        return 1
    
    try:
        result = sum_of_squares(numbers)
        print(f"\nSum of squares: {result:.4f}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main(argv: List[str] | None = None) -> int:
    """Main entry point for the sum of squares calculator."""
    parser = argparse.ArgumentParser(
        description='Calculate the sum of squares of numbers',
        epilog='If no arguments are provided, enters interactive mode'
    )
    parser.add_argument('numbers', nargs='*', type=float, 
                       help='Numbers to calculate sum of squares')
    parser.add_argument('-f', '--file', metavar='CSV_FILE',
                       help='Read numbers from a CSV file')
    parser.add_argument('-c', '--column', metavar='COLUMN', default='Value',
                       help='Column name to read from CSV (default: Value)')
    
    args = parser.parse_args(argv if argv is not None else None)
    
    # If numbers provided via CLI
    if args.numbers:
        try:
            result = sum_of_squares(args.numbers)
            print(f"Sum of squares: {result:.4f}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    # If CSV file provided
    if args.file:
        try:
            numbers = []
            with open(args.file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if args.column not in reader.fieldnames:
                    print(f"Error: Column '{args.column}' not found in CSV.")
                    print(f"Available columns: {', '.join(reader.fieldnames)}")
                    return 1
                
                for row in reader:
                    try:
                        val = float(row[args.column])
                        numbers.append(val)
                    except (ValueError, KeyError):
                        continue
            
            if not numbers:
                print(f"No valid numbers found in column '{args.column}'")
                return 1
            
            result = sum_of_squares(numbers)
            print(f"Sum of squares from {args.file} (column '{args.column}'): {result:.4f}")
            return 0
            
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading CSV file: {e}", file=sys.stderr)
            return 1
    
    # Interactive mode
    return interactive_mode()


if __name__ == '__main__':
    raise SystemExit(main())

