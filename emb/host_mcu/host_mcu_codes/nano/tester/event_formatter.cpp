#include <Arduino.h>

#include "event_formatter.h"

void EventFormatter::print(const PinEvent& event)
{
    Serial.print(event.sequence);

    Serial.print(',');

    Serial.print(event.time_us);

    Serial.print(',');

    Serial.print(event.pinName);

    Serial.print(',');

    if(event.type == EVENT_RISE)
    {
        Serial.println("RISE");
    }
    else
    {
        Serial.println("FALL");
    }
}