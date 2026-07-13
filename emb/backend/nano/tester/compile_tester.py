# emb/backend/nano/tester/compile_tester.py

import subprocess
import os

def compile_tester_firmware():
    src_dir = os.path.join("emb", "sources", "nano")
    build_dir = "build"
    os.makedirs(build_dir, exist_ok=True)

    elf_path = os.path.join(build_dir, "tester.elf")
    hex_path = os.path.join(build_dir, "tester.hex")

    subprocess.check_call([
        "/usr/bin/avr-gcc",
        "-mmcu=atmega328p",
        "-DF_CPU=16000000UL",
        "-Os",
        "-std=gnu99",
        "-Wall",
        "-Wextra",
        "-I", src_dir,
        os.path.join(src_dir, "main.c"),
        os.path.join(src_dir, "tester.c"),
        os.path.join(src_dir, "logger.c"),
        "-o", elf_path
    ])

    subprocess.check_call([
        "/usr/bin/avr-objcopy",
        "-O", "ihex",
        elf_path,
        hex_path
    ])

    return hex_path

