import csv
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://storage.googleapis.com/public-datasets-lila/caltech-unzipped/cct_images"
OUTPUT_DIR = "data/images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read selected image names
with open("data/subset.csv", newline="") as file:
    rows = list(csv.DictReader(file))

def download_image(row):
    filename = row["file_name"]
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Skip images already downloaded
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return "Skipped"

    url = f"{BASE_URL}/{filename}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, "wb") as image:
                image.write(response.content)

            return "Downloaded"

        except requests.RequestException as e:
            if attempt == 2:
                print(f"\nFailed: {filename} | Error: {e}")
                return "Failed"

print(f"Starting download of {len(rows)} images...")

downloaded = 0
skipped = 0
failed = 0

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(download_image, row) for row in rows]

    for i, future in enumerate(as_completed(futures), 1):
        result = future.result()

        if result == "Downloaded":
            downloaded += 1
        elif result == "Skipped":
            skipped += 1
        else:
            failed += 1

        if i % 50 == 0 or i == len(rows):
            print(
                f"Progress: {i}/{len(rows)} | "
                f"Downloaded: {downloaded} | "
                f"Skipped: {skipped} | "
                f"Failed: {failed}"
            )

print("\nDownload complete!")
print("Downloaded:", downloaded)
print("Skipped:", skipped)
print("Failed:", failed)