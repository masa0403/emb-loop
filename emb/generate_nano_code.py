import json


INPUT = "logs/nano_test_plan.json"
HARDWARE = "target_mcu/attiny202/hardware.json"

OUTPUT = (
    "host_mcu/host_mcu_codes/nano/tester/test_plan.cpp"
)


def convert_command(cmd):

    name = cmd["cmd"]

    if name == "DELAY":

        return (
            f"    {{CMD_DELAY,0,{cmd['value']}}}"
        )


    if name == "PIN_HIGH":

        pin = cmd["pin"].replace("D","")

        return (
            f"    {{CMD_PIN_HIGH,{pin},0}}"
        )


    if name == "PIN_LOW":

        pin = cmd["pin"].replace("D","")

        return (
            f"    {{CMD_PIN_LOW,{pin},0}}"
        )


    if name == "END":

        return (
            "    {CMD_END,0,0}"
        )


    raise Exception(
        f"Unknown command {name}"
    )

def generate_config(commands, hardware):

    output_pins = []

    for cmd in commands:

        if cmd["cmd"] in (
            "PIN_HIGH",
            "PIN_LOW"
        ):

            pin = int(cmd["pin"].replace("D", ""))

            if pin not in output_pins:
                output_pins.append(pin)

    monitor_pins = []
    monitor_names = []

    for host_pin, target_pin in hardware["host_mcu"]["monitor_pins"].items():

        monitor_pins.append(
            int(host_pin.replace("D",""))
        )

        monitor_names.append(
            hardware["target_mcu"]["name"]
            + "."
            + target_pin.replace("target.","")
        )

    with open(
        "host_mcu/host_mcu_codes/nano/tester/generated_config.h",
        "w"
    ) as f:

        f.write("#pragma once\n\n")

        f.write(
            f"#define OUTPUT_PIN_COUNT {len(output_pins)}\n\n"
        )

        f.write(
            f"#define MONITOR_COUNT {len(monitor_pins)}\n\n"
        )

        f.write(
            "const uint8_t OUTPUT_PINS[] = {\n"
        )

        for pin in output_pins:

            f.write(f"    {pin},\n")

        f.write("};\n")

        f.write(
            "const uint8_t MONITOR_PINS[] = {\n"
        )

        for pin in monitor_pins:
            f.write(f"    {pin},\n")

        f.write("};\n\n")

        f.write(
            "const char* MONITOR_NAMES[] = {\n"
        )

        for name in monitor_names:
            f.write(f'    "{name}",\n')

        f.write("};\n")

def main():

    with open(INPUT) as f:
        data=json.load(f)

    with open(HARDWARE) as f:
        hardware = json.load(f)

    commands = data["commands"]


    lines=[]

    lines.append(
        '#include "test_plan.h"\n'
    )

    lines.append(
        "const TestCommand TEST_PLAN[] =\n"
    )

    lines.append(
        "{\n"
    )


    for cmd in commands:

        lines.append(
            convert_command(cmd)
            + ",\n\n"
        )


    lines.append(
        "};\n"
    )


    with open(OUTPUT,"w") as f:

        f.write(
            "".join(lines)
        )


    print(
        "test_plan.cpp generated"
    )

    generate_config(commands,hardware)

    print(
        "generated_config.h generated"
    )



if __name__=="__main__":

    main()