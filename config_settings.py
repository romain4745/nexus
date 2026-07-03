"""Single config file for everything"""

import os
import random
import string

class Config:
    # Tor
    TOR_SOCKS_PORT = 9050
    TOR_CONTROL_PORT = 9051
    USE_TOR = True
    
    # Session
    SESSION_ID = ''.join(random.choices(string.hexdigits, k=32))
    
    # Messaging
    CHAT_SELF_DESTRUCT_SECONDS = 30  # messages disappear after 30s
    MAX_MESSAGES_IN_MEMORY = 100
    
    # SMS
    SMS_SELF_DESTRUCT_AFTER_SEND = True
    
    # VoIP
    VOIP_DURATION_MIN = 30
    VOIP_DURATION_MAX = 120
    
    # Anti-forensics
    WIPE_CLIPBOARD_ON_EXIT = True
    WIPE_HISTORY_ON_EXIT = True
    MEMORY_ONLY_LOGGING = True

CONFIG = Config()