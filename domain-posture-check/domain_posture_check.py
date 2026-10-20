#!/usr/bin/env python3
"""Check basic DNS, HTTPS, TLS, and response-header posture for one domain."""

from __future__ import annotations

import argparse
import json
import socket
import ssl
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

HEADERS_TO_CHECK = {
    "strict-transport-security": "HSTS",
    "content-security-policy": "Content-Security-Policy",
    "x-content-type-options": "X-Content-Type-Options",
    "referrer-policy": "Referrer-Policy",
    "permissions-policy": "Permissions-Policy",
}


def normalize_host(value: str) -> str:
    """Accept a hostname or URL and return a normalized hostname."""
    candidate = value.strip()
    if not candidate:
        raise ValueError("Please provide a domain name.")

    parsed = urlsplit(candidate if "://" in candidate else f"//{candidate}")
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise ValueError("Provide a domain only, without a path, query, or fragment.")
    host = parsed.hostname
    if not host:
        raise ValueError("Could not read a hostname from that input.")
    try:
        normalized = host.encode("idna").decode("ascii").lower().rstrip(".")
    except UnicodeError as exc:
        raise ValueError("That hostname could not be converted to a valid domain.") from exc
    if len(normalized) > 253 or any(not label or len(label) > 63 for label in normalized.split(".")):
        raise ValueError("That hostname does not look valid.")
    return normalized


def resolve_host(host: str) -> list[str]:
    results = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    return sorted({item[4][0] for item in results})


def check_tls(host: str, timeout: float) -> dict[str, str | bool]:
    context = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout=timeout) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=host) as tls_socket:
            cert = tls_socket.getpeercert()
    expires = cert.get("notAfter")
    result: dict[str, str | bool] = {"validated": True}
    if expires:
        expiry = datetime.strptime(expires, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        result["expires_utc"] = expiry.isoformat()
        result["days_remaining"] = (expiry - datetime.now(timezone.utc)).days
    return result


def check_https_headers(host: str, timeout: float) -> dict[str, object]:
    request = Request(
        f"https://{host}/",
        method="HEAD",
        headers={"User-Agent": "DomainPostureCheck/1.0 (educational security project)"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            headers = {key.lower(): value for key, value in response.headers.items()}
    except HTTPError as exc:
        status = exc.code
        headers = {key.lower(): value for key, value in exc.headers.items()}
    return {
        "status": status,
        "present": {label: name in headers for name, label in HEADERS_TO_CHECK.items()},
    }


def build_report(host: str, timeout: float) -> dict[str, object]:
    report: dict[str, object] = {"domain": host}
    try:
        report["dns"] = {"resolved": True, "addresses": resolve_host(host)}
    except (socket.gaierror, OSError) as exc:
        report["dns"] = {"resolved": False, "error": str(exc)}
        return report

    try:
        report["tls"] = check_tls(host, timeout)
    except (OSError, ssl.SSLError, ValueError) as exc:
        report["tls"] = {"validated": False, "error": str(exc)}

    try:
        report["https"] = check_https_headers(host, timeout)
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        report["https"] = {"reachable": False, "error": str(exc)}
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check DNS, HTTPS, TLS, and selected response headers for one domain."
    )
    parser.add_argument("domain", help="domain name to check, such as example.com")
    parser.add_argument("--timeout", type=float, default=5.0, help="network timeout in seconds (default: 5)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    try:
        host = normalize_host(args.domain)
    except ValueError as exc:
        parser.error(str(exc))

    report = build_report(host, args.timeout)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"Domain posture check: {host}")
    dns = report["dns"]
    if dns["resolved"]:
        print("DNS: resolved")
        for address in dns["addresses"]:
            print(f"  - {address}")
    else:
        print(f"DNS: lookup failed ({dns['error']})")

    tls = report.get("tls", {})
    if tls.get("validated"):
        print("TLS: certificate validated")
        if "expires_utc" in tls:
            print(f"  Expires: {tls['expires_utc']} ({tls['days_remaining']} days remaining)")
    else:
        print(f"TLS: check failed ({tls.get('error', 'unknown error')})")

    https = report.get("https", {})
    if "status" in https:
        print(f"HTTPS: responded with status {https['status']}")
        print("Selected response headers:")
        for name, present in https["present"].items():
            print(f"  {'present' if present else 'missing'}: {name}")
    else:
        print(f"HTTPS: request failed ({https.get('error', 'unknown error')})")

    print("\nA missing header is an observation to review, not proof of a vulnerability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
