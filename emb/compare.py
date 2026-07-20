import json


HARDWARE_JSON = "target_mcu/attiny202/hardware.json"
LATEST_JSON = "logs/latest.json"
TEST_REQUEST_JSON = "requests/test_request.json"


def load_json(path):

    with open(path, "r") as f:
        return json.load(f)



# hardware.jsonから
# ATtiny202.PA2 → latest.json形式
# の対応表を作る
def create_pin_map(hardware):

    monitor_pins = hardware["host_mcu"]["monitor_pins"]

    pin_map = {}

    for host_pin, target_pin in monitor_pins.items():

        # target.PA2
        target_pin = target_pin.replace(
            "target.",
            ""
        )

        pin_map[host_pin] = (
            hardware["target_mcu"]["name"]
            + "."
            + target_pin
        )

    return pin_map



def normalize_event(event):

    return {
        "pin": event["pin"],
        "type": event["type"]
    }



def compare():

    hardware = load_json(
        HARDWARE_JSON
    )

    latest = load_json(
        LATEST_JSON
    )

    request = load_json(TEST_REQUEST_JSON)
    expected_events = request["expected_events"]


    # 現在はlatest.jsonが
    # ATtiny202.PA2形式なので
    # hardware変換は不要
    actual_events=[]


    for event in expected_events:

        actual_events.append(
            normalize_event(event)
        )


    missing=[]

    for event in expected_events:

        if event not in actual_events:

            missing.append(event)



    extra=[]

    for event in actual_events:

        if event not in expected_events:

            extra.append(event)



    if missing:

        status="FAIL"

    else:

        status="PASS"



    result={

        "status":status,

        "expected_count":len(expected_events),

        "actual_count":len(actual_events),

        "missing":missing,

        "extra":extra

    }


    output_path = "logs/result.json"

    with open(output_path, "w") as f:
        json.dump(
            result,
            f,
            indent=4
        )


    print(
        json.dumps(
            result,
            indent=4
        )
    )

    print(f"Result saved: {output_path}")


if __name__=="__main__":

    compare()