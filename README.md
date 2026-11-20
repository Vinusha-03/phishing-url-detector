# Phishing URL Detector (Python)

A beginner-friendly cybersecurity project that checks a URL for common phishing warning signs using simple Python heuristics.

## Features

- Checks for IP-address-based URLs.
- Flags URL shorteners.
- Looks for suspicious words such as `login`, `verify`, and `password`.
- Checks for unusually long URLs and many subdomains.
- Flags URLs without HTTPS and selected uncommon top-level domains.
- Explains which warning signs caused the result.

## Requirements

- Python 3.9 or later
- No third-party packages

## Run the project

Open a terminal in this project folder.

Check a URL:

```bash
python phishing_detector.py https://example.com
```

Or run without an argument and enter a URL when prompted:

```bash
python phishing_detector.py
```

Try these educational test examples:

```bash
python phishing_detector.py https://example.com
python phishing_detector.py http://192.0.2.10/login/verify
python phishing_detector.py http://secure-account-login.example.top/verify
```

The IP address in the second example is reserved for documentation and is not a real target.

## How it works

The program parses the URL with Python's `urllib.parse`, then checks for patterns that can sometimes appear in phishing links. It reports the reasons behind its result.

## Important limitations

This is a learning project, not a production phishing-detection service. It does not open URLs, check website reputation, inspect page content, or use machine learning. A suspicious-looking URL is not automatically malicious, and a URL marked lower risk is not guaranteed safe. Never enter sensitive information just because this tool reports lower risk.

## Concepts learned

- URL parsing
- Python functions and sets
- Basic input validation
- Conditional logic
- Command-line arguments with `argparse`
- Cybersecurity awareness and heuristic detection
