#include "serial_sender.h"

#include "logger.h"

#include "event_formatter.h"

#include "config.h"


SerialSender serialSender;

void SerialSender::begin()
{
    Serial.println("HELLO");

    delay(1000);

    printStartup();
}
void SerialSender::update()
{
    PinEvent event;

    while(logger.getEvent(event))
    {
        EventFormatter::print(event);
    }
}

void SerialSender::printStartup()
{
    Serial.println("#SYS,STATUS,BEGIN");

    Serial.print("#SYS,NAME,");
    Serial.println(TESTER_NAME);

    Serial.print("#SYS,VERSION,");
    Serial.println(TESTER_VERSION);

    for(uint8_t i = 0; i < MONITOR_COUNT; i++)
    {
        Serial.print("#SYS,MONITOR,");
        Serial.println(MONITOR_NAMES[i]);
    }

    Serial.println("#SYS,STATUS,READY");
}