import serial
import json
import time
import os

def run_tester_session(board, port):
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(1)

    log = []
    start = time.time()

    while time.time() - start < 3.0:
        line = ser.readline().decode().strip()
        if line:
            log.append(line)

    ser.close()

    # 新しい成功判定ロジック
    ok = (
        "D8_HIGH" in log and
        "PA2_HIGH" in log and
        "PA2_LOW" in log and
        "PA6_HIGH_END" in log
    )

    result = {
        "board": board,
        "result": "pass" if ok else "fail",
        "log": log
    }

    os.makedirs(f"logs/{board}", exist_ok=True)
    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    path = f"logs/{board}/{ts}.json"

    with open(path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[tester] JSON saved: {path}")
