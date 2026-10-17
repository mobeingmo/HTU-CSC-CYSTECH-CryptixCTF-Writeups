#!/usr/bin/env python3
import struct

data = open("spool.bin", "rb").read() # reads the chall file 
pos = 0

def take(n):
    global pos
    result = data[pos:pos + n]
    if len(result) != n:
        raise ValueError("Truncated spool file")
    pos += n
    return result
# Take each print assert to help recover the flag:
assert take(4) == b"PRN1"

assert take(4) == b"MAP1"
count = struct.unpack(">H", take(2))[0]

glyph_map = {}
for _ in range(count):
    code, character = struct.unpack(">BB", take(2))
    glyph_map[code] = character

assert take(4) == b"DOC1"
decoy_length = struct.unpack(">H", take(2))[0]
decoy = take(decoy_length)
print("Decoy:", decoy.decode("ascii"))

assert take(4) == b"DAT1"
payload_length = struct.unpack(">H", take(2))[0]
payload = take(payload_length)

flag = bytes(glyph_map[code] for code in payload)
print("Recovered:", flag.decode("ascii"))

flag = bytes(glyph_map[code] for code in payload)
print("Recovered:", flag.decode("ascii"))
