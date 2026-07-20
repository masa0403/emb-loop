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

        // 仮実装
        logger.logPWM(name,50);
    }
    else
    {
        logger.log(name, EVENT_FALL);
    }

    detectPWM(currentState);

    lastState = currentState;

}

void PinMonitor::detectPWM(uint8_t currentState)
{
    uint32_t now = micros();

    if(currentState == HIGH)
    {
        // 前周期が存在するならDutyを計算
        if(lastPeriodStart != 0)
        {
            uint32_t period = now - lastPeriodStart;

            uint32_t highTime = now - riseTime;

            if(period > 0)
            {
                uint16_t duty =
                    (highTime * 100) / period;

                logger.logPWM(name, duty);
            }
        }

        riseTime = now;
        lastPeriodStart = now;
    }
}