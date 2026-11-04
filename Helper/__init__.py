"""Shared helpers for all WeekN folders.

Importing anything from this package loads Helper/.env, so callers don't need
to call load_dotenv() themselves.
"""
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
