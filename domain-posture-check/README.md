# Domain Posture Check

A small Python command-line project for practicing DNS, HTTPS, TLS, and HTTP response-header fundamentals.

It checks **one domain per run** and reports observations. It does not exploit a target, brute-force paths, scan ports, or claim that a site is secure.

## Requirements

- Python 3.9 or newer
- No third-party packages

## Run

    python3 domain_posture_check.py example.com

You can also enter a full URL:

    python3 domain_posture_check.py https://example.com

The tool makes one DNS lookup, one TLS connection, and one HTTP HEAD request to the domain. The exact headers and certificate dates depend on the domain and can change. Run the offline unit tests with: python3 -m unittest -v.

## What it checks

- Whether the hostname resolves to IP addresses
- Whether HTTPS responds
- Whether Python's default TLS checks accept the server certificate
- The certificate expiration date, when available
- Presence of selected response headers: HSTS, Content-Security-Policy, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy

A missing header is a prompt for review, not proof of a vulnerability. Some headers may be set at a proxy or CDN or may be inappropriate for a particular application.

## Authorization and privacy

Use this only on domains you own or are explicitly authorized to assess. The script sends a single HTTPS HEAD request and does not submit credentials or collect page content. Do not use it against targets where you lack permission.

## Learning notes

This project practices Python's argparse, socket, ssl, urllib, exception handling, and structured output. Next improvements: add automated unit tests with mocked network responses, and write a short example analysis for a domain you control.
