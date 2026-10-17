Important: This is a teaching prototype, not a real printer language challenge. Its mapping table stores the character bytes directly, so participants can solve it by parsing the format rather than reversing a real font. That is intentional for the first version.

inspect the artifact: python3 make_challenge.py
file spool.bin
xxd spool.bin | head -30
strings spool.bin


What you should notice:
- PRN1 identifies our invented container.
- MAP1 introduces the glyph mapping.
- DOC1 contains the decoy.
- DAT1 introduces the encoded payload.
The interesting part is that the payload consists of glyph codes, not the original flag bytes.


