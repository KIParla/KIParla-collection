#!/usr/bin/env python3
"""
Merge TSV files from an explicit list, ensuring unique 'code'.

Default: keep only columns common to every file (must include 'code').
Optional: --columns "col1,col2,..." to keep exactly those columns
          (script ensures 'code' is included; errors if a file lacks it).

Usage:
    python merge_tsv_simple.py --output merged.tsv file1.tsv file2.tsv file3.tsv
    python merge_tsv_simple.py --output merged.tsv --columns "id,name,date" a.tsv b.tsv
"""

import argparse
import os
import sys
import pandas as pd

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("files", nargs="+", help="Input TSV files")
	ap.add_argument("--output", "-o", required=True, help="Output TSV path")
	ap.add_argument("--columns", help="Comma-separated list of columns to keep (e.g., 'id,name,date')")
	args = ap.parse_args()

	# Validate paths
	missing_paths = [p for p in args.files if not os.path.isfile(p)]
	if missing_paths:
		print("These paths do not exist or are not files:\n  " + "\n  ".join(missing_paths), file=sys.stderr)
		sys.exit(1)

	# Load all files as strings, keep empty strings for missing cells
	dfs = []
	for path in args.files:
		try:
			df = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
		except Exception as ex:
			print(f"Failed to read {path}: {ex}", file=sys.stderr)
			sys.exit(2)
		# Ensure each file has 'code'
		if "code" not in df.columns:
			print(f"{os.path.basename(path)} is missing required 'code' column.", file=sys.stderr)
			sys.exit(3)
		dfs.append(df)

	# Determine columns to keep

	cols = [c.strip() for c in args.columns.split(",") if c.strip()]
	# Ensure 'code' is included
	if "code" not in cols:
		cols = ["code"] + cols
	# Check all files contain all requested columns
	for path, df in zip(args.files, dfs):
		missing = [c for c in cols if c not in df.columns]
		if missing:
			print(path)
			print(f"{os.path.basename(path)} is missing columns: {', '.join(missing)}", file=sys.stderr)
			sys.exit(4)
	selected = [df[cols] for df in dfs]

	# Merge
	merged = pd.concat(selected, ignore_index=True)

	# Enforce unique 'code' (keep first occurrence by input order)
	before = len(merged)
	merged = merged.drop_duplicates(subset=["code"], keep="first")
	after = len(merged)

	merged.to_csv(args.output, sep="\t", index=False)
	print(f"Merged {len(dfs)} file(s) into {args.output}")
	print(f"Rows before de-dup: {before} | after: {after}")
	print(f"Columns: {', '.join(merged.columns)}")

if __name__ == "__main__":
	main()