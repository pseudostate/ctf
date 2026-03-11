import struct

data = bytearray(open('sc.bin','rb').read())

# Stage 1: XOR with "calc.exe"
enc_qword = struct.unpack_from('<Q', data, 5)[0]
key1 = enc_qword ^ 0x0df0adbaefbeadde
for i in range(63):
    offset = 5 + i * 8
    qw = struct.unpack_from('<Q', data, offset)[0]
    struct.pack_into('<Q', data, offset, qw ^ key1)

# Stage 2: XOR with magic (0x0df0adbaefbeadde)
key2 = 0x0df0adbaefbeadde
for i in range(34):
    offset = 0x2d7 + i * 8
    qw = struct.unpack_from('<Q', data, offset)[0]
    struct.pack_into('<Q', data, offset, qw ^ key2)

# Show decrypted stage 2
stage2 = data[0x2d7:0x2d7+272]
print("=== Stage 2 decrypted (0x2d7~0x3e6) ===")
for i in range(0, 272, 16):
    chunk = stage2[i:i+16]
    hex_part = ' '.join(f'{b:02x}' for b in chunk)
    ascii_part = ''.join(chr(b) if 32<=b<127 else '.' for b in chunk)
    print(f'{0x2d7+i:04x}: {hex_part:<48}  {ascii_part}')