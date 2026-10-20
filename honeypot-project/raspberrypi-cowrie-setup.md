# Raspberry Pi Cowrie Honeypot

**Status: Planned — not installed or tested yet.**

## Goal

Build a small, contained honeypot project on my Raspberry Pi 4 (8 GB) to learn how an SSH/Telnet honeypot records unsolicited activity and how to review those events defensively.

## Safety and scope

- Keep the honeypot on an isolated local lab network or host-only segment.
- Do not expose it to the public internet or configure router port forwarding.
- Do not use real passwords, personal data, or credentials from another system.
- Keep the device and logs disposable; record only the test activity needed for the lab.
- Generate test connections only from my own lab machine.

## Planned workflow

1. Draw the lab layout and record the Pi OS version, network mode, and addresses privately.
2. Install Cowrie using its current official documentation and record the exact version and setup steps.
3. Confirm the service is reachable only from the authorized lab machine.
4. Make a few benign test SSH connection attempts using clearly fake usernames and passwords.
5. Review the resulting event logs: timestamps, source address, attempted usernames, and session events.
6. Summarize what the logs show, what they cannot prove, and practical defensive steps.
7. Redact local addresses and other identifying details before publishing screenshots or sample logs.

## Results

Not started. Add commands, versions, observations, and redacted evidence here only after performing the lab.

## Reflection prompts

- Which events did Cowrie record during my controlled tests?
- What useful context did the logs provide, and what did they miss?
- How would I alert on repeated attempts without treating every event as a confirmed compromise?
- What containment or monitoring change would I make based on the exercise?
