#include "ring_buffer.h"

RingBuffer::RingBuffer()
{
    head = 0;
    tail = 0;
    count = 0;
}

bool RingBuffer::push(const PinEvent& event)
{
    if (full())
        return false;

    buffer[head] = event;

    head++;

    if (head >= EVENT_BUFFER_SIZE)
        head = 0;

    count++;

    return true;
}

bool RingBuffer::pop(PinEvent& event)
{
    if (empty())
        return false;

    event = buffer[tail];

    tail++;

    if (tail >= EVENT_BUFFER_SIZE)
        tail = 0;

    count--;

    return true;
}

bool RingBuffer::empty() const
{
    return count == 0;
}

bool RingBuffer::full() const
{
    return count == EVENT_BUFFER_SIZE;
}