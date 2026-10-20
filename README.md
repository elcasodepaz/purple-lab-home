# Purple Lab Home

A growing portfolio of cybersecurity projects and controlled labs. The focus is learning penetration-testing methods in authorized environments and connecting observations to defensive takeaways.

## Projects

### Domain Posture Check

A standard-library Python command-line tool that checks **one domain per run** for DNS resolution, an HTTPS response, TLS certificate validity, and selected security headers.

- Project guide: domain-posture-check/README.md
- Python script: domain-posture-check/domain_posture_check.py

## Hands-on labs

### Windows Firewall Port Scan Lab

**Planned — not yet performed.** A narrow service-discovery scan of the user's own Windows 11 lab computer from Kali, followed by review of the Windows Defender Firewall log.

- Guide: attack-simulations/firewall-portscan-lab/README.md
- Do not mark this lab complete until real results have been recorded and sensitive details have been redacted.

### Raspberry Pi Cowrie Honeypot

**Planned — not yet installed or tested.** A contained Raspberry Pi exercise to generate a few benign SSH connection attempts from the user's own lab machine and review the resulting logs.

- Guide: honeypot-project/raspberrypi-cowrie-setup.md
- Keep it local and isolated; do not expose it to the public internet or use real credentials.
- Do not claim findings until the exercise has been performed and documented.

## Lab approach

- Test only systems I own or have explicit permission to assess.
- Define the target and allowed activity before testing.
- Keep tools narrow and explain what they do and do not establish.
- Record real commands, observations, limitations, and defensive recommendations.
- Build the portfolio project by project while practicing Python, Linux, networking, and security fundamentals.

## Training

- Google Cybersecurity Professional Certificate — completed
- HTB Academy Linux course — completed
