#ifndef RING_BUFFER_H
#define RING_BUFFER_H

#include "event.h"
#include "config.h"

class RingBuffer
{
public:

    RingBuffer();

    bool push(const PinEvent& event);

    bool pop(PinEvent& event);

    bool empty() const;

    bool full() const;

private:

    PinEvent buffer[EVENT_BUFFER_SIZE];

    volatile uint8_t head;

    volatile uint8_t tail;

    volatile uint8_t count;
};

#endif