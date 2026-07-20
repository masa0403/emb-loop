#include <avr/io.h>

int main(void)
{
    // PA2 output
    PORTA.DIRSET = PIN2_bm;

    // PA3 output
    PORTA.DIRSET = PIN3_bm;

    while (1)
    {
        // HIGH
        PORTA.OUTSET = PIN2_bm;
        PORTA.OUTSET = PIN3_bm;

        for (volatile uint32_t i = 0; i < 200000; i++);

        // LOW
        PORTA.OUTCLR = PIN2_bm;
        PORTA.OUTCLR = PIN3_bm;

        for (volatile uint32_t i = 0; i < 200000; i++);
    }
}