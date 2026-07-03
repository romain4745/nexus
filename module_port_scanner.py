"""TCP port scanner"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    def __init__(self):
        self.open_ports = []
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
            993, 995, 1433, 1521, 2049, 3306, 3389, 5432, 5900, 5985,
            5986, 6379, 8080, 8443, 9000, 9090, 27017
        ]
    
    def _scan_port(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            result = s.connect_ex((host, port))
            s.close()
            if result == 0:
                return port, self._guess_service(port)
            return None, None
        except:
            return None, None
    
    def _guess_service(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 1521: "Oracle", 2049: "NFS", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 5985: "WinRM-HTTP",
            5986: "WinRM-HTTPS", 6379: "Redis", 8080: "HTTP-Proxy",
            8443: "HTTPS-Alt", 9000: "SonarQube", 9090: "Cockpit",
            27017: "MongoDB"
        }
        return services.get(port, "Unknown")
    
    def scan(self, target, ports=None):
        if ports is None:
            ports = self.common_ports
        
        print(f"\n=== Port Scanner: {target} ===")
        print(f"  Scanning {len(ports)} common ports...")
        
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(self._scan_port, target, p): p for p in ports}
            for f in as_completed(futures):
                port, service = f.result()
                if port:
                    print(f"  [+] PORT {port}/tcp OPEN - {service}")
                    self.open_ports.append((port, service))
        
        print(f"\n[+] Open ports: {len(self.open_ports)}")
        return self.open_ports