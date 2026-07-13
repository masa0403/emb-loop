#eemb/backend/avr/compile.py
from pathlib import Path
import subprocess
from emb.path import BUILD, PACKAGE, SOURCES


# -----------------------------
# コンパイル
# -----------------------------
def compile_source(source_file, toolchain, board):
    source = Path(source_file)

    # 相対パスはカレントディレクトリ基準
    if not source.is_absolute():
        source = Path.cwd() / source

    candidates = [
        PACKAGE / source_file,
        SOURCES / board / source_file,
        SOURCES / source_file,
        source,
    ]

    for c in candidates:
        if Path(c).exists():
            source = Path(c).resolve()
            break
    else:
        raise FileNotFoundError(source_file)

    ...


    base = source.stem
    mcu = toolchain["mcu"]
    gcc = toolchain["avr_gcc"]
    objcopy = toolchain["avr_objcopy"]


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