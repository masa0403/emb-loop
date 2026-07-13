#include <avr/io.h>
#include <util/delay.h>

#define INPUT_PIN 0   // Nano D8 = PB0 → ATtiny202 PA3
#define OUTPUT_PIN 7  // Nano D7 = PD7 ← ATtiny202 PA2

// UART 初期化
void uart_init() {
    UBRR0H = 0;
    UBRR0L = 8; // 115200 baud
    UCSR0B = (1 << TXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_send(char c) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}

void uart_print(const char* s) {
    while (*s) uart_send(*s++);
}

void uart_print_int(unsigned long v) {
    char buf[16];
    int i = 0;

    if (v == 0) {
        uart_send('0');
        return;
    }

    while (v > 0) {
        buf[i++] = '0' + (v % 10);
        v /= 10;
    }

    while (i--) uart_send(buf[i]);
}

int main(void) {
    uart_init();

    uart_print("[nano] start tester\n");

    // D8 = PB0 → 出力
    DDRB |= (1 << INPUT_PIN);

    // D7 = PD7 → 入力
    DDRD &= ~(1 << OUTPUT_PIN);

    uart_print("[nano] D8 HIGH (start)\n");

    // 入力 HIGH を保持しながら監視開始（ここが重要）
    PORTB |= (1 << INPUT_PIN);

    unsigned long output_time = 0;
    int prev = 0;

    // 最大 4000 回 = 約200ms 監視
    for (unsigned long i = 0; i < 4000; i++) {

        int now = (PIND & (1 << OUTPUT_PIN)) ? 1 : 0;

        // 立ち上がり検出（RISING）
        if (!prev && now) {
            output_time = i * 50;  // 50us * i
            uart_print("[nano] RISING detected at ");
            uart_print_int(output_time);
            uart_print(" us\n");
            break;
        }

        prev = now;
        _delay_us(50);
    }

    uart_print("[nano] D8 LOW (end)\n");
    PORTB &= ~(1 << INPUT_PIN);

    const char* result = (output_time > 0) ? "pass" : "fail";

    // JSON は最後に1行だけ送る（PC側が確実に拾える）
    uart_print("{\"input_time\":0,\"output_time\":");
    uart_print_int(output_time);
    uart_print(",\"delay_us\":");
    uart_print_int(output_time);
    uart_print(",\"result\":\"");
    uart_print(result);
    uart_print("\"}\n");

    while (1) {}
}
