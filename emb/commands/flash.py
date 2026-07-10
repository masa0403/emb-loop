from emb.backend.avr.compile import compile_source
from emb.backend.avr.flash import flash
from emb.backend.avr.toolchain import resolve_toolchain


import sys

def main(args):

    board = args[0]
    source = args[1]
    port = args[2]


    toolchain = resolve_toolchain(board)


    hex_file = compile_source(
        source,
        toolchain
    )


    flash(
        hex_file,
        port,
        toolchain
    )