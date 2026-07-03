#!/usr/bin/env python3
"""
NEXUS - All-in-One Penetration Testing Framework
Anonymized | Self-Destructing | Darknet Messaging

Authorized Use Only.
"""

import os
import sys
import platform

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from colorama import init, Fore, Style
init(autoreset=True)

from config_settings import CONFIG
from core_tor_manager import TorManager
from core_self_destruct import SelfDestruct
from module_dns_enum import DNSEnum
from module_port_scanner import PortScanner
from module_dir_buster import DirBuster
from module_sqli_engine import SQLiEngine
from module_xss_engine import XSSEngine
from module_onion_chat import OnionChat
from module_sms_gateway import SMSGateway
from module_voip_gateway import VoIPGateway
from module_phishing_kit import PhishingKit

BANNER = f"""
{Fore.RED}
    ╔═══════════════════════════════════════╗
    ║         N E X U S   v 3 . 0          ║
    ║  All-in-One Penetration Framework     ║
    ║  Darknet • Self-Destruct • Anonymous  ║
    ╚═══════════════════════════════════════╝
{Style.RESET_ALL}
"""

class NEXUS:
    def __init__(self):
        self.tor = TorManager()
        self.destruct = SelfDestruct()
        self.modules = {}
        self.running = True
    
    def start(self):
        print(BANNER)
        
        # Connect Tor
        print(f"{Fore.CYAN}[*] Connecting to Tor...{Style.RESET_ALL}")
        if self.tor.connect():
            print(f"{Fore.GREEN}[+] Tor online - Exit IP: {self.tor.exit_ip}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Tor offline - limited anonymity{Style.RESET_ALL}")
        
        # Initialize modules
        self.modules = {
            'dns_enum': DNSEnum(self.tor.get_session() if self.tor.connected else None),
            'port_scan': PortScanner(),
            'dir_bust': DirBuster(self.tor if self.tor.connected else None),
            'sqli': SQLiEngine(),
            'xss': XSSEngine(),
            'chat': OnionChat(self.tor, self.destruct),
            'sms': SMSGateway(self.tor),
            'voip': VoIPGateway(self.tor),
            'phish': PhishingKit(self.tor),
        }
        
        self._shell()
    
    def _shell(self):
        while self.running:
            try:
                cmd = input(f"\n{Fore.RED}nexus{Fore.WHITE}@{Fore.CYAN}darknet{Fore.WHITE} > {Style.RESET_ALL}").strip()
                self._execute(cmd)
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                break
        
        self._shutdown()
    
    def _execute(self, cmd):
        if not cmd:
            return
        
        parts = cmd.split(maxsplit=2)
        base = parts[0].lower()
        
        commands = {
            'help': self._help,
            'exit': self._shutdown,
            'quit': self._shutdown,
            'clear': lambda _: os.system('cls' if os.name == 'nt' else 'clear'),
            'whoami': self._whoami,
            'wipe': self._wipe,
            'dns': self._run_dns,
            'scan': self._run_scan,
            'dirb': self._run_dirb,
            'sqli': self._run_sqli,
            'xss': self._run_xss,
            'chat': self._run_chat,
            'sms': self._run_sms,
            'voip': self._run_voip,
            'phish': self._run_phish,
        }
        
        handler = commands.get(base)
        if handler:
            handler(cmd)
        else:
            print(f"{Fore.YELLOW}[!] Unknown: {base}. Type 'help'{Style.RESET_ALL}")
    
    def _help(self, cmd):
        print(f"""{Fore.CYAN}
╔══════════════════════════════════════╗
║           NEXUS COMMANDS            ║
╠══════════════════════════════════════╣
║ RECON                                ║
║   dns <domain>    Subdomain enum     ║
║   scan <ip>       Port scanner       ║
║   dirb <url>      Directory buster   ║
║ EXPLOIT                              ║
║   sqli <url>      SQL injection      ║
║   xss <url>       XSS scanner        ║
║ SOCIAL                               ║
║   phish           Start phishing     ║
║ MESSAGING                            ║
║   chat            Darknet chat       ║
║   sms <num> <msg> Anonymous SMS      ║
║   voip <num>      Anonymous VoIP     ║
║ SYSTEM                               ║
║   whoami          Show identity      ║
║   wipe            Wipe all traces    ║
║   clear           Clear screen       ║
║   exit            Exit + auto-wipe   ║
╚══════════════════════════════════════╝{Style.RESET_ALL}""")
    
    def _whoami(self, cmd):
        print(f"{Fore.CYAN}[*] Session ID:   {CONFIG.SESSION_ID}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Exit IP:      {self.tor.exit_ip}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Tor Status:   {'Connected' if self.tor.connected else 'Disconnected'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Self-Destruct: Active (30s message TTL){Style.RESET_ALL}")
    
    def _wipe(self, cmd):
        self.destruct.wipe_all()
    
    def _run_dns(self, cmd):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{Fore.YELLOW}Usage: dns <domain>{Style.RESET_ALL}")
            return
        self.modules['dns_enum'].run(parts[1])
    
    def _run_scan(self, cmd):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{Fore.YELLOW}Usage: scan <ip>{Style.RESET_ALL}")
            return
        self.modules['port_scan'].scan(parts[1])
    
    def _run_dirb(self, cmd):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{Fore.YELLOW}Usage: dirb <url>{Style.RESET_ALL}")
            return
        self.modules['dir_bust'].run(parts[1])
    
    def _run_sqli(self, cmd):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{Fore.YELLOW}Usage: sqli <url>{Style.RESET_ALL}")
            return
        self.modules['sqli'].run(parts[1])
    
    def _run_xss(self, cmd):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{Fore.YELLOW}Usage: xss <url>{Style.RESET_ALL}")
            return
        self.modules['xss'].scan(parts[1])
    
    def _run_chat(self, cmd):
        self.modules['chat'].start_server()
    
    def _run_sms(self, cmd):
        parts = cmd.split(maxsplit=2)
        if len(parts) < 3:
            print(f"{Fore.YELLOW}Usage: sms <number> <message>{Style.RESET_ALL}")
            return
        self.modules['sms'].send(parts[1], parts[2])
    
    def _run_voip(self, cmd):
        parts = cmd.split(maxsplit=2)
        if len(parts) < 2:
            print(f"{Fore.YELLOW}Usage: voip <number> [message]{Style.RESET_ALL}")
            return
        msg = parts[2] if len(parts) >= 3 else None
        self.modules['voip'].call(parts[1], msg)
    
    def _run_phish(self, cmd):
        parts = cmd.split()
        brand = parts[1] if len(parts) > 1 else 'bank'
        self.modules['phish'].start_server(brand=brand)
    
    def _shutdown(self):
        print(f"\n{Fore.RED}[*] Wiping all session data...{Style.RESET_ALL}")
        self.destruct.wipe_all()
        print(f"{Fore.GREEN}[+] Goodbye. No traces remain.{Style.RESET_ALL}")
        self.running = False
        sys.exit(0)


if __name__ == "__main__":
    if platform.system() != "Windows" and os.geteuid() != 0:
        print(f"{Fore.YELLOW}[!] Run as root for full functionality{Style.RESET_ALL}")
    
    app = NEXUS()
    app.start()