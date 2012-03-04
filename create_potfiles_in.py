#!/usr/bin/env python
import os
import re
import sys

# Paths to exclude
EXCLUSIONS = [
    '.',
    './tests',
    './po',
    './build',
]

POTFILE_IN = "po/POTFILES.in"

sys.stdout.write("Creating " + POTFILE_IN + " ... ")
sys.stdout.flush()
to_translate = []
for (dirpath, dirnames, filenames) in os.walk("."):
    for filename in filenames:
        if os.path.splitext(filename)[1] in (".py", ".in") \
                and dirpath not in EXCLUSIONS:
            to_translate.append(os.path.join(dirpath, filename))

f = open(POTFILE_IN, "wb")
for line in to_translate:
    f.write(line + "\n")

f.close()

print "Done"
