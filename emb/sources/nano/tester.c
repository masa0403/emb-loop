#include <avr/io.h>
#include <util/delay.h>
#include "logger.h"

void tester_run() {
    // D8 = PB0 → OUTPUT（ATtiny202 PA3）
    DDRB |= (1 << PB0);

    // D7 = PD7 → INPUT（ATtiny202 PA2）
    DDRD &= ~(1 << PD7);

    // D9 = PB1 → INPUT（ATtiny202 PA6）
    DDRB &= ~(1 << PB1);

    logger_print("LOG_START");

    // 1秒前からログ開始
    for (uint16_t i = 0; i < 1000; i++) {
        if (PIND & (1 << PD7)) logger_print("PA2_HIGH_BEFORE");
        _delay_ms(1);
    }

    // 刺激：D8 を一瞬 HIGH
    PORTB |= (1 << PB0);
    logger_print("D8_HIGH");
    _delay_ms(20);
    PORTB &= ~(1 << PB0);

    // PA2 の変化をログ
    uint8_t pa2_prev = 0;
    uint16_t timeout = 5000; // 5秒

    for (uint16_t i = 0; i < timeout; i++) {

        uint8_t pa2_now = (PIND & (1 << PD7)) ? 1 : 0;

        if (pa2_now != pa2_prev) {
            if (pa2_now)
                logger_print("PA2_HIGH");
            else
                logger_print("PA2_LOW");

            pa2_prev = pa2_now;
        }

        // PA6(D9) が HIGH になったら終了
        if (PINB & (1 << PB1)) {
            logger_print("PA6_HIGH_END");
            return;
        }

        _delay_ms(1);
    }

    logger_print("TIMEOUT");
}
