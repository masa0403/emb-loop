#ifndef EVENT_H
#define EVENT_H

#include <Arduino.h>

enum EventType : uint8_t
{
    EVENT_RISE = 0,
    EVENT_FALL = 1
};

struct PinEvent
{
    uint32_t sequence;

    uint32_t time_us;

    const char* pinName;

    EventType type;
};

#endif