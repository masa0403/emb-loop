#include "logger.h"

Logger logger;

Logger::Logger()
{
    sequence = 0;
}

void Logger::begin()
{
}

void Logger::log(const char* pinName,EventType type)
{
    PinEvent event;

    event.sequence = sequence++;

    event.time_us = micros();

    event.pinName = pinName;

    event.type = type;

    buffer.push(event);
}

bool Logger::getEvent(PinEvent& event)
{
    return buffer.pop(event);
}