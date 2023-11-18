#!/usr/bin/env python

import os
import glob

lib_dir = os.path.dirname(os.path.realpath(__file__))
pro_dir = os.getcwd()

print("Library directory: %s" % lib_dir)
print("Project directory: %s" % pro_dir)

# write sym-lib-table
table = []
table.append("(sym_lib_table")
for lib in glob.glob(os.path.join(lib_dir, '*.lib')):
    lib_name = os.path.splitext(os.path.basename(lib))[0]
    lib_path = os.path.relpath(lib, pro_dir)
    table.append("  (lib (name %s)(type Legacy)(uri ${KIPRJMOD}/%s)(options \"\")(descr \"\"))" % (lib_name, lib_path))
table.append(")")
sym_lib_table = "\n".join(table)
open("sym-lib-table", "w").write(sym_lib_table)

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
