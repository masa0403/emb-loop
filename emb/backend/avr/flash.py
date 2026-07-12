import subprocess
from datetime import datetime
from pathlib import Path
from emb.path import PACKAGE

# logs/ のルート
LOGS = PACKAGE.parent / "logs"

# ------------------------------------------------------------
# ログファイルのパスを生成（マイコン名ごとにフォルダを作る）
# ------------------------------------------------------------
def create_log_file(mcu: str) -> Path:
    # logs/attiny202/
    mcu_dir = LOGS / mcu
    mcu_dir.mkdir(parents=True, exist_ok=True)

    # 日付＋時刻入りファイル名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return mcu_dir / f"{timestamp}.txt"


# ------------------------------------------------------------
# 書き込み（AVR 専用）
# ------------------------------------------------------------
def flash(hex_file, toolchain, mcu, port):

    avrdude = toolchain["avrdude"]
    avrdude_conf = toolchain["avrdude_conf"]
    programmer = "jtag2updi"

    print("Writing...")

    # ログファイル生成
    log_file = create_log_file(mcu)

    # avrdude 実行（ログを取るため run() を使う）
    result = subprocess.run(
        [
            avrdude,
            "-C", avrdude_conf,
            "-p", mcu,
            "-c", programmer,
            "-P", port,
            "-U", f"flash:w:{hex_file}:i"
        ],
        capture_output=True,
        text=True
    )

    # ログ保存
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== STDOUT ===\n")
        f.write(result.stdout or "")
        f.write("\n\n=== STDERR ===\n")
        f.write(result.stderr or "")

    print(f"Log saved : {log_file}")

    # avrdude が失敗したら例外を投げる
    if result.returncode != 0:
        print("Flash failed.")
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args
        )

    print("Flashed!")
