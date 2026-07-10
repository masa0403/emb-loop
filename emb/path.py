from pathlib import Path

PACKAGE = Path(__file__).resolve().parent

ROOT = PACKAGE

BOARDS = PACKAGE / "boards"
FIRMWARE = PACKAGE / "firmware"
EXAMPLES = PACKAGE / "examples"

BUILD = PACKAGE.parent / "build"
LOGS = PACKAGE.parent / "logs"