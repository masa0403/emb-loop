#include "logger.h"

#include "pin_monitor.h"

#include "serial_sender.h"

#include "test_executor.h"

#include "event_bus.h"



PinMonitor monitors[MONITOR_COUNT];

void setup()
{
    Serial.begin(SERIAL_BAUD);
    
    delay(2000);

    logger.begin();

    eventBus.begin();

    serialSender.begin();

    for (uint8_t i = 0; i < MONITOR_COUNT; i++)
    {
        monitors[i].begin(MONITOR_PINS[i], MONITOR_NAMES[i]);
    }

    testExecutor.begin();

}

void loop()
{
    testExecutor.update();
    
    for(uint8_t i=0;i<MONITOR_COUNT;i++)
    {
        monitors[i].update();
    }

    serialSender.update();
}