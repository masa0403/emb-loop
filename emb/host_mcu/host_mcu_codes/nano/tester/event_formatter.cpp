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

    switch(event.type)
    {
    case EVENT_RISE:

        Serial.println("RISE");

        break;

    case EVENT_FALL:

        Serial.println("FALL");

        break;

    case EVENT_PWM:

        Serial.print("PWM,");

        Serial.println(event.value);

        break;
    }
}