from pathlib import Path
from .toolchain import (
    find_avr_gcc,
    find_avr_objcopy
)
import subprocess
from emb.path import BUILD, PACKAGE, EXAMPLES

# -----------------------------
# コンパイル
# -----------------------------
def compile_source(
        source_file,
        toolchain
    ):

    source = Path(source_file)

    if not source.is_absolute():

        candidates = [
            PACKAGE / source,
            EXAMPLES / source,
            source,
        ]

        for c in candidates:
            if c.exists():
                source = c.resolve()
                break
        else:
            raise FileNotFoundError(source_file)

    base = source.stem
    mcu = toolchain["mcu"]
    gcc = toolchain["gcc"]
    objcopy = toolchain["objcopy"]

    build_dir = BUILD
    build_dir.mkdir(exist_ok=True)

    elf = build_dir / f"{base}.elf"
    hex_file = build_dir / f"{base}.hex"


    print("Compiling...")


    subprocess.check_call([
        gcc,
        "-mmcu=" + mcu,
        "-Os",
        "-DF_CPU=5000000UL",
        str(source),
        "-o",
        str(elf)
    ])


    print("Creating HEX...")


    subprocess.check_call([
        objcopy,
        "-O",
        "ihex",
        str(elf),
        str(hex_file)
    ])


    print("Compile OK")

    return str(hex_file)