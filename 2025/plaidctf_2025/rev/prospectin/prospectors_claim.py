from pwn import *

def get_score(flag: str) -> int:
    flag_bytes = bytearray(flag, encoding="ascii")
    score = 0
    if flag_bytes[27] == 0x32: score += 1
    if ((flag_bytes[31] ^ flag_bytes[24]) == 0xaa): score += 1
    if ((flag_bytes[31] + flag_bytes[46]) == 0x100 - 0x70): score += 1
    if ((flag_bytes[59] + flag_bytes[36]) == 0x100 - 0x7f): score += 1
    if (flag_bytes[13] == 0xbe): score += 1
    if (flag_bytes[32] == 100): score += 1
    if (flag_bytes[26] == 0x31): score += 1
    if (flag_bytes[42] == 0x39): score += 1
    if ((flag_bytes[45] + flag_bytes[63]) == 0x100 - 0x6d): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if ((flag_bytes[1] + flag_bytes[15]) == ord('8')): score += 1
    if ((flag_bytes[13] ^ flag_bytes[35]) == 0x8e): score += 1
    if ((flag_bytes[1] ^ flag_bytes[46]) == 0x71): score += 1
    if (flag_bytes[42] == 0xb4): score += 1
    if (flag_bytes[19] == 0x36): score += 1
    if (flag_bytes[28] == flag_bytes[48]): score += 1
    if ((flag_bytes[10] ^ flag_bytes[33]) == 3): score += 1
    if (flag_bytes[30] == 0x76): score += 1
    if (flag_bytes[5] == 0x32): score += 1
    if ((flag_bytes[1] ^ flag_bytes[48]) == 0x85): score += 1
    if (flag_bytes[2] == 0x54): score += 1
    if (flag_bytes[23] == 0xe1): score += 1
    if ((flag_bytes[9] ^ flag_bytes[54]) == 0x81): score += 1
    if ((flag_bytes[53] + flag_bytes[26]) == ord('a')): score += 1
    if ((flag_bytes[18] ^ flag_bytes[57]) == 7): score += 1
    if ((flag_bytes[18] ^ flag_bytes[5]) == 0x56): score += 1
    if ((flag_bytes[14] + flag_bytes[53]) == ord('f')): score += 1
    if ((flag_bytes[48] ^ flag_bytes[56]) == 0x54): score += 1
    if (flag_bytes[52] == 0xe5): score += 1
    if (flag_bytes[36] == ord('o')): score += 1
    if ((flag_bytes[37] + flag_bytes[30]) == ord('f')): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if (flag_bytes[23] == 0x38): score += 1
    if (flag_bytes[39] == ord('4')): score += 1
    if ((flag_bytes[56] + flag_bytes[19]) == 0x100 - 0x69): score += 1
    if ((flag_bytes[19] ^ flag_bytes[50]) == 0x2d): score += 1
    if ((flag_bytes[34] + flag_bytes[1]) == 0x100 - 0x5c): score += 1
    if ((flag_bytes[47] + flag_bytes[38]) == 0x100 - 0xc): score += 1
    if ((flag_bytes[27] + flag_bytes[47]) == 0x100 - 0x69): score += 1
    if ((flag_bytes[47] + flag_bytes[10]) == 0x100 - 0x6a): score += 1
    if (flag_bytes[2] == 0x72): score += 1
    if (flag_bytes[59] == 0x36): score += 1
    if (flag_bytes[28] == 0xb1): score += 1
    if ((flag_bytes[8] ^ flag_bytes[58]) == 8): score += 1
    if ((flag_bytes[2] ^ flag_bytes[46]) == 0x3a): score += 1
    if (flag_bytes[59] == 0x44): score += 1
    if (flag_bytes[57] == 0x12): score += 1
    if ((flag_bytes[17] ^ flag_bytes[40]) == 0x5b): score += 1
    if (flag_bytes[41] == 0x2a): score += 1
    if (flag_bytes[41] == 0x33): score += 1
    if ((flag_bytes[26] + flag_bytes[38]) == ord('?')): score += 1
    if ((flag_bytes[61] ^ flag_bytes[0]) == 0x60): score += 1
    if (flag_bytes[21] == 0x24): score += 1
    if ((flag_bytes[5] + flag_bytes[43]) == ord('-')): score += 1
    if (flag_bytes[57] == 99): score += 1
    if ((flag_bytes[55] ^ flag_bytes[52]) == 5): score += 1
    if (flag_bytes[4] == 0x7b): score += 1
    if ((flag_bytes[16] + flag_bytes[9]) == 0x100 - 0x53): score += 1
    if ((flag_bytes[22] + flag_bytes[45]) == 0x100 - 0x68): score += 1
    if (flag_bytes[24] == 0x32): score += 1
    if (flag_bytes[48] == 0x35): score += 1
    if ((flag_bytes[54] ^ flag_bytes[19]) == 0x5b): score += 1
    if ((flag_bytes[54] + flag_bytes[14]) == 0x100 - 0x67): score += 1
    if (flag_bytes[53] == 0xd2): score += 1
    if ((flag_bytes[0] ^ flag_bytes[48]) == 0x65): score += 1
    if ((flag_bytes[42] + flag_bytes[49]) == 0x100 - 0x66): score += 1
    if ((flag_bytes[20] + flag_bytes[29]) == 0x100 - 0x6a): score += 1
    if ((flag_bytes[40] ^ flag_bytes[50]) == 0xda): score += 1
    if ((flag_bytes[60] + flag_bytes[32]) == 0x100 - 0x6a): score += 1
    if ((flag_bytes[39] + flag_bytes[7]) == 0x100 - 0x68): score += 1
    if (flag_bytes[50] == flag_bytes[10]): score += 1
    if ((flag_bytes[57] ^ flag_bytes[10]) == 0x52): score += 1
    if (flag_bytes[56] == 0x61): score += 1
    if (flag_bytes[20] == 0x61): score += 1
    if ((flag_bytes[62] ^ flag_bytes[8]) == 1): score += 1
    if ((flag_bytes[44] ^ flag_bytes[34]) == 0x30): score += 1
    if (flag_bytes[33] == 0x32): score += 1
    if ((flag_bytes[47] ^ flag_bytes[49]) == 4): score += 1
    if ((flag_bytes[27] ^ flag_bytes[22]) == 0x53): score += 1
    if ((flag_bytes[0] + flag_bytes[41]) == 0x100 - 0x7d): score += 1
    if (flag_bytes[18] == 0xf1): score += 1
    if (flag_bytes[28] == 0x35): score += 1
    if (flag_bytes[16] == 0xd3): score += 1
    if ((flag_bytes[6] + flag_bytes[47]) == 0x100 - 0x67): score += 1
    if ((flag_bytes[28] + flag_bytes[25]) == 0x100 -0x51): score += 1
    if ((flag_bytes[63] + flag_bytes[19]) == 0x100 - 0x4d): score += 1
    if (flag_bytes[29] == 0x35): score += 1
    if (flag_bytes[61] == 0x30): score += 1
    if ((flag_bytes[15] + flag_bytes[25]) == 0x100 - 0x7b): score += 1
    if ((flag_bytes[20] ^ flag_bytes[61]) == 0x4f): score += 1
    if ((flag_bytes[27] ^ flag_bytes[50]) == 3): score += 1
    if ((flag_bytes[62] + flag_bytes[51]) == ord('b')): score += 1
    if ((flag_bytes[20] + flag_bytes[44]) == 0x100 - 0x3b): score += 1
    if ((flag_bytes[43] + flag_bytes[18]) == 0x100 - 0x37): score += 1
    if ((flag_bytes[9] + flag_bytes[36]) == ord('h')): score += 1
    if (flag_bytes[9] == flag_bytes[19]): score += 1
    if ((flag_bytes[19] ^ flag_bytes[33]) == 4): score += 1
    if ((flag_bytes[55] + flag_bytes[0]) == 0x100 - 0x7b): score += 1
    if (flag_bytes[22] == 0x61): score += 1
    if (flag_bytes[17] == 0x39): score += 1
    if (flag_bytes[10] == 0x31): score += 1
    if (flag_bytes[53] == 0x30): score += 1
    if ((flag_bytes[49] + flag_bytes[61]) == 0x100 - 0x17): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if ((flag_bytes[55] + flag_bytes[3]) == 0x100 - -0x41): score += 1
    if ((flag_bytes[45] + flag_bytes[25]) == 0x100 - 0x67): score += 1
    if (flag_bytes[46] == 0x32): score += 1
    if ((flag_bytes[24] + flag_bytes[43]) == 0x100 - 0x69): score += 1
    if (flag_bytes[26] == 0x31): score += 1
    if (flag_bytes[14] == 0x36): score += 1
    if ((flag_bytes[3] + flag_bytes[62]) == ord('v')): score += 1
    if (flag_bytes[27] == 0x32): score += 1
    if ((flag_bytes[63] ^ flag_bytes[45]) == 0x4a): score += 1
    if ((flag_bytes[44] + flag_bytes[14]) == 0x100 - 0x10): score += 1
    if (flag_bytes[9] == 0xd8): score += 1
    if ((flag_bytes[58] + flag_bytes[62]) == ord('b')): score += 1
    if ((flag_bytes[61] + flag_bytes[22]) == 0x100 - 0x6d): score += 1
    if ((flag_bytes[51] ^ flag_bytes[53]) == 2): score += 1
    if (flag_bytes[27] == 0x32): score += 1
    if ((flag_bytes[50] ^ flag_bytes[59]) == 7): score += 1
    if (flag_bytes[52] == 0x30): score += 1
    if (flag_bytes[33] == 0x79): score += 1
    if (flag_bytes[61] == 0x33): score += 1
    if ((flag_bytes[21] + flag_bytes[49]) == 0x100 - 0x3b): score += 1
    if (flag_bytes[36] == ord('S')): score += 1
    if (flag_bytes[15] == 9): score += 1
    if ((flag_bytes[0] + flag_bytes[32]) == 0x100 - 0x4c): score += 1
    if ((flag_bytes[14] + flag_bytes[51]) == ord('h')): score += 1
    if ((flag_bytes[43] ^ flag_bytes[14]) == 0xfb): score += 1
    if (flag_bytes[58] == 0x4f): score += 1
    if (flag_bytes[10] == 0x3e): score += 1
    if (flag_bytes[47] == 0xec): score += 1
    if (flag_bytes[45] == 0x37): score += 1
    if ((flag_bytes[22] + flag_bytes[59]) == 0x100 - 1): score += 1
    if ((flag_bytes[24] ^ flag_bytes[2]) == 0x28): score += 1
    if (flag_bytes[48] == 0xd1): score += 1
    if ((flag_bytes[55] ^ flag_bytes[7]) == 0xe8): score += 1
    if (flag_bytes[47] == 0x65): score += 1
    if ((flag_bytes[5] + flag_bytes[57]) == 0x100 - 4): score += 1
    if ((flag_bytes[24] + flag_bytes[5]) == ord('d')): score += 1
    if ((flag_bytes[34] ^ flag_bytes[54]) == 2): score += 1
    if (flag_bytes[9] == 0x36): score += 1
    if (flag_bytes[5] == 0x32): score += 1
    if (flag_bytes[26] == 0x31): score += 1
    if (flag_bytes[60] == 0x32): score += 1
    if ((flag_bytes[4] + flag_bytes[7]) == 0x100 - 0x21): score += 1
    if (flag_bytes[31] == 0x34): score += 1
    if ((flag_bytes[50] ^ flag_bytes[52]) == 0x59): score += 1
    if (flag_bytes[58] == 0x39): score += 1
    if ((flag_bytes[12] ^ flag_bytes[43]) == 0x53): score += 1
    if (flag_bytes[7] == 0x61): score += 1
    if ((flag_bytes[53] ^ flag_bytes[7]) == 0x54): score += 1
    if ((flag_bytes[59] + flag_bytes[6]) == ord('j')): score += 1
    if ((flag_bytes[17] + flag_bytes[28]) == ord('n')): score += 1
    if (flag_bytes[4] == 0x7b): score += 1
    if (flag_bytes[35] == 0x65): score += 1
    if ((flag_bytes[36] + flag_bytes[44]) == 0x100 - 0x6a): score += 1
    if (flag_bytes[63] == 0x7d): score += 1
    if ((flag_bytes[27] ^ flag_bytes[41]) == 0x5d): score += 1
    if (flag_bytes[40] == 0x62): score += 1
    if ((flag_bytes[24] ^ flag_bytes[21]) == 99): score += 1
    if ((flag_bytes[21] ^ flag_bytes[19]) == 0x52): score += 1
    if (flag_bytes[10] == 0x31): score += 1
    if ((flag_bytes[37] + flag_bytes[6]) == ord('g')): score += 1
    if (flag_bytes[6] == 0x7b): score += 1
    if (flag_bytes[56] == 0x93): score += 1
    if ((flag_bytes[9] ^ flag_bytes[29]) == 3): score += 1
    if (flag_bytes[47] == 199): score += 1
    if (flag_bytes[29] == 0x35): score += 1
    if (flag_bytes[63] == 0x7d): score += 1
    if ((flag_bytes[51] + flag_bytes[38]) == ord('G')): score += 1
    if ((flag_bytes[60] + flag_bytes[20]) == 0x100 - 0x6d): score += 1
    if ((flag_bytes[1] ^ flag_bytes[15]) == 0x74): score += 1
    if ((flag_bytes[11] ^ flag_bytes[58]) == 0x16): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if ((flag_bytes[0] + flag_bytes[63]) == 0x100 - 0x33): score += 1
    if (flag_bytes[60] == 0x32): score += 1
    if (flag_bytes[54] == 99): score += 1
    if (flag_bytes[7] == 0x4b): score += 1
    if ((flag_bytes[29] ^ flag_bytes[40]) == 0x57): score += 1
    if (flag_bytes[58] == 0x39): score += 1
    if ((flag_bytes[33] ^ flag_bytes[44]) == 0x56): score += 1
    if (flag_bytes[17] == 0x96): score += 1
    if (flag_bytes[19] == 0xab): score += 1
    if ((flag_bytes[59] + flag_bytes[51]) == 0x100 - 0x51): score += 1
    if (flag_bytes[21] == 0x7f): score += 1
    if ((flag_bytes[35] ^ flag_bytes[11]) == 0xd1): score += 1
    if (flag_bytes[40] == 0x62): score += 1
    if ((flag_bytes[18] ^ flag_bytes[13]) == 0x5e): score += 1
    if (flag_bytes[7] == 0x16): score += 1
    if ((flag_bytes[54] + flag_bytes[6]) == 0x100 - 0x69): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if (flag_bytes[45] == 0x37): score += 1
    if ((flag_bytes[19] + flag_bytes[5]) == ord('h')): score += 1
    if (flag_bytes[4] == 0x1a): score += 1
    if (flag_bytes[62] == 0x30): score += 1
    if ((flag_bytes[12] ^ flag_bytes[24]) == 4): score += 1
    if ((flag_bytes[46] + flag_bytes[32]) == 0x100 - 0x6a): score += 1
    if (flag_bytes[34] == 0x61): score += 1
    if (flag_bytes[3] == 0x46): score += 1
    if ((flag_bytes[11] + flag_bytes[47]) == 0x100 - 0x69): score += 1
    if (flag_bytes[46] == 0x32): score += 1
    if (flag_bytes[25] == 0x60): score += 1
    if (flag_bytes[9] == 0x36): score += 1
    if (flag_bytes[26] == 0x3a): score += 1
    if ((flag_bytes[55] ^ flag_bytes[42]) == 0xc): score += 1
    if ((flag_bytes[34] ^ flag_bytes[19]) == 0x57): score += 1
    if (flag_bytes[56] == 0x61): score += 1
    if ((flag_bytes[43] ^ flag_bytes[31]) == 0x51): score += 1
    if (flag_bytes[55] == 0x35): score += 1
    if (flag_bytes[9] == 0xa9): score += 1
    if ((flag_bytes[46] + flag_bytes[3]) == ord('x')): score += 1
    if (flag_bytes[48] == 0x1f): score += 1
    if ((flag_bytes[35] + flag_bytes[23]) == 0x100 - 99): score += 1
    if (flag_bytes[36] == ord('m')): score += 1
    if ((flag_bytes[30] ^ flag_bytes[28]) == 6): score += 1
    if (flag_bytes[53] == 0x30): score += 1
    if (flag_bytes[20] == 0xf7): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if ((flag_bytes[60] + flag_bytes[45]) == ord('i')): score += 1
    if ((flag_bytes[41] ^ flag_bytes[12]) == 5): score += 1
    if ((flag_bytes[9] ^ flag_bytes[42]) == 0x85): score += 1
    if (flag_bytes[32] == 100): score += 1
    if (flag_bytes[53] == 0x30): score += 1
    if ((flag_bytes[38] + flag_bytes[55]) == ord('g')): score += 1
    if (flag_bytes[32] == flag_bytes[13]): score += 1
    if (flag_bytes[36] == ord('2')): score += 1
    if (flag_bytes[23] == 0x9b): score += 1
    if (flag_bytes[13] == 100): score += 1
    if (flag_bytes[8] == 0x31): score += 1
    if (flag_bytes[36] == ord('2')): score += 1
    if (flag_bytes[14] == 0xc3): score += 1
    if ((flag_bytes[41] + flag_bytes[21]) == 0x100 - 0x69): score += 1
    if ((flag_bytes[45] + flag_bytes[37]) == ord('j')): score += 1
    if (flag_bytes[32] == 0x32): score += 1
    if (flag_bytes[44] == 100): score += 1
    if (flag_bytes[2] == 0x54): score += 1
    if ((flag_bytes[35] ^ flag_bytes[50]) == 0x54): score += 1
    if (flag_bytes[51] == 0x32): score += 1
    if (flag_bytes[48] == 0x35): score += 1
    if (flag_bytes[41] == 0x33): score += 1
    if (flag_bytes[27] == 0x32): score += 1
    if ((flag_bytes[49] + flag_bytes[59]) == 0x100 - 0x69): score += 1
    if (flag_bytes[36] == ord('2')): score += 1
    if (flag_bytes[22] == 0x61): score += 1
    if ((flag_bytes[55] + flag_bytes[4]) == ord('\x12')): score += 1
    if (flag_bytes[46] == 0x9e): score += 1
    if ((flag_bytes[22] ^ flag_bytes[31]) == 0x55): score += 1
    if (flag_bytes[50] == 0x43): score += 1
    if (flag_bytes[23] == 0x38): score += 1
    if (flag_bytes[52] == 0xc): score += 1
    if (flag_bytes[52] == 0x30): score += 1
    if (flag_bytes[22] == 0x61): score += 1
    if (flag_bytes[14] == 0x36): score += 1
    if (flag_bytes[2] == 0x54): score += 1
    if ((flag_bytes[8] ^ flag_bytes[22]) == 0x50): score += 1
    if ((flag_bytes[35] + flag_bytes[0]) == 0x100 - 0x59): score += 1
    if ((flag_bytes[39] + flag_bytes[2]) == 0x100 - 0x39): score += 1
    if ((flag_bytes[41] ^ flag_bytes[6]) == 7): score += 1
    if ((flag_bytes[33] + flag_bytes[11]) == 0x100 - 0x5b): score += 1
    if (flag_bytes[25] == 0x62): score += 1
    if (flag_bytes[26] == 0x31): score += 1
    if ((flag_bytes[20] + flag_bytes[27]) == ord('#')): score += 1
    if ((flag_bytes[6] ^ flag_bytes[35]) == 0x9c): score += 1
    if ((flag_bytes[14] ^ flag_bytes[11]) == 4): score += 1
    if (flag_bytes[39] == ord('4')): score += 1
    if ((flag_bytes[40] + flag_bytes[31]) == 0x100 - 0x6a): score += 1
    if (flag_bytes[57] == 99): score += 1
    if (flag_bytes[7] == 100): score += 1
    if (flag_bytes[14] == 0x36): score += 1
    if (flag_bytes[5] == 0x43): score += 1
    if ((flag_bytes[23] ^ flag_bytes[22]) == 0x59): score += 1
    if (flag_bytes[21] == 100): score += 1
    if ((flag_bytes[22] ^ flag_bytes[44]) == 5): score += 1
    if (flag_bytes[53] == 0x30): score += 1
    if (flag_bytes[31] == 0x34): score += 1
    if (flag_bytes[22] == 0x61): score += 1
    if ((flag_bytes[46] + flag_bytes[8]) == ord('z')): score += 1
    if ((flag_bytes[25] ^ flag_bytes[3]) == 0x24): score += 1
    if (flag_bytes[43] == 0x65): score += 1
    if (flag_bytes[44] == 0xf): score += 1
    if ((flag_bytes[16] ^ flag_bytes[21]) == 0x57): score += 1
    if ((flag_bytes[9] ^ flag_bytes[62]) == 6): score += 1
    if (flag_bytes[27] == 0x32): score += 1
    if ((flag_bytes[18] + flag_bytes[54]) == 0x100 - 0x2f): score += 1
    if (flag_bytes[32] == 100): score += 1
    if ((flag_bytes[57] + flag_bytes[18]) == 0x100 - 0x39): score += 1
    if ((flag_bytes[43] ^ flag_bytes[32]) == 1): score += 1
    if (flag_bytes[17] == 0xa4): score += 1
    if ((flag_bytes[8] ^ flag_bytes[9]) == 7): score += 1
    if (flag_bytes[40] == 0x62): score += 1
    if ((flag_bytes[56] + flag_bytes[4]) == ord('\n')): score += 1
    if ((flag_bytes[21] + flag_bytes[28]) == 0x100 - 0x67): score += 1
    if (flag_bytes[12] == 0x7c): score += 1
    if ((flag_bytes[63] + flag_bytes[18]) == 0x100 - 0x1f): score += 1
    if (flag_bytes[27] == 0x32): score += 1
    if (flag_bytes[23] == 0x38): score += 1
    if ((flag_bytes[44] + flag_bytes[18]) == 0x100 - 0x38): score += 1
    if ((flag_bytes[9] + flag_bytes[19]) == ord('l')): score += 1
    if ((flag_bytes[61] + flag_bytes[11]) == 0x100 - 0x19): score += 1
    if (flag_bytes[21] == 100): score += 1
    if ((flag_bytes[57] + flag_bytes[31]) == 0x100 - 0x69): score += 1
    if ((flag_bytes[28] ^ flag_bytes[40]) == 0x57): score += 1
    if (flag_bytes[45] == 0x37): score += 1
    if ((flag_bytes[13] + flag_bytes[47]) == 0x100 - 0x37): score += 1
    if (flag_bytes[18] == 100): score += 1
    if (flag_bytes[15] == 0x37): score += 1
    if ((flag_bytes[58] ^ flag_bytes[16]) == 10): score += 1
    if ((flag_bytes[0] ^ flag_bytes[21]) == 0x34): score += 1
    if ((flag_bytes[62] + flag_bytes[49]) == 0x100 - 0x6f): score += 1
    if (flag_bytes[46] == 0x32): score += 1
    if ((flag_bytes[57] + flag_bytes[0]) == 0x100 - 0x58): score += 1
    if (flag_bytes[36] == ord('2')): score += 1
    if (flag_bytes[50] == 0x31): score += 1
    if (flag_bytes[48] == 0x35): score += 1
    if (flag_bytes[42] == 0x39): score += 1
    if ((flag_bytes[61] + flag_bytes[35]) == 0x100 - 0x6b): score += 1
    if ((flag_bytes[27] + flag_bytes[1]) == ord('u')): score += 1
    if (flag_bytes[48] == 0x35): score += 1
    if ((flag_bytes[35] ^ flag_bytes[33]) == 0x51): score += 1
    if ((flag_bytes[29] ^ flag_bytes[57]) == 0x56): score += 1
    if (flag_bytes[23] == 0x4b): score += 1
    if ((flag_bytes[31] + flag_bytes[13]) == 0x100 - 0x54): score += 1
    if (flag_bytes[39] == ord('J')): score += 1
    if (flag_bytes[39] == ord('4')): score += 1
    if (flag_bytes[33] == 0x73): score += 1
    if (flag_bytes[7] == 100): score += 1
    if (flag_bytes[0] == 0x50): score += 1
    if (flag_bytes[22] == 0x61): score += 1
    if ((flag_bytes[62] + flag_bytes[55]) == ord('e')): score += 1
    if (flag_bytes[52] == 0x30): score += 1
    if ((flag_bytes[7] + flag_bytes[22]) == 0x100 - 0x34): score += 1
    if ((flag_bytes[26] ^ flag_bytes[14]) == 7): score += 1
    if (flag_bytes[2] == 0x54): score += 1
    if (flag_bytes[46] == 0x32): score += 1
    if (flag_bytes[52] == 0x30): score += 1
    if ((flag_bytes[54] ^ flag_bytes[35]) == 6): score += 1
    if ((flag_bytes[31] ^ flag_bytes[34]) == 0x55): score += 1
    if (flag_bytes[33] == 0x32): score += 1
    if ((flag_bytes[40] + flag_bytes[33]) == 0x100 - 0x6c): score += 1
    if (flag_bytes[7] == 100): score += 1
    if (flag_bytes[15] == 0x37): score += 1
    if ((flag_bytes[10] ^ flag_bytes[43]) == 0x54): score += 1
    if (flag_bytes[15] == 0x37): score += 1
    if ((flag_bytes[29] + flag_bytes[30]) == ord('h')): score += 1
    if ((flag_bytes[43] ^ flag_bytes[13]) == 1): score += 1
    if ((flag_bytes[58] + flag_bytes[24]) == 0x100 - 0x27): score += 1
    if ((flag_bytes[17] + flag_bytes[61]) == ord('i')): score += 1
    if (flag_bytes[41] == 0xa6): score += 1
    if ((flag_bytes[54] ^ flag_bytes[24]) == 0x51): score += 1
    if (flag_bytes[62] == 0x30): score += 1
    if ((flag_bytes[57] + flag_bytes[37]) == 0x100 - 0x6a): score += 1
    if ((flag_bytes[61] ^ flag_bytes[4]) == 0x4b): score += 1
    if ((flag_bytes[37] + flag_bytes[52]) == ord('c')): score += 1
    if ((flag_bytes[21] ^ flag_bytes[26]) == 0x3d): score += 1
    if (flag_bytes[50] == 0xe9): score += 1
    if ((flag_bytes[5] ^ flag_bytes[29]) == 7): score += 1
    if (flag_bytes[31] == 0x34): score += 1
    if (flag_bytes[53] == 1): score += 1
    if ((flag_bytes[15] + flag_bytes[7]) == 0x100 - 0x65): score += 1
    if (flag_bytes[41] == 0x33): score += 1
    if ((flag_bytes[35] + flag_bytes[27]) == 0x100 - 0x69): score += 1
    if (flag_bytes[42] == 0x39): score += 1
    if (flag_bytes[27] == 0x32): score += 1
    if (flag_bytes[47] == 0x65): score += 1
    if ((flag_bytes[45] ^ flag_bytes[30]) == 4): score += 1
    if (flag_bytes[30] == 0x33): score += 1
    if (flag_bytes[22] == 0x61): score += 1
    if (flag_bytes[49] == 0x61): score += 1
    if ((flag_bytes[31] + flag_bytes[21]) == 0x100 - 0x68): score += 1
    if (flag_bytes[24] == 0x32): score += 1
    if (flag_bytes[15] == 0x37): score += 1
    if (flag_bytes[35] == 0xcb): score += 1
    if ((flag_bytes[4] + flag_bytes[37]) == 0x100 - 0x52): score += 1
    if (flag_bytes[49] == 0x61): score += 1
    if ((flag_bytes[7] ^ flag_bytes[31]) == 0x50): score += 1
    if ((flag_bytes[15] + flag_bytes[19]) == ord('m')): score += 1
    if ((flag_bytes[30] ^ flag_bytes[22]) == 199): score += 1
    if ((flag_bytes[16] ^ flag_bytes[60]) == 1): score += 1
    if (flag_bytes[12] == 0x36): score += 1
    if (flag_bytes[28] == 1): score += 1
    if ((flag_bytes[44] + flag_bytes[58]) == 0x100 - 99): score += 1
    if ((flag_bytes[49] ^ flag_bytes[37]) == 0x52): score += 1
    if (flag_bytes[6] == 0x34): score += 1
    if (flag_bytes[38] == 0x32): score += 1
    if (flag_bytes[62] == 0x30): score += 1
    if ((flag_bytes[37] ^ flag_bytes[21]) == 0x57): score += 1
    if ((flag_bytes[40] + flag_bytes[5]) == 0x100 - 0x6c): score += 1
    if ((flag_bytes[11] + flag_bytes[34]) == 0x100 - 0x6d): score += 1
    if (flag_bytes[43] == 0x99): score += 1
    if ((flag_bytes[22] + flag_bytes[27]) == 0x100 - 0x78): score += 1
    if (flag_bytes[46] == flag_bytes[38]): score += 1
    if ((flag_bytes[48] ^ flag_bytes[61]) == 5): score += 1
    if (flag_bytes[12] == 0x56): score += 1
    if ((flag_bytes[44] ^ flag_bytes[28]) == 0x51): score += 1
    if (flag_bytes[45] == 0x37): score += 1
    if ((flag_bytes[37] ^ flag_bytes[2]) == 0x67): score += 1
    if ((flag_bytes[54] ^ flag_bytes[16]) == 0x7b): score += 1
    if ((flag_bytes[45] ^ flag_bytes[18]) == 0x91): score += 1
    if (flag_bytes[18] == 100): score += 1
    return score

if __name__ == "__main__":
    flag = "PCTF{24d16126d6739d6ada82b125534d2ae2324b39ed72e5a1200c5ac96200}"
    print(f"{flag} -> score = {hex(get_score(flag))}")
    