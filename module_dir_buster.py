"""Directory/file enumeration - Gobuster style"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

class DirBuster:
    def __init__(self, tor_manager=None):
        self.session = tor_manager.get_session() if tor_manager else requests.Session()
        self.found = []
        
        self.wordlist = [
            'admin', 'login', 'wp-admin', 'wp-content', 'backup', 'backups',
            'db', 'database', 'config', '.git', '.env', '.svn', 'credentials',
            'api', 'v1', 'v2', 'graphql', 'swagger', 'uploads', 'files',
            'download', 'images', 'css', 'js', 'phpinfo.php', 'info.php',
            'test.php', 'shell.php', 'robots.txt', 'sitemap.xml',
            'server-status', 'cgi-bin', 'admin.php', 'login.php', 'dashboard',
            'panel', 'cpanel', 'phpmyadmin', 'xmlrpc.php', 'wp-login.php',
            'status', 'health', 'debug', 'secret', 'private', 'hidden',
            'docs', 'install', 'setup', 'tmp', 'temp', 'cache', 'logs',
            '.htaccess', '.htpasswd', 'proxy', 'vpn', 'ssh', 'ftp',
            'mail', 'webmail', 'roundcube', 'owa', 'exchange'
        ]
        
        self.extensions = ['', '.php', '.asp', '.aspx', '.jsp', '.html', '.txt', '.json', '.bak']
    
    def _check(self, base_url, path):
        url = urljoin(base_url + '/', path)
        try:
            r = self.session.get(url, timeout=8, allow_redirects=False)
            if r.status_code in [200, 201, 204, 301, 302, 307, 403, 401]:
                size = len(r.content)
                loc = r.headers.get('Location', '') if r.status_code in [301, 302] else ''
                return {'url': url, 'status': r.status_code, 'size': size, 'redirect': loc}
        except:
            pass
        return None
    
    def run(self, base_url):
        print(f"\n=== Directory Buster: {base_url} ===")
        
        paths = []
        for word in self.wordlist:
            for ext in self.extensions:
                paths.append(f"{word}{ext}")
        
        print(f"  Testing {len(paths)} paths...")
        
        with ThreadPoolExecutor(max_workers=25) as ex:
            futures = {ex.submit(self._check, base_url, p): p for p in paths}
            for i, f in enumerate(as_completed(futures)):
                result = f.result()
                if result:
                    rdir = f" -> {result['redirect']}" if result['redirect'] else ''
                    print(f"  [{result['status']}] {result['url']} (Size: {result['size']}){rdir}")
                    self.found.append(result)
                if i % 50 == 0 and i > 0:
                    print(f"    Progress: {i}/{len(paths)}")
        
        print(f"\n[+] Found {len(self.found)} paths")
        return self.found