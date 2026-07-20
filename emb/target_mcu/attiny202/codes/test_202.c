#include <avr/io.h>

int main(void)
{
    PORTA.DIRSET = PIN2_bm;

    while(1)
    {
    }
}