#!/usr/bin/env python

import idaapi
import struct

EASYPATCHING_VERSION = "1.0"

def copy_file(src, dst):
    open(dst, "wb").write(open(src, "rb").read())

def apply_patch_byte(ea, fpos, org_val, patch_val):
    global patch_file

    if fpos != -1:
        patch_file.seek(fpos)
        patch_file.write(struct.pack("B", patch_val))

    return 0

def save_patched_file():
    global patch_file

    start_ea = 0x0
    end_ea = idaapi.cvar.inf.max_ea

    org_file = idaapi.get_root_filename()
    new_file = org_file + "-patched"

    try:
        copy_file(org_file, new_file)

        patch_file = open(new_file, "rb+")
        idaapi.visit_patched_bytes(start_ea, end_ea, apply_patch_byte)
        patch_file.close()

        print("Pached: {} -> {}".format(org_file, new_file))

    except FileNotFoundError:
        print("Original file not found: {}".format(org_file))

def PLUGIN_ENTRY():
    return easy_patching()

class easy_patching(idaapi.plugin_t):
    flags = idaapi.PLUGIN_UNL
    comment = "Easy patching with Ctrl+Alt+W"
    help = "Easy patching with Ctrl+Alt+W"
    wanted_name = "Easy Patching"
    wanted_hotkey = "Ctrl+Alt+W"

    def init(self):
        global easy_patching_init

        if "easy_patching_init" not in globals():
            print("Easy patching v{} (c) Hiroki Hada".format(EASYPATCHING_VERSION))

        easy_patching_init = True

        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        save_patched_file()

    def term(self):
        pass








