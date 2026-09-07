#!/usr/bin/env python3
"""
Fetch missing RLA discrepancy reports from the Wayback Machine.
Queries the CDX API, picks the most recent 200 capture, and downloads it.
"""
import urllib.request, urllib.error, urllib.parse
import json, time, sys, os

CDX = "https://web.archive.org/cdx/search/cdx"
WB  = "https://web.archive.org/web"

# (label, dest_path, candidate_urls)
TARGETS = [
    (
        "2018 Primary (ballot polling)",
        "2018/ballotPollingAudit/DiscrepancyReport.pdf",
        [
            "https://www.coloradosos.gov/pubs/elections/RLA/2018/primary/DiscrepancyReport.pdf",
            "https://www.coloradosos.gov/pubs/elections/RLA/files/2018/primary/DiscrepancyReport.pdf",
        ],
    ),
    (
        "2018 General (ballot polling)",
        "2018G/ballotPollingAudit/DiscrepancyReport.pdf",
        [
            "https://www.coloradosos.gov/pubs/elections/RLA/2018/general/DiscrepancyReport.pdf",
            "https://www.coloradosos.gov/pubs/elections/RLA/files/2018/general/DiscrepancyReport.pdf",
        ],
    ),
    (
        "2019 Coordinated",
        "2019/DiscrepancyReport.pdf",
        [
            "https://www.coloradosos.gov/pubs/elections/RLA/2019/DiscrepancyReport.pdf",
            "https://www.coloradosos.gov/pubs/elections/RLA/2019/coordinated/DiscrepancyReport.pdf",
            "https://www.coloradosos.gov/pubs/elections/RLA/files/2019/coordinated/DiscrepancyReport.pdf",
        ],
    ),
    (
        "2022 General",
        "2022/general/DiscrepancyReport.pdf",
        [
            "https://www.coloradosos.gov/pubs/elections/RLA/files/2022/general/DiscrepancyReport.pdf",
        ],
    ),
    (
        "2023 Coordinated",
        "2023/coordinated/DiscrepancyReport.pdf",
        [
            "https://www.coloradosos.gov/pubs/elections/RLA/files/2023/coordinated/DiscrepancyReport.pdf",
            "https://www.coloradosos.gov/pubs/elections/RLA/files/2023/coordinated/DiscrepancyReport.xlsx",
        ],
    ),
]

def cdx_lookup(url, retries=4, delay=10):
    # Use output=text (TSV, no header) to avoid JSON envelope ambiguity
    params = "?" + urllib.parse.urlencode({
        "url": url,
        "output": "text",
        "limit": 10,
        "fl": "timestamp,statuscode,mimetype,original",
        "filter": "statuscode:200",
        "collapse": "digest",
    })
    for attempt in range(retries):
        try:
            req = urllib.request.urlopen(CDX + params, timeout=30)
            data = req.read().decode()
            rows = []
            for line in data.strip().splitlines():
                parts = line.split()
                if len(parts) == 4:
                    rows.append(parts)
            return rows
        except Exception as e:
            print(f"    CDX attempt {attempt+1}/{retries} failed: {e}", flush=True)
            if attempt < retries - 1:
                time.sleep(delay)
    return None

def download_from_wayback(timestamp, original_url, dest_path, retries=3, delay=10):
    # Use /if_/ prefix to get the raw file, not the Wayback toolbar-wrapped version
    wb_url = f"{WB}/{timestamp}if_/{original_url}"
    print(f"    Downloading: {wb_url}", flush=True)
    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    for attempt in range(retries):
        try:
            req = urllib.request.urlopen(wb_url, timeout=60)
            content_type = req.headers.get("Content-Type", "")
            data = req.read()
            # Reject HTML responses (Wayback error/redirect pages)
            if "html" in content_type.lower() or (
                len(data) < 100_000 and b"<html" in data[:500].lower()
            ):
                print(f"    Warning: got HTML ({content_type}, {len(data)} bytes) — not a real file", flush=True)
                return False
            with open(dest_path, "wb") as f:
                f.write(data)
            print(f"    Saved {len(data):,} bytes ({content_type}) -> {dest_path}", flush=True)
            return True
        except Exception as e:
            print(f"    Download attempt {attempt+1}/{retries} failed: {e}", flush=True)
            if attempt < retries - 1:
                time.sleep(delay)
    return False

def main():
    for label, dest_path, urls in TARGETS:
        print(f"\n=== {label} ===", flush=True)
        if os.path.exists(dest_path):
            print(f"  Already exists: {dest_path}", flush=True)
            continue

        found = False
        for url in urls:
            print(f"  CDX lookup: {url}", flush=True)
            rows = cdx_lookup(url)
            if rows is None:
                print("  CDX unreachable — aborting this run", flush=True)
                sys.exit(1)
            if not rows:
                print("  No 200 captures found", flush=True)
                continue
            # Pick most recent capture
            best = sorted(rows, key=lambda r: r[0], reverse=True)[0]
            ts, status, mime, orig = best
            print(f"  Best capture: {ts}  {mime}  {orig}", flush=True)
            # Adjust dest extension if xlsx
            actual_dest = dest_path
            if orig.endswith(".xlsx") or "xlsx" in mime:
                actual_dest = dest_path.replace(".pdf", ".xlsx")
            ok = download_from_wayback(ts, orig, actual_dest)
            if ok:
                found = True
                break

        if not found:
            print(f"  Not found in Wayback Machine", flush=True)

if __name__ == "__main__":
    main()
