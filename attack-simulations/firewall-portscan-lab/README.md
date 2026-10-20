# Windows Firewall Port Scan Lab

**Status: Planned — not yet performed.** This guide is the starting plan. Add your own observations and evidence after you run it; do not describe the lab as completed before then.

## Goal

From your Kali system, perform a small, authorized service-discovery scan of your own Windows 11 lab computer. Then review the Windows Defender Firewall log for traffic associated with the scan.

This gives you practice with the penetration-testing workflow (scope, discovery, notes) and the defensive workflow (firewall telemetry, interpretation, recommendations).

## Lab scope

- **Scanner:** your Kali Linux system
- **Target:** your own Windows 11 Pro lab computer
- **Network:** your private home lab network
- **Allowed activity:** one TCP connect scan of the target's 20 most common TCP ports, with service identification
- **Out of scope:** every other device, public IP addresses, networks you do not own, exploitation, password guessing, denial-of-service, and stealth/evasion options

If you cannot confidently identify the Windows computer's private IP address, stop and identify it before scanning. Do not substitute your router's address or scan a whole subnet.

## Preparation

1. Confirm Kali and the Windows lab computer are connected to your own private home network.
2. On Windows, open Command Prompt and run:

       ipconfig

3. Record the Windows computer's IPv4 address in your private lab notes. Double-check that it belongs to the Windows computer, not the router.
4. On Windows, open Windows Defender Firewall with Advanced Security by running:

       wf.msc

5. Open the properties for the active firewall profile. In its Logging settings, set **Log dropped packets** to **Yes**. Keep successful-connection logging off for this exercise. Note the log file path shown there; the default is usually:

       %systemroot%\system32\LogFiles\Firewall\pfirewall.log

Changing this option enables local firewall logging. Do not turn off the firewall.

## Run the scan

From Kali, replace the placeholder with the Windows computer's private IPv4 address:

    nmap -sT -sV --top-ports 20 -oN baseline.txt WINDOWS_LAB_IP

For example, if your Windows lab computer's address were 192.168.1.25, the final argument would be 192.168.1.25. Use your actual address.

- -sT uses a TCP connect scan.
- -sV asks Nmap to identify services on ports that respond.
- --top-ports 20 limits the scan to 20 commonly used TCP ports.
- -oN saves a readable results file named baseline.txt.

Run this command only against the Windows computer you own in this lab.

## Review the defensive evidence

1. On Windows, open the firewall log path you recorded. You may need an administrator account to read it.
2. Find entries from the time you ran the scan. Look for dropped TCP traffic from your Kali computer to the Windows computer.
3. Compare those observations with the Nmap results. A port reported open, closed, or filtered describes what the scanner observed; it does not by itself tell you whether a service is needed.
4. For every open port you find, identify the service and ask whether the Windows lab computer needs it reachable from the home network. Do not disable a service or change firewall rules during this first pass.

## Results to record

- Date and time of the scan:
- Kali private IP:
- Windows lab private IP (replace with a placeholder before publishing):
- Nmap version:
- Number of open ports:
- Open ports and identified services:
- Number of matching firewall log entries:
- What the scan could not determine:
- One defensive recommendation and why:
- Screenshot or sanitized text evidence:

Do not publish private IP addresses, usernames, hostnames, or unrelated log entries. Redact them before adding evidence to GitHub.

## What this lab demonstrates

After you run it and record real results, this lab can demonstrate how you:

- define a narrow scope for an authorized test
- perform limited service discovery
- collect and compare results from a scanner and a host firewall log
- distinguish observations from conclusions
- write a practical defensive recommendation

## Resume note

This lab is **not completed yet**. After you perform it, replace this note with a short summary based on your actual results. Never claim a finding, detection, or impact that you did not observe.
