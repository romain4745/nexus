"""Subdomain enumeration - Sublist3r style"""

import dns.resolver
import dns.exception
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

class DNSEnum:
    def __init__(self, tor_session=None):
        self.session = tor_session or requests.Session()
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2
        self.resolver.lifetime = 2
        self.found = set()
        
        self.wordlist = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop3',
            'admin', 'blog', 'dev', 'test', 'api', 'app', 'stage', 'staging',
            'prod', 'beta', 'demo', 'shop', 'store', 'portal', 'secure',
            'vpn', 'remote', 'exchange', 'owa', 'cpanel', 'whm', 'ns1',
            'ns2', 'mx1', 'mx2', 'dns1', 'server', 'cloud', 'cdn',
            'dashboard', 'panel', 'console', 'monitor', 'git', 'jenkins',
            'jira', 'wiki', 'help', 'support', 'chat', 'status',
            'admin1', 'admin2', 'backup', 'db', 'database', 'config',
            'web', 'www1', 'www2', 'beta2', 'alpha', 'internal',
            'private', 'hidden', 'secret', 'test1', 'dev1', 'staging1'
        ]
    
    def _crtsh(self, domain):
        """Certificate Transparency log search"""
        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            r = self.session.get(url, timeout=15)
            if r.status_code == 200:
                for entry in r.json():
                    name = entry.get('name_value', '')
                    for sub in name.split('\n'):
                        sub = sub.strip().lower()
                        if sub.endswith(domain):
                            self.found.add(sub)
                print(f"  [crt.sh] Found {len(self.found)} so far")
        except: pass
    
    def _dns_bruteforce(self, domain):
        """DNS brute force with threading"""
        print(f"  [DNS] Bruteforcing {len(self.wordlist)} subdomains...")
        
        def check(sub):
            try:
                target = f"{sub}.{domain}"
                answers = self.resolver.resolve(target, 'A')
                ips = [str(r) for r in answers]
                return target, ips
            except:
                return None, None
        
        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(check, sub): sub for sub in self.wordlist}
            for f in as_completed(futures):
                target, ips = f.result()
                if target:
                    self.found.add(target)
                    print(f"    [+] {target} -> {', '.join(ips[:3])}")
    
    def run(self, domain):
        print(f"\n=== DNS Enumeration: {domain} ===")
        self._crtsh(domain)
        self._dns_bruteforce(domain)
        
        print(f"\n[+] Total subdomains: {len(self.found)}")
        for s in sorted(self.found):
            print(f"    {s}")
        return list(self.found)