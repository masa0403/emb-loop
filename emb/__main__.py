import sys

from emb.commands.flash import main as flash_command

SUPPORTED_BOARDS = {
    "attiny202",
}

def main():

    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            " python -m emb <board> <source> <port>"
        )
        return

    first = sys.argv[1]

    # setupだけは特別扱い
    if first == "setup":

        from emb.commands.setup import main as setup_command

        setup_command(sys.argv[2:])
        return

    # ボード名なら自動でFlashパイプラインを開始
    if first in SUPPORTED_BOARDS:

        flash_command(sys.argv[1:])
        return

    print(f"Unknown board or command: {first}")


if __name__ == "__main__":
    main()