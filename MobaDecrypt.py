#!/usr/bin/env python3
import sys, os, platform, random, base64, binascii
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
import sys

########### Crypto Code borrowed from https://github.com/HyperSine/how-does-MobaXterm-encrypt-password
class MobaXtermCrypto:

    def __init__(self, SysHostname: bytes, SysUsername: bytes, SessionP: bytes = None):
        self._SysHostname = SysHostname
        self._SysUsername = SysUsername
        self._SessionP = SessionP

    def _KeyCrafter(self, **kargs) -> bytes:
        if kargs.get('ConnHostname') != None and kargs.get('ConnUsername') != None:
            s1 = self._SysUsername + self._SysHostname
            while len(s1) < 20:
                s1 = s1 + s1

            s2 = kargs.get('ConnUsername') + kargs.get('ConnHostname')
            while len(s2) < 20:
                s2 = s2 + s2

            key_space = [
                s1.upper(),
                s2.upper(),
                s1.lower(),
                s2.lower()
            ]
        else:
            s = self._SessionP
            while len(s) < 20:
                s = s + s

            key_space = [
                s.upper(),
                s.upper(),
                s.lower(),
                s.lower()
            ]

        key = bytearray(b'0d5e9n1348/U2+67')
        for i in range(0, len(key)):
            b = key_space[(i + 1) % len(key_space)][i]
            if (b not in key) and (b in b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'):
                key[i] = b

        return bytes(key)

################### THIS DECODES HASHES THAT ARE FROM INI FILES
    def DecryptCredential(self, Ciphertext: str) -> bytes:
        key = self._KeyCrafter()

        ct = bytearray()
        for char in Ciphertext.encode('ascii'):
            if char in key:
                ct.append(char)

        if len(ct) % 2 == 0:
            pt = bytearray()
            for i in range(0, len(ct), 2):
                l = key.find(ct[i])
                key = key[-1:] + key[0:-1]
                h = key.find(ct[i + 1])
                key = key[-1:] + key[0:-1]
                assert (l != -1 and h != -1)
                pt.append(16 * h + l)
            return bytes(pt)
        else:
            raise ValueError('Invalid ciphertext.')

#################### IF STORED IN REGISTRY YOU NEED 2 MORE PARAMS: THE CONNECTION'S IP/HOST and USERNAME
    def DecryptPassword(self, Ciphertext: str, ConnHostname: bytes, ConnUsername: bytes) -> bytes:
        key = self._KeyCrafter(ConnHostname = ConnHostname, ConnUsername = ConnUsername)

        ct = bytearray()
        for char in Ciphertext.encode('ascii'):
            if char in key:
                ct.append(char)

        if len(ct) % 2 == 0:
            pt = bytearray()
            for i in range(0, len(ct), 2):
                l = key.find(ct[i])
                key = key[-1:] + key[0:-1]
                h = key.find(ct[i + 1])
                key = key[-1:] + key[0:-1]
                assert(l != -1 and h != -1)
                pt.append(16 * h + l)
            return bytes(pt)
        else:
            raise ValueError('Invalid ciphertext.')


print(f'''
  __  __       _          __  ___                      
 |  \/  | ___ | |__   __ _\ \/ / |_ ___ _ __ _ __ ___  
 | |\/| |/ _ \| '_ \ / _` |\  /| __/ _ \ '__| '_ ` _ \ 
 | |  | | (_) | |_) | (_| |/  \| ||  __/ |  | | | | | |
 |_|__|_|\___/|_.__/ \__,_/_/\_\\__\____|_|  |_| |_| |_|
 |  _ \  ___  ___ _ __ _   _ _ __ | |_ ___  _ __       
 | | | |/ _ \/ __| '__| | | | '_ \| __/ _ \| '__|      
 | |_| |  __/ (__| |  | |_| | |_) | || (_) | |         
 |____/ \___|\___|_|   \__, | .__/ \__\___/|_|         
                       |___/|_|
 
      by illwill - decryption class by HyperSine\n''')

if len(sys.argv) < 5: 
    print(f"Usage:\n")
    print(f"From inifile:")
    print(f"    MobaDecrypt.py Computer Username SessionP Hash\n")
    print(f"From Registry Password:")
    print(f"    MobaDecrypt.py Computer Username SessionP Hash Host/IP User")
    print(f"From Registry Credential:")
    print(f"    MobaDecrypt.py Computer Username SessionP Hash")
    sys.exit(1)
else:
    print(f"[*] Computer: "+sys.argv[1])
    print(f"[*] Username: "+sys.argv[2])
    print(f"[*] SessionP: "+sys.argv[3])
    print(f"[*] EncPass:  "+sys.argv[4])

if len(sys.argv) == 5:
    cipher = MobaXtermCrypto(sys.argv[1].encode('ansi'), sys.argv[2].encode('ansi') , sys.argv[3].encode('ansi'))
    passw = cipher.DecryptCredential(sys.argv[4])
    print(f'[*] Password: %s' % passw.decode("ascii"))
    sys.exit(1) 
if len(sys.argv) == 7:
    print(f"[*] Host/IP:  "+sys.argv[5])
    print(f"[*] User:     "+sys.argv[6])
    cipher = MobaXtermCrypto(sys.argv[1].encode('ansi'), sys.argv[2].encode('ansi') , sys.argv[3].encode('ansi'))
    passw = cipher.DecryptPassword(sys.argv[4], sys.argv[5].encode('ansi'), sys.argv[6].encode('ansi'))
    print(f'[*] Password: %s' % passw.decode("ascii"))
    sys.exit(1) 
