#emb/loop_nano_attiny202.py
from pathlib import Path
import subprocess
from host_mcu.code_utility import load_calib, detect_nano_port
from host_mcu.logger import measure_period, receive_serial_log
from host_mcu.compile_flash import (
    flash_avr,
    compile_nano_sketch,
    upload_nano_sketch,
    compile_avr
)
from serial_json import save_latest_json


def run_command(cmd):

    print(">>", " ".join(cmd))

    subprocess.check_call(cmd)



def generate_testplan():

    print("[Step0-1] Generate nano_test_plan")

    run_command([
        "python3",
        "generate_testplan.py"
    ])

def generate_nano_code():

    print("[Step0-3] Generate test_plan.cpp")

    run_command([
        "python3",
        "generate_nano_code.py"
    ])



# ---------------------------------------------------------
# Step 0: AI TestPlan Generation
# ---------------------------------------------------------

generate_testplan()

generate_nano_code()

# ---------------------------------------------------------
# Step 1: Target Flashing! Nano を再び JTAG2UPDI 化
# ---------------------------------------------------------
hex_path = Path("host_mcu/host_mcu_codes/nano/programmer/JTAG2UPDI.hex")
#flash_nano
flash_avr(hex_path, "nano", detect_nano_port())

# ---------------------------------------------------------
# Step 2: 補正済み F_CPU で ATtiny202 に本番コードを書き込む
# ---------------------------------------------------------
SOURCE_MAIN  = Path("target_mcu/attiny202/codes/test_202.c")
BOARD = "attiny202"
OUTPUT = Path("target_mcu/attiny202/codes_compiled")
OUTPUT.mkdir(exist_ok=True)
calib = load_calib()
f_cpu = f"{calib['attiny202']}UL"

print(f"Using calibrated F_CPU={f_cpu}")
#compile_attiny202
elf, hex_path = compile_avr(SOURCE_MAIN, BOARD, OUTPUT, f_cpu)
#flash_attiny202
flash_avr(hex_path, BOARD, detect_nano_port())


# ---------------------------------------------------------
# Step 3: Tester Flash! Nano にTesterを書き込む
# ---------------------------------------------------------
#cketch_path
NANO_SKETCH = Path("host_mcu/host_mcu_codes/nano/tester/tester.ino")

#compile_nano
compile_nano_sketch(NANO_SKETCH)
#flash_nano
upload_nano_sketch(NANO_SKETCH, detect_nano_port())

# ---------------------------------------------------------
# Step 4: Logging from Nano to PC
# ---------------------------------------------------------
#nano - PC
logs = receive_serial_log(5)
print(logs)

save_latest_json(logs)

print("[Step8] Compare result")

run_command([
    "python3",
    "compare.py"
])


print("[Step9] Generate AI feedback")

run_command([
    "python3",
    "generate_ai_feedback.py"
])