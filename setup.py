#!/usr/bin/env python

import os
import sys
import glob
import re

lib_dir = os.path.dirname(os.path.realpath(__file__))
pro_dir = os.getcwd()

print("Library directory: %s" % lib_dir)
print("Project directory: %s" % pro_dir)

# find project file
pro_file = glob.glob("*.pro")
if pro_file == []:
    print("No project file found!")
    sys.exit(1)
pro_file = pro_file[0]
print("Project file: %s" % pro_file)

# read project file
config = open(pro_file).readlines()

# extract existing component libraries in project file
r = re.compile("LibName\d+=([0-9a-zA-Z_\-/]*)")
libs = [r.match(line).group(1) for line in config if r.match(line)]
config = [line for line in config if not r.match(line)]

# add new libraries
for lib in reversed(sorted(glob.glob(os.path.join(lib_dir, '*.lib')))):
    lib_path = os.path.splitext(os.path.relpath(lib, pro_dir))[0]
    if not lib_path in libs:
        libs.insert(0, lib_path)

# write changed project file
libs = ["LibName%d=%s\n" % (index + 1, name) for (index, name) in enumerate(libs)]
index = config.index("[eeschema/libraries]\n") + 1
for lib in reversed(libs):
    config.insert(index, lib)
open(pro_file, "w").write("".join(config))

# write fp-lib-table
table = []
table.append("(fp_lib_table")
for lib in glob.glob(os.path.join(lib_dir, '*.pretty')):
    lib_name = os.path.splitext(os.path.basename(lib))[0]
    lib_path = os.path.relpath(lib, pro_dir)
    table.append("  (lib (name %s)(type KiCad)(uri ${KIPRJMOD}/%s)(options \"\")(descr \"\"))" % (lib_name, lib_path))
table.append(")")
fp_lib_table = "\n".join(table)
open("fp-lib-table", "w").write(fp_lib_table)
