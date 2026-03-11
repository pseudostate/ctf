#!/bin/bash
grep -i "117 " can.log | awk '{sub(/\r$/, ""); print substr($NF, length($NF)-1)}' | xxd -r -p
