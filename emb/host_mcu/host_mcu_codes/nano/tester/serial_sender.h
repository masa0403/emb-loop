#ifndef SERIAL_SENDER_H
#define SERIAL_SENDER_H

class SerialSender
{
public:

    void begin();

    void update();

private:

    void printStartup();
};

extern SerialSender serialSender;

#endif