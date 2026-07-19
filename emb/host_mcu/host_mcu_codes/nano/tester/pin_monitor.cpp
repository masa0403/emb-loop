#include "pin_monitor.h"

#include "logger.h"

PinMonitor::PinMonitor()
{
}

void PinMonitor::begin(
    uint8_t p,
    const char* n)
{
    pin = p;

    name = n;

    pinMode(pin,INPUT);

    lastState=digitalRead(pin);
}
void PinMonitor::update()
{
    uint8_t currentState = digitalRead(pin);

    if(currentState == lastState)
        return;

    if(currentState == HIGH)
    {
        logger.log(name, EVENT_RISE);
    }
    else
    {
        logger.log(name, EVENT_FALL);
    }

    lastState = currentState;
}