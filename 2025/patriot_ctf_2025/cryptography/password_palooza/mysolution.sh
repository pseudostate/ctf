#!/bin/sh

# -m 0 = MD5
# -a 6 = Hybrid Wordlist + Mask
# ?d = 0123456789
# --potfile-disable = not write potfile

hashcat -m 0 -a 6 "3a52fc83037bd2cb81c5a04e49c048a2" rockyou.txt ?d?d -O -w 1 --potfile-disable
