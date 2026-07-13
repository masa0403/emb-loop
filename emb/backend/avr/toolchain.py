from pathlib import Path
import subprocess

# ============================================================
# AVR 専用 toolchain 自動セットアップ
# ============================================================

DXCORE_TOOLS = Path.home() / ".arduino15/packages/DxCore/tools"

MEGATINYCORE_URL = (
    "https://raw.githubusercontent.com/SpenceKonde/ReleaseScripts/"
    "refs/heads/master/package_drazzy.com_index.json"
)

# ------------------------------------------------------------
# 再帰的にファイルを探す
# ------------------------------------------------------------
def find_file(base: Path, name: str) -> str:
    # bin/ を優先
    for path in base.rglob("bin/" + name):
        if path.is_file():
            return str(path)

    # fallback
    for path in base.rglob("*"):
        if path.is_file() and path.name == name:
            return str(path)

    raise FileNotFoundError(f"{name} not found under {base}")



# ------------------------------------------------------------
# MegaTinyCore を Arduino CLI で自動インストール
# ------------------------------------------------------------
def install_megatinycore():
    print("[toolchain] Installing MegaTinyCore via Arduino CLI...")

    subprocess.check_call([
        "arduino-cli", "config", "set",
        "board_manager.additional_urls", MEGATINYCORE_URL
    ])

    subprocess.check_call(["arduino-cli", "core", "update-index"])
    subprocess.check_call(["arduino-cli", "core", "install", "megaTinyCore:megaavr"])

    print("[toolchain] MegaTinyCore installation complete.")


# ------------------------------------------------------------
# AVR toolchain を解決（AVR専用）
# ------------------------------------------------------------
def resolve_avr_toolchain(board: str):
    print(f"[toolchain] Resolving AVR toolchain for {board}...")

    # ------------------------------------------------------------
    # ATtiny202 / tinyAVR 系 (DxCore)
    # ------------------------------------------------------------
    if board in ["attiny202", "attiny402", "attiny412", "attiny1614", "attiny3216"]:
        if not DXCORE_TOOLS.exists():
            print("[toolchain] DxCore toolchain not found.")
            install_megatinycore()

        avr_gcc = find_file(DXCORE_TOOLS, "avr-gcc")
        avr_objcopy = find_file(DXCORE_TOOLS, "avr-objcopy")
        avrdude = find_file(DXCORE_TOOLS, "avrdude")
        avrdude_conf = find_file(DXCORE_TOOLS, "avrdude.conf")

        return {
            "mcu": board,
            "avr_gcc": avr_gcc,
            "avr_objcopy": avr_objcopy,
            "avrdude": avrdude,
            "avrdude_conf": avrdude_conf
        }

    # ------------------------------------------------------------
    # Arduino Nano (ATmega328P)
    # ------------------------------------------------------------
    elif board == "nano":
        return {
            "mcu": "atmega328p",
            "programmer": "arduino",
            "avr_gcc": "/usr/bin/avr-gcc",
            "avr_objcopy": "/usr/bin/avr-objcopy",
            "avrdude": "/usr/bin/avrdude",
            "avrdude_conf": "/etc/avrdude.conf"
        }

    else:
        raise ValueError(f"Unknown board: {board}")
