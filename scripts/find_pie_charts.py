#!/usr/bin/env python3
"""
Compatibility wrapper for the old pie-chart command.

The generic image description/metadata utility now lives in:
  scripts/process_images_clip.py
"""

from __future__ import annotations

import sys

from process_images_clip import main


if "--preset" not in sys.argv:
    sys.argv.extend(["--preset", "pie_charts"])

raise SystemExit(main())
