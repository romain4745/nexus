"""Darknet encrypted chat over Tor hidden service
   Messages auto-destruct after 30 seconds
   No logs, no disk writes, memory only"""

import socket
import threading
import json
import time
import random
import string
from cryptography.fernet import Fernet

class OnionChat:
    def __init__(self, tor_manager, destructor):
        self.tor = tor_manager
        self.destruct = destructor
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.messages = []  # In-memory only
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.onion_addr = None
    
    def start_server(self):
        """Start chat as hidden service"""
        local_port = random.randint(10000, 60000)
        self.onion_addr = self.tor.create_onion_service(local_port)
        
        print(f"\n[+] DARKNET CHAT ACTIVE")
        print(f"[+] Onion Address: {self.onion_addr}")
        print(f"[+] Encryption Key: {self.key.decode()[:20]}...")
        print(f"[+] Messages auto-destruct after 30 seconds")
        print(f"[+] Send this onion address + key to target via SMS/VoIP")
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', local_port))
        self.server_socket.listen(1)
        self.server_socket.settimeout(1)
        
        self.running = True
        accept_thread = threading.Thread(target=self._accept_clients, daemon=True)
        accept_thread.start()
        
        self._chat_loop()
    
    def _accept_clients(self):
        while self.running:
            try:
                client, addr = self.server_socket.accept()
                self.client_socket = client
                print(f"\n[+] Target connected to chat!")
                
                recv_thread = threading.Thread(target=self._receive_messages, daemon=True)
                recv_thread.start()
            except socket.timeout:
                continue
            except:
                break
    
    def _receive_messages(self):
        while self.running and self.client_socket:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                msg = self.cipher.decrypt(data).decode()
                ts = time.strftime('%H:%M:%S')
                
                self.messages.append({
                    'text': msg,
                    'timestamp': ts,
                    'epoch': time.time()
                })
                
                print(f"\n[TARGET {ts}]: {msg}")
                
                # Schedule message destruction
                self.destruct.schedule_destroy(self.messages[-1], 30)
                
            except:
                break
    
    def _chat_loop(self):
        print("\n[*] Waiting for target to connect...")
        print("[*] Type /quit to exit chat")
        
        while self.running:
            try:
                msg = input("\n[YOU]: ").strip()
                if msg.lower() == '/quit':
                    break
                if not msg:
                    continue
                if not self.client_socket:
                    print("[!] No target connected yet")
                    continue
                
                encrypted = self.cipher.encrypt(msg.encode())
                self.client_socket.send(encrypted)
                
                ts = time.strftime('%H:%M:%S')
                self.messages.append({
                    'text': msg,
                    'timestamp': ts,
                    'epoch': time.time(),
                    'sent': True
                })
                
                self.destruct.schedule_destroy(self.messages[-1], 30)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[!] Error: {e}")
                break
        
        self.running = False
        self._cleanup()
    
    def _cleanup(self):
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        self.messages.clear()
        print("[*] Chat session destroyed, all messages wiped")