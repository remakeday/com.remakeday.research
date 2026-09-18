#!/usr/bin/env python3
"""Fail when checked research figure data has drifted from public Markdown."""

import sys

from refresh_research_data import main


if __name__ == "__main__":
    sys.argv.append("--check")
    sys.exit(main())
