"""Download the open Lassa fever surveillance dataset from Zenodo into data/.

Dan-Nwafor, C. (2022). Epidemiological data on Lassa fever in Nigeria, 2018-2021 [dataset].
Zenodo. https://doi.org/10.5281/zenodo.7309567 (CC BY 4.0)
"""
import hashlib
import urllib.request
from pathlib import Path

URL = "https://zenodo.org/api/records/7309567/files/Lassa%20Fever_Dataset_NCDC.sav/content"
TARGET = Path(__file__).resolve().parent / "data" / "Lassa Fever_Dataset_NCDC.sav"
EXPECTED_BYTES = 4494534


def main():
    TARGET.parent.mkdir(exist_ok=True)
    if not TARGET.exists():
        print("Downloading", URL)
        urllib.request.urlretrieve(URL, TARGET)
    size = TARGET.stat().st_size
    md5 = hashlib.md5(TARGET.read_bytes()).hexdigest()
    print(f"{TARGET}  {size:,} bytes  md5={md5}")
    if size != EXPECTED_BYTES:
        raise SystemExit(f"Unexpected file size (expected {EXPECTED_BYTES:,} bytes).")


if __name__ == "__main__":
    main()
