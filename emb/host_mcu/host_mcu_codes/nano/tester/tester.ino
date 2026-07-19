#include "logger.h"

#include "pin_monitor.h"

#include "serial_sender.h"

PinMonitor monitors[MONITOR_COUNT];

void setup()
{
    Serial.begin(SERIAL_BAUD);
    
    delay(2000);

    logger.begin();

    serialSender.begin();

    for (uint8_t i = 0; i < MONITOR_COUNT; i++)
    {
        monitors[i].begin(MONITOR_PINS[i], MONITOR_NAMES[i]);
    }
}

void loop()
{
    for(uint8_t i=0;i<MONITOR_COUNT;i++)
    {
        monitors[i].update();
    }
    serialSender.update();
}