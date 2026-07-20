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

    uint16_t pwmValue = 0;

    uint32_t lastRise;

    bool pwmActive;

        uint32_t riseTime = 0;
    uint32_t lastPeriodStart = 0;

    void detectPWM(uint8_t currentState);
};

#endif