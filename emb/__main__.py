import sys

from emb.commands.flash import main as flash_command


def main():

    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            " python -m emb <command>"
        )
        return


    command = sys.argv[1]


    if command == "flash":

        flash_command(
            sys.argv[2:]
        )

    elif command == "setup":

        from emb.commands.setup import main as setup_command

        setup_command(
            sys.argv[2:]
        )

    else:

        print(
            f"Unknown command: {command}"
        )


if __name__ == "__main__":
    main()