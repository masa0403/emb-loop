#include <avr/io.h>
#include <util/delay.h>
#include "logger.h"

void uart_tx(char c) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}

void logger_init() {
    // 115200 baud
    UBRR0H = 0;
    UBRR0L = 8;  // 16MHz / (16 * 115200) - 1 ≈ 8
    UCSR0B = (1 << TXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void logger_print(const char *s) {
    while (*s) {
        uart_tx(*s++);
    }
    uart_tx('\n');
}

// ★当時の高速サンプリングロガー
void logger_sample_pd7() {
    uint16_t count = 0;
    uint16_t timeout = 30000;  // 約30ms

    while (count < timeout) {
        if (PIND & (1 << PD7)) {
            logger_print("PD7_HIGH");
            return;
        }
        _delay_us(10);
        count++;
    }

    logger_print("PD7_LOW");
}
