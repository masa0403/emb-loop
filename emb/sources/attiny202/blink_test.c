
#include <avr/io.h>

int main(void) {
    PORTA.PIN3CTRL |= PORT_PULLUPEN_bm;

    PORTA.DIRSET = PIN2_bm;  // PA2 output
    PORTA.DIRCLR = PIN3_bm;  // PA3 input

    while (1) {
        if (PORTA.IN & PIN3_bm) {
            PORTA.OUTSET = PIN2_bm;
        } else {
            PORTA.OUTCLR = PIN2_bm;
        }
    }
}
