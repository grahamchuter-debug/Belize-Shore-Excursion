#!/usr/bin/env python3
"""Download images from Wikimedia Commons for Belize site."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"

DOWNLOADS: list[tuple[str, str, str]] = [
    ("hero-belize.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Caye_Caulker_Belize_aerial_%2820688990128%29.jpg/1920px-Caye_Caulker_Belize_aerial_%2820688990128%29.jpg",
     "Wikimedia: Caye Caulker aerial, Belize Barrier Reef"),
    ("belize-cruise-port.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Waterfront_in_Caye_Caulker%2C_Belize.jpg/1920px-Waterfront_in_Caye_Caulker%2C_Belize.jpg",
     "Wikimedia: Belize waterfront (Caye Caulker)"),
    ("belize-port-arrival.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/%22The_Split%22%2C_Caye_Caulker%2C_Belize.jpg/1920px-%22The_Split%22%2C_Caye_Caulker%2C_Belize.jpg",
     "Wikimedia: Caye Caulker The Split, Belize"),
    ("belize-intro.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Lighthouse_Reef_Belize.jpg/1920px-Lighthouse_Reef_Belize.jpg",
     "Wikimedia: Lighthouse Reef / Great Blue Hole area, Belize"),
    ("best-belize-excursions.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Caye_Caulker_Belize_aerial_%2820688990128%29.jpg/1920px-Caye_Caulker_Belize_aerial_%2820688990128%29.jpg",
     "Wikimedia: Caye Caulker representing Belize excursions"),
    ("one-day-belize.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Altun_Ha_Belize_6.jpg/1920px-Altun_Ha_Belize_6.jpg",
     "Wikimedia: Altun Ha ruins Belize"),
    ("belize-cave-tubing.png",
     "https://upload.wikimedia.org/wikipedia/commons/2/2a/Barton_Creek_Cave%2C_Belize_2.jpg",
     "Wikimedia: Barton Creek Cave, Belize (illustrative for cave tubing)"),
    ("belize-zip-line.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Forest_canopy_in_Belize_%285344010084%29.jpg/1920px-Forest_canopy_in_Belize_%285344010084%29.jpg",
     "Wikimedia: Belize rainforest canopy"),
    ("belize-snorkel.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Waterfront_in_Caye_Caulker%2C_Belize.jpg/1920px-Waterfront_in_Caye_Caulker%2C_Belize.jpg",
     "Wikimedia: Caye Caulker snorkel destination"),
    ("belize-beach.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/%22The_Split%22%2C_Caye_Caulker%2C_Belize.jpg/1920px-%22The_Split%22%2C_Caye_Caulker%2C_Belize.jpg",
     "Wikimedia: Caye Caulker beach area Belize"),
    ("altun-ha.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Altun_Ha_Belize_6.jpg/1920px-Altun_Ha_Belize_6.jpg",
     "Wikimedia: Altun Ha Mayan ruins Belize"),
    ("lamanai.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Lamanai_01.JPG/1920px-Lamanai_01.JPG",
     "Wikimedia: Lamanai Mayan site Belize"),
    ("belize-zoo.png",
     "https://upload.wikimedia.org/wikipedia/commons/0/0b/Jaguar_%282254169745%29.jpg",
     "Wikimedia: Jaguar at Lamanai Belize (wildlife illustrative)"),
    ("belize-jeep.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Forest_canopy_in_Belize_%285344010084%29.jpg/1920px-Forest_canopy_in_Belize_%285344010084%29.jpg",
     "Wikimedia: Belize jungle (illustrative for Jeep tours)"),
    ("belize-private.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Caye_Caulker_Belize_aerial_%2820688990128%29.jpg/1920px-Caye_Caulker_Belize_aerial_%2820688990128%29.jpg",
     "Wikimedia: Belize excursion destination"),
    ("belize-faq.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Waterfront_in_Caye_Caulker%2C_Belize.jpg/1920px-Waterfront_in_Caye_Caulker%2C_Belize.jpg",
     "Wikimedia: Belize waterfront for FAQ page"),
    ("belize-ruins.png",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Altun_Ha_Belize_6.jpg/1920px-Altun_Ha_Belize_6.jpg",
     "Wikimedia: Mayan ruins Belize"),
]


def download(filename: str, url: str, note: str) -> bool:
    dest = IMAGES / filename
    print(f"  {filename}")
    print(f"    {note}")
    result = subprocess.run(
        ["curl", "-fsSL", "-o", str(dest), url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"    FAILED: {result.stderr.strip()}", file=sys.stderr)
        return False
    size = dest.stat().st_size
    if size < 10_000:
        print(f"    WARNING: small file ({size} bytes)", file=sys.stderr)
    print(f"    OK ({size // 1024} KB)")
    return True


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    print("Downloading Belize images…")
    failed = 0
    for i, (filename, url, note) in enumerate(DOWNLOADS):
        if i:
            time.sleep(1.5)
        if not download(filename, url, note):
            failed += 1
    if failed:
        print(f"Warning: {failed} download(s) failed — placeholders remain for those files.")
    else:
        print("Done.")


if __name__ == "__main__":
    main()
