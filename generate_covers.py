#!/usr/bin/env python3
"""Generate covers for MAGA Rally Warriors coloring books."""

import os
import requests
import urllib.parse
from pathlib import Path
import time

# Book titles
BOOKS = [
    "Orange Snowflakes",
    "The Poorly Educated",
    "It Can Only Good Happen",
    "The Covfefe Kool-Aid",
    "Leave the Orange Pedo Alone",
    "Cosplaytriots",
    "Freedumb Fighters",
    "Many People Are Saying",
    "The Grift That Keeps Grifting",
    "Big Brain Energy",
    "Very Stable Geniuses",
    "Alternative Facts",
    "The Best People",
    "The Best Words",
    "Hamberder Time",
    "Fake News Fighters",
    "The Deep State Hunters",
    "MAGA Murika",
    "Space Force Cadets",
    "All Aboard the Trump Train",
    "People of MAGA",
]

def generate_cover(title: str, output_dir: Path) -> bool:
    """Generate a cover image for a book."""

    # Cover prompt - colorful, eye-catching, satirical
    prompt = f"""book cover design for adult coloring book titled "MAGA Rally Warriors: {title}",
    featuring patriotic american flag themed crowd scene with diverse stereotypical trump rally attendees,
    red white and blue color scheme, bold typography, professional book cover layout,
    satirical political humor style, vibrant colors, eye-catching design for amazon kindle"""

    encoded_prompt = urllib.parse.quote(prompt)

    # KDP cover size (6x9 book = 2560x1600 or similar aspect ratio)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1600&height=2560&nologo=true&model=flux"

    try:
        print(f"  Generating cover for: {title}")
        response = requests.get(url, timeout=180)

        if response.status_code == 200 and len(response.content) > 10000:
            # Save cover
            safe_title = title.replace(" ", "_").replace("'", "").replace(":", "")
            cover_path = output_dir / f"cover_{safe_title}.png"
            cover_path.write_bytes(response.content)
            print(f"  ✓ Saved: {cover_path.name}")
            return True
        else:
            print(f"  ✗ Failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", type=str, help="Generate cover for specific title")
    parser.add_argument("--output", type=str, default="output/covers", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.title:
        titles = [args.title]
    else:
        titles = BOOKS

    print(f"Generating {len(titles)} covers...")

    success = 0
    for title in titles:
        if generate_cover(title, output_dir):
            success += 1
        time.sleep(2)  # Rate limiting

    print(f"\nDone! Generated {success}/{len(titles)} covers")
    print(f"Covers saved to: {output_dir}")


if __name__ == "__main__":
    main()
