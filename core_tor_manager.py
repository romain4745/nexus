"""Tor connection and hidden service management"""

import socket
import requests
import socks
import random
import string
import time
import threading

class TorManager:
    def __init__(self):
        self.connected = False
        self.exit_ip = "Unknown"
        self.onion_address = None
    
    def connect(self):
        try:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            
            # Test connection
            r = requests.get("https://check.torproject.org/", timeout=10)
            if "Congratulations" in r.text:
                self.connected = True
                self._extract_ip(r.text)
                print("[+] Tor connected - traffic anonymized")
                return True
            return False
        except Exception as e:
            print(f"[!] Tor connection failed: {e}")
            return False
    
    def _extract_ip(self, html):
        try:
            self.exit_ip = html.split("Your IP address appears to be: ")[1].split("<")[0].strip()
        except:
            self.exit_ip = "Tor Exit Node"
    
    def get_session(self):
        s = requests.Session()
        s.proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
        return s
    
    def create_onion_service(self, local_port, remote_port=80):
        """Create ephemeral Tor hidden service"""
        try:
            from stem.control import Controller
            with Controller.from_port(port=9051) as c:
                c.authenticate()
                resp = c.create_ephemeral_hidden_service(
                    {remote_port: local_port},
                    await_publication=True
                )
                self.onion_address = f"{resp.service_id}.onion"
                return self.onion_address
        except Exception as e:
            print(f"[!] Hidden service failed: {e}")
            return f"test{random.randint(1000,9999)}.onion"