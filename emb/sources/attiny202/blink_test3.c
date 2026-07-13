#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
    // PA3 = 入力（Nano D8）
    PORTA.DIRCLR = PIN3_bm;
    PORTA.PIN3CTRL = PORT_PULLUPEN_bm;

    // PA2 = 出力（テスト対象）
    PORTA.DIRSET = PIN2_bm;

    // PA6 = 出力（終了フラグ）
    PORTA.DIRSET = PIN6_bm;

    // 初期状態
    PORTA.OUTCLR = PIN2_bm | PIN6_bm;

    while (1) {
        // PA3 が HIGH になったら開始
        if (PORTA.IN & PIN3_bm) {

            // PA2 を 0.5秒 HIGH
            PORTA.OUTSET = PIN2_bm;
            _delay_ms(500);

            // PA2 を LOW
            PORTA.OUTCLR = PIN2_bm;

            // PA6 を 0.5秒 HIGH（終了フラグ）
            PORTA.OUTSET = PIN6_bm;
            _delay_ms(500);

            // PA6 を LOW
            PORTA.OUTCLR = PIN6_bm;

            while (1); // 終了
        }
    }
}
