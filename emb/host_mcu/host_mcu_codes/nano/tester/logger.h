#ifndef LOGGER_H
#define LOGGER_H

#include "ring_buffer.h"

class Logger
{
public:

    Logger();

    void begin();

    void log(const char* pinName,EventType type);

    void logPWM(const char* pin,uint16_t duty);

    bool getEvent(PinEvent& event);

private:

    RingBuffer buffer;

    uint32_t sequence;

    static void onEvent(const PinEvent& event);
};

extern Logger logger;

#endif