# NEXUS — All-in-One Penetration Testing Framework

**Authorized Security Testing Only.**
**Anonymized | Self-Destructing | Darknet Messaging | SMS/VoIP Spoofing**

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start (After Git Clone)](#quick-start-after-git-clone)
3. [Linux / Kali Installation](#linux--kali-installation)
4. [Windows Installation](#windows-installation)
5. [Directory Structure](#directory-structure)
6. [Complete Command Reference](#complete-command-reference)
   - [System Commands](#system-commands)
   - [Reconnaissance](#reconnaissance-commands)
   - [Exploitation](#exploitation-commands)
   - [Social Engineering](#social-engineering-commands)
   - [Darknet Messaging](#darknet-messaging-commands)
7. [Advanced Workflow Example](#advanced-workflow-example)
8. [Security & Anonymity Features](#security--anonymity-features)
9. [Troubleshooting](#troubleshooting)
10. [Uninstall](#uninstall)

---

## Overview

NEXUS is a modular, all-in-one penetration testing framework that combines:

- **Reconnaissance** — Subdomain enumeration (Sublist3r-style), port scanning (Nmap-style), directory brute force (Gobuster-style)
- **Exploitation** — SQL injection (SQLMap-style), XSS detection
- **Social Engineering** — Phishing page generator
- **Anonymous Communication** — Darknet chat over Tor hidden service (self-destructing messages), anonymous SMS with burner numbers, VoIP calls with spoofed caller ID
- **Anti-Forensics** — Memory-only operations, automatic trace wiping, clipboard and history cleanup

---

## Quick Start (After Git Clone)

### Prerequisites
- **Python 3.8+** installed
- **Git** installed
- **Tor** installed (recommended for full anonymity)

### Clone and Run in Under 1 Minute

```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/nexus.git
cd nexus

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3 (Linux): Start Tor
sudo systemctl start tor

# Step 4: Launch NEXUS
python main.py