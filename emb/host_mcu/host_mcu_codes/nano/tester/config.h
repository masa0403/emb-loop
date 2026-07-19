#ifndef CONFIG_H
#define CONFIG_H

constexpr uint32_t SERIAL_BAUD = 115200;

constexpr uint8_t EVENT_BUFFER_SIZE = 64;

constexpr const char* TESTER_NAME = "NanoTester01";

constexpr const char* TESTER_VERSION = "1.0";

constexpr uint8_t MONITOR_COUNT = 3;

constexpr uint8_t MONITOR_PINS[MONITOR_COUNT] =
{
    7,
    8,
    9
};

constexpr const char* MONITOR_NAMES[MONITOR_COUNT] =
{
    "attiny202.PA2",
    "attiny202.PA3",
    "attiny202.PA6"
};

#endif