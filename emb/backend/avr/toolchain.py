from pathlib import Path
import subprocess
import shutil
import yaml
from emb.path import BOARDS

PACKAGES_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / "Arduino15"
    / "packages"
)

def find_tool(name):

    # -----------------------------
    # 1. PATH検索
    # -----------------------------
    path = shutil.which(name)

    if path:
        print(f"[toolchain] Found {name}: {path}")
        return path


    # -----------------------------
    # 2. Arduino IDE検索
    # -----------------------------
    arduino_dir = (
        Path.home()
        / "AppData"
        / "Local"
        / "Arduino15"
        / "packages"
    )

    if arduino_dir.exists():

        for exe in PACKAGES_DIR.rglob("*"):

            if not exe.is_file():
                continue

            if exe.name.lower() in [
                name.lower(),
                name.lower() + ".exe"
            ]:
                print(
                    f"[toolchain] Found {name}: {exe}"
                )

                return str(exe)


    raise FileNotFoundError(
        f"{name} not found"
    )

def find_avr_gcc():
    return find_tool("avr-gcc")


def find_avr_objcopy():
    return find_tool("avr-objcopy")


def load_board(board):

    board_file = (
        Path(__file__).parents[2]
        / "boards"
        / f"{board}.yaml"
    )

    if not board_file.exists():
        raise FileNotFoundError(
            f"Board definition not found: {board}"
        )


    with open(board_file, encoding="utf-8") as f:
        config = yaml.safe_load(f)


    return config

def resolve_toolchain(board):
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    yaml_file = (
        BOARDS
        / board
        / f"{board}.yaml"
    )

    if not yaml_file.exists():
        raise FileNotFoundError(yaml_file)

    with open(yaml_file, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["gcc"] = find_tool(
        config["tools"]["gcc"]
    )

    config["objcopy"] = find_tool(
        config["tools"]["objcopy"]
    )

    avr = find_best_avrdude(
        config["programmer"]
    )

    config["avrdude"] = avr["exe"]
    config["avrdude_conf"] = avr["conf"]

    return config


PACKAGES_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / "Arduino15"
    / "packages"
)


def find_best_avrdude(programmer):

    candidates = []

    for exe in PACKAGES_DIR.rglob("avrdude.exe"):

        conf = exe.parent.parent / "etc" / "avrdude.conf"

        if not conf.exists():
            continue

        candidates.append(
            {
                "exe": exe,
                "conf": conf
            }
        )

    if not candidates:
        raise FileNotFoundError(
            "No avrdude installation found."
        )

    print(
        f"[toolchain] Found {len(candidates)} avrdude candidates."
    )

    for candidate in candidates:

        exe = candidate["exe"]
        conf = candidate["conf"]

        print(
            f"[toolchain] Testing {exe}"
        )

        try:

            result = subprocess.run(
                [
                    str(exe),
                    "-C",
                    str(conf),
                    "-c",
                    "?"
                ],
                capture_output=True,
                text=True,
                timeout=5
            )

            text = (
                result.stdout
                +
                result.stderr
            ).lower()

            if programmer.lower() in text:

                print(
                    f"[toolchain] Selected {exe}"
                )

                return {
                    "exe": str(exe),
                    "conf": str(conf)
                }

        except Exception:

            continue

    raise RuntimeError(
        f"No avrdude supports '{programmer}'."
    )