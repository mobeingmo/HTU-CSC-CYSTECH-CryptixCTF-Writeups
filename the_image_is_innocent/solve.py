#!/usr/bin/env python3

# The Image Is Innocent - writeup by Mohammad Alshkibi

# The Challenge revolves around 3 main ideas: per-channel LSB diffing (LSB steganography), hiding data in a custom PNG chunk (PNG chunk structure) and chaining files together with hashes


#                                                          ==HINTS==

# 1. Not a single image holds the flag. The differences between images do. Running zsteg or stegsolve on one file only gives you noise.
# 2. Do NOT sort by file type nor size. 
# 3. Every image remembers where it came from. It remembers what its parent looked like, not how it was packed.
# 4. Diff per channel. Load all 19 images and check, for each channel, which pixels’ LSBs differ across the set. Red and green differ everywhere. Blue differs in just 14 pixels, all on row 173, columns 98–112. That is the real signal.

#                                                    Solver Script (Official):
# Defining: 
import glob, hashlib, re, struct, sys
import numpy as np
from PIL import Image
folder = sys.argv[1] if len(sys.argv) > 1 else "dist" # (For me, I had the files in a directory named "dist/" already reordered)
paths = sorted(glob.glob(f"{folder}/*.png"))          # Sort the images in the path
pix = {p: np.array(Image.open(p).convert("RGB")) for p in paths}   # converts the image into RGB values

# step 1: use per-channel LSB diff to find out where the real signal lives. by using zsteg and other tools we notice that R and G differ almost everywhere which are noise but BLUE on the other hand differs in only a few pixels

# The core of the solve script: 
# --

stack = np.stack([pix[p][..., 2] & 1 for p in paths])      # (n, H, W) blue LSBs
varying = stack.min(0) != stack.max(0)
ys, xs = np.nonzero(varying)
print(f"blue LSB varies at y={set(ys)} x={xs.min()}..{xs.max()} ({len(xs)} px)") # shows the Blue LSB difference Y axis
# ASCII bytes always have MSB = 0, so the first pixel of each byte never varies (here x=97 and x=105 are constant) The varying pixels show up as two 7-px groups; anchor the 16-px window on the LAST varying pixel, not the first.
sig_y, x1 = ys[0], xs.max()
x0 = x1 - 15

# -- 

def fragment(p): # differenciating blue LSB bytes: 
    bits = pix[p][sig_y, x0:x1 + 1, 2] & 1
    return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))

# private chunk to prev pointer
def prev_ptr(p):
    data, off = open(p, "rb").read(), 8
    while off < len(data):
        ln, tag = struct.unpack(">I4s", data[off:off + 8])
        if tag == b"crYp":
            return re.search(rb"prev=([0-9a-f]{16})", data[off + 8:off + 8 + ln]).group(1).decode()
        off += 12 + ln

# hash of the decoded pixels identifies each image
by_hash = {hashlib.sha256(pix[p].tobytes()).hexdigest()[:16]: p for p in paths}
child = {} 	# parent path TO child path (hint 3)
root = None
for p in paths:
    ptr = prev_ptr(p)
    if set(ptr) == {"0"}:
        root = p
    else:
        child[by_hash[ptr]] = p

order, cur = [], root
while cur: 
    order.append(cur)
    cur = child.get(cur)
print(f"chain length: {len(order)}")

flag = b"".join(fragment(p) for p in order)
print(flag.rstrip(b"\x00").decode()) # to strip the padding byte, in case the flag has odd length
# and that's it! 
# Flag: `Cryptix{1m_b1u3_b4d4b33b4d4d13}`
