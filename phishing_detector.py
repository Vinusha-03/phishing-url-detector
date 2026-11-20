#!/usr/bin/env python3
"""
Phishing URL Detector (educational project).

Uses simple URL-pattern heuristics. It does not visit URLs, download content,
or guarantee that a URL is safe.
"""

import argparse
import ipaddress
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = {
    "login", "verify", "account", "update", "secure", "password",
    "banking", "wallet", "confirm", "signin", "payment",
}
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly",
}
SUSPICIOUS_TLDS = {
    "zip", "mov", "top", "xyz", "click", "work",
}


def normalize_url(raw_url: str) -> str:
    """Add a scheme when the user enters a bare domain."""
    value = raw_url.strip()
    if not value:
        raise ValueError("Please enter a URL.")
    if "://" not in value:
        value = "http://" + value
    return value


def analyze_url(raw_url: str) -> tuple[str, list[str]]:
    """Return a heuristic risk label and the reasons found."""
    url = normalize_url(raw_url)
    parsed = urlparse(url)
    host = parsed.hostname

    if not host:
        raise ValueError("That does not look like a valid URL. Check the address.")

    reasons = []
    hostname = host.lower().rstrip(".")
    labels = hostname.split(".")

    # Check whether the hostname is an IP address.
    try:
        ipaddress.ip_address(hostname)
        reasons.append("The address uses an IP address instead of a domain name.")
    except ValueError:
        pass

    if "@" in parsed.netloc:
        reasons.append("The address contains '@', which can hide the real destination.")

    if hostname.startswith("xn--") or ".xn--" in hostname:
        reasons.append("The domain contains punycode, which can be used for look-alike names.")

    if len(labels) > 4:
        reasons.append("The domain has an unusually large number of subdomains.")

    if len(url) > 100:
        reasons.append("The URL is unusually long.")

    if parsed.scheme.lower() != "https":
        reasons.append("The URL does not use HTTPS.")

    if hostname in SHORTENER_DOMAINS:
        reasons.append("The domain is a URL-shortening service, so the final destination is hidden.")

    tld = labels[-1] if labels else ""
    if tld in SUSPICIOUS_TLDS:
        reasons.append(f"The domain uses the less-common '.{tld}' top-level domain.")

    searchable_text = (hostname + " " + parsed.path.lower()).lower()
    found_keywords = sorted(word for word in SUSPICIOUS_KEYWORDS if word in searchable_text)
    if found_keywords:
        reasons.append("It contains security-sensitive words: " + ", ".join(found_keywords) + ".")

    if parsed.port not in (None, 80, 443):
        reasons.append("The URL uses a non-standard web port.")

    if not reasons:
        return "LOWER RISK (not guaranteed safe)", [
            "No obvious warning signs were found by these basic checks."
        ]

    # This is a simple educational score, not a trained classifier.
    if len(reasons) >= 3:
        label = "HIGHER RISK"
    else:
        label = "POTENTIALLY SUSPICIOUS"

    return label, reasons


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check a URL for common phishing warning signs (heuristics only)."
    )
    parser.add_argument("url", nargs="?", help="URL to analyze")
    args = parser.parse_args()

    raw_url = args.url or input("Enter a URL to check: ")

    try:
        label, reasons = analyze_url(raw_url)
    except ValueError as error:
        parser.exit(1, f"Error: {error}\n")

    print(f"\nResult: {label}")
    print("Reasons:")
    for reason in reasons:
        print(f"- {reason}")

    print("\nReminder: This tool does not visit the URL and cannot prove a site is safe.")
    print("Do not enter passwords or personal information on an unfamiliar website.")


if __name__ == "__main__":
    main()
