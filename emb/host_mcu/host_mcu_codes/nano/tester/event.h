#ifndef EVENT_H
#define EVENT_H

#include <Arduino.h>

#pragma once

#include <stdint.h>

enum EventType
{
    EVENT_RISE,
    EVENT_FALL,

    EVENT_PWM
};

struct PinEvent
{
    uint32_t sequence;

    uint32_t time_us;

    const char* pinName;

    EventType type;

    uint16_t value;
};
#endif