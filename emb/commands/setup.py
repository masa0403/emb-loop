from emb.backend.avr.toolchain import resolve_toolchain
from emb.backend.avr.programmer import install_jtag2updi


def main(args):

    if len(args) != 2:

        print("Usage:")
        print("  python -m emb setup nano COM3")
        return

    board = args[0]
    port = args[1]

    if board.lower() != "nano":
        raise ValueError("Currently only nano is supported.")

    toolchain = resolve_toolchain("attiny202")

    install_jtag2updi(
        port,
        toolchain
    )