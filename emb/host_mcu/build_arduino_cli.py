from pathlib import Path
import subprocess
import os

# ------------------------------------------------------------
# ターゲットMCUを書き込みのためのArduino CLIをインストール
# ------------------------------------------------------------
def setup_arduino_cli():
    # emb/bin を基準ディレクトリにする
    base_dir = Path(__file__).resolve().parent.parent / "bin"
    base_dir.mkdir(parents=True, exist_ok=True)

    # install.sh は base_dir/bin にインストールする仕様
    bin_dir = base_dir / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    arduino_cli = bin_dir / "arduino-cli"

    # すでに存在するなら PATH を通して返す
    if arduino_cli.exists():
        os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"
        return str(arduino_cli)

    print("[setup] Installing Arduino CLI...")

    # install.sh を base_dir で実行すると bin/ が作られる
    subprocess.check_call(
        "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh",
        shell=True,
        cwd=str(base_dir)
    )

    # PATH を通す
    os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"

    print("[setup] Arduino CLI installed.")
    return str(arduino_cli)

# ------------------------------------------------------------
# インストールしたArduino CLIのパスを探す
# ------------------------------------------------------------
def find_file(base: Path, name: str) -> str:
    for path in base.rglob("bin/" + name):
        if path.is_file():
            return str(path)
    for path in base.rglob("*"):
        if path.is_file() and path.name == name:
            return str(path)
    raise FileNotFoundError(f"{name} not found under {base}")