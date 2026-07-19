#emb/calib_nano_attiny202.py
from pathlib import Path

from host_mcu.compile_flash import (
    flash_avr,
    compile_nano_sketch,
    upload_nano_sketch,
    compile_avr
)
from host_mcu.code_utility import save_calib, load_calib, detect_nano_port
from host_mcu.pc_receive_log import measure_period



# ---------------------------------------------------------
# Step 1: Target Flash! Nano を JTAG2UPDI 化
# ---------------------------------------------------------
hex_path = Path("host_mcu/host_mcu_codes/nano/programmer/JTAG2UPDI.hex")
#flash_nano
flash_avr(hex_path, "nano", detect_nano_port())

# ---------------------------------------------------------
# Step 2: Target Flash! ATtiny202 に blink を書き込む
# ---------------------------------------------------------
SOURCE_CALIB = Path("target_mcu/attiny202/codes/blink.c")
BOARD = "attiny202"
OUTPUT = Path("target_mcu/attiny202/codes_compiled")
OUTPUT.mkdir(exist_ok=True)
f_cpu_guess = "20000000UL"

#compile_attiny202
elf, hex_path = compile_avr(SOURCE_CALIB, BOARD, OUTPUT, f_cpu_guess)
#compile_attiny202
flash_avr(hex_path, BOARD, detect_nano_port())



# ---------------------------------------------------------
# Step 3: Logger Flash! Nano に周期測定スケッチを書き込む
# ---------------------------------------------------------
#cketch_path
NANO_SKETCH = Path("host_mcu/host_mcu_codes/nano/calib/calib.ino")

#compile_nano
compile_nano_sketch(NANO_SKETCH)
#flash_nano
upload_nano_sketch(NANO_SKETCH, detect_nano_port())

# ---------------------------------------------------------
# Step 4: Logging! Nano で周期測定
# ---------------------------------------------------------
#nano - PC
period = measure_period()



# ---------------------------------------------------------
# Step 5: PC Thinking! F_CPU を計算して保存
# ---------------------------------------------------------
expected = 2.0  # ON→OFF→ON の 1周期
ratio = expected / period
f_cpu_real = int(20000000 * ratio)

print(f"Computed F_CPU = {f_cpu_real} Hz")
#save f_cpu to .json
save_calib({"attiny202": f_cpu_real})



# ---------------------------------------------------------
# Step 6: Target Flashing! Nano を再び JTAG2UPDI 化
# ---------------------------------------------------------
hex_path = Path("host_mcu/host_mcu_codes/nano/programmer/JTAG2UPDI.hex")
#flash_nano
flash_avr(hex_path, "nano", detect_nano_port())

# ---------------------------------------------------------
# Step 7: 補正済み F_CPU で ATtiny202 に本番コードを書き込む
# ---------------------------------------------------------
SOURCE_MAIN  = Path("target_mcu/attiny202/codes/blink.c")
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