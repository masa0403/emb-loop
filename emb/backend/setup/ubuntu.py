# emb/backend/setup/ubuntu.py

import shutil

TOOLS = {
    "avr-gcc": "gcc-avr",
    "avrdude": "avrdude",
}

def check_avr_toolchain():
    print("Checking AVR toolchain...\n")

    missing = []

    # avr-gcc と avrdude のチェック
    for exe, pkg in TOOLS.items():
        print(f"Checking {exe}...", end=" ")

        if shutil.which(exe):
            print("OK")
        else:
            print("NOT FOUND")
            missing.append(pkg)

    # avr-libc のチェック（特殊）
    print("Checking avr-libc...", end=" ")
    if shutil.which("avr-gcc"):
        print("OK")
    else:
        print("NOT FOUND")
        missing.append("avr-libc")

    if len(missing) == 0:
        print("\nEnvironment is ready.")
        return

    print("\nMissing packages:")
    for pkg in missing:
        print(f"- {pkg}")

    print("\nRun:")
    print("sudo apt update")
    print("sudo apt install " + " ".join(missing))
