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

    event.value = 0;

    buffer.push(event);
}

void Logger::logPWM(
    const char* pin,
    uint16_t duty)
{
    PinEvent event;

    event.sequence = sequence++;

    event.time_us = micros();

    event.pinName = pin;

    event.type = EVENT_PWM;

    event.value = duty;

    buffer.push(event);
}
bool Logger::getEvent(PinEvent& event)
{
    return buffer.pop(event);
}

void Logger::onEvent(const PinEvent& event)
{
    logger.buffer.push(event);
}