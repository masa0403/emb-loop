import subprocess
from emb.path import LOGS


def create_log_file():

    LOGS.mkdir(parents=True, exist_ok=True)

    nums = []

    for f in LOGS.glob("*.txt"):
        try:
            nums.append(int(f.stem))
        except ValueError:
            pass

    next_num = max(nums, default=0) + 1

    return LOGS / f"{next_num:04d}.txt"

# -----------------------------
# 書き込み
# -----------------------------
def flash(
        hex_file,
        port,
        toolchain
    ):
    print("Writing...")

    log_file = create_log_file()

    programmer = toolchain["programmer"]
    baud = str(toolchain["baud"])

    avrdude = toolchain["avrdude"]
    conf = toolchain["avrdude_conf"]
    result = subprocess.run(
        [
            avrdude,
            "-C",
            conf,
            "-v",
            "-p",
            toolchain["mcu"],
            "-c",
            programmer,
            "-P",
            port,
            "-b",
            baud,
            "-U",
            f"flash:w:{hex_file}:i"
        ],
        text=True
    )

    # ログ保存
    with open(log_file, "w", encoding="utf-8") as f:

        if result.stdout:
            f.write(result.stdout)

        if result.stderr:
            f.write(result.stderr)

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args
        )

    print(f"Log saved : {log_file}")
    print("Done!")

