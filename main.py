"""Entrypoint for the news-image-20261124 entry.

Builds the daily news infographic: "The World in One Day — Tuesday,
24 November 2026" (1024x1024, six verified stories). Run: python3 main.py
"""
from make_entry import generate

if __name__ == "__main__":
    generate()
    print("entry.png ready")
