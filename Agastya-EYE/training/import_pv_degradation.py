"""Import the DOI-pinned, CC BY 4.0 PV cell degradation benchmark."""

import argparse
import hashlib
import json
import shutil
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_URL = "https://data.mendeley.com/public-api/zip/pxyzzkbs4b/download/1"
ARCHIVE_SHA256 = "b24ce7811318d6776fa4b780fb787bc96685ec203108b4dc11f39f6d95ab7427"
DOI = "10.17632/pxyzzkbs4b.1"
TOP_FOLDER = "PV_EL_HDR_BW_Test_DB"
DEFAULT_ARCHIVE = ROOT / "datasets" / ".cache" / "PV_EL_HDR_BW_Test_DB_v1.zip"
OUTPUT = ROOT / "datasets" / "raw" / "pv_el_hdr_bw_v1"
MAX_UNCOMPRESSED_BYTES = 5_000_000_000


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_archive(destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".download")
    request = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "Agastya-EYE-research/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        if sha256_file(temporary) != ARCHIVE_SHA256:
            raise ValueError("download checksum does not match the pinned Mendeley Data v1 archive")
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return destination


def safe_member_path(member_name):
    member = PurePosixPath(member_name)
    if ("\\" in member_name or ":" in member_name or member.is_absolute()
            or not member.parts or any(part in ("", ".", "..") for part in member.parts)):
        raise ValueError(f"unsafe archive path: {member_name!r}")
    if member.parts[0] != TOP_FOLDER:
        raise ValueError(f"unexpected top-level archive folder: {member_name!r}")
    relative = Path(*member.parts[1:])
    if not relative.parts:
        return None
    return relative


def import_archive(archive_path, output=OUTPUT):
    archive_path = Path(archive_path).resolve()
    output = Path(output).resolve()
    raw_root = (ROOT / "datasets" / "raw").resolve()
    if output == raw_root or not output.is_relative_to(raw_root):
        raise ValueError("import output must stay inside datasets/raw")
    if output.exists():
        raise FileExistsError(f"{output} already exists; move it yourself before re-importing")
    if not archive_path.is_file():
        raise FileNotFoundError(f"archive not found: {archive_path}")
    actual_hash = sha256_file(archive_path)
    if actual_hash != ARCHIVE_SHA256:
        raise ValueError("archive checksum differs from the DOI-pinned Mendeley Data v1 file")

    staging = output.with_name(output.name + ".staging")
    if staging.exists():
        raise FileExistsError(f"staging path already exists: {staging}")
    staging.mkdir(parents=True)
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            total_size = sum(info.file_size for info in infos)
            if total_size > MAX_UNCOMPRESSED_BYTES or len(infos) > 1000:
                raise ValueError("archive exceeds the importer size or member-count limit")
            extracted = []
            for info in infos:
                relative = safe_member_path(info.filename)
                if relative is None or info.is_dir():
                    continue
                mode = info.external_attr >> 16
                if mode and (mode & 0o170000) == 0o120000:
                    raise ValueError(f"symbolic link is not allowed in dataset archive: {info.filename}")
                destination = staging / relative
                if not destination.resolve().is_relative_to(staging.resolve()):
                    raise ValueError(f"archive path escapes import directory: {info.filename}")
                destination.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, destination.open("wb") as target:
                    shutil.copyfileobj(source, target)
                extracted.append(relative.as_posix())

        csv_path = staging / "data" / "ELPV_DATA_FULL.CSV"
        image_count = sum(1 for path in (staging / "images").rglob("*.png") if path.is_file())
        if not csv_path.is_file() or image_count != 252 or not (staging / "LICENSE.txt").is_file():
            raise ValueError(f"dataset integrity check failed (CSV present, PNG count={image_count}, license present)")
        manifest = {
            "source": "PV_EL_HDR_BW_Test_DB",
            "version": 1,
            "doi": DOI,
            "source_url": "https://data.mendeley.com/datasets/pxyzzkbs4b/1",
            "license": "CC BY 4.0",
            "archive_sha256": actual_hash,
            "extracted_files": len(extracted),
            "image_count": image_count,
            "imported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "citation": "Polenghi et al. (2026), Mendeley Data v1, doi:10.17632/pxyzzkbs4b.1",
        }
        (staging / "agastya_import.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        staging.replace(output)
        return manifest
    except Exception:
        shutil.rmtree(staging)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--download", action="store_true", help="Download the pinned Mendeley v1 ZIP if missing")
    args = parser.parse_args()
    try:
        archive_path = args.archive
        if not archive_path.is_file() and args.download:
            archive_path = download_archive(archive_path)
        result = import_archive(archive_path)
        print(json.dumps({"output": str(OUTPUT), **result}, indent=2))
    except (OSError, ValueError, zipfile.BadZipFile, urllib.error.URLError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
