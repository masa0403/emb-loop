#ifndef PIN_MONITOR_H
#define PIN_MONITOR_H

#include <Arduino.h>

class PinMonitor
{
public:
    PinMonitor();

    void begin(uint8_t pin, const char* name);

    void update();

private:
    uint8_t pin;
    const char* name;
    uint8_t lastState;
};

#endif