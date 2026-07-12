# emb/commands/setup.py

import sys
from emb.backend.setup.ubuntu import check_avr_toolchain
from emb.backend.avr.toolchain import resolve_avr_toolchain
from emb.backend.avr.flash import flash
from emb.backend.avr.compile import compile_source

def main(args):
    if len(args) == 0:
        print("Usage: emb setup <target>")
        return

    target = args[0].lower()

    if target == "nano":
        print("Nano setup is not implemented in this snippet.")
        return

    elif target == "attiny202":
        check_avr_toolchain()
        toolchain = resolve_toolchain("attiny202")
        port = args[2]
        source_file = args[1]
        file = compile_source(source_file, toolchain, target)
        flash(file, port, toolchain)
        return

    else:
        print(f"Unknown setup target: {target}")
        return
