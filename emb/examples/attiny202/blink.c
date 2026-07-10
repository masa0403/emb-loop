#include <avr/io.h>
#include <util/delay.h>


int main(void)
{
    PORTA.DIRSET = PIN2_bm;


    while(1)
    {
        PORTA.OUTSET = PIN2_bm;
        _delay_ms(100);


        PORTA.OUTCLR = PIN2_bm;
        _delay_ms(100);
    }


    return 0;
}