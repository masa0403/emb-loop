#define F_CPU 20000000UL
#include <avr/io.h>
#include <util/delay.h>

// ---------------------------------------------------------
// PWM 初期化（PA6 = TCA0 WO0）
// ---------------------------------------------------------
void pwm_init() {
    PORTA.DIRSET = PIN6_bm;  // PA6 を出力

    // TCA0 をシングルモードで使う
    TCA0.SINGLE.CTRLA = TCA_SINGLE_CLKSEL_DIV1_gc;  // F_CPU / 1
    TCA0.SINGLE.CTRLB = TCA_SINGLE_WGMODE_SINGLESLOPE_gc |
                        TCA_SINGLE_CMP0EN_bm;        // WO0 を有効化

    TCA0.SINGLE.PER = 255;   // 8bit PWM
    TCA0.SINGLE.CMP0 = 0;    // 初期 duty = 0%
    TCA0.SINGLE.CTRLA |= TCA_SINGLE_ENABLE_bm;
}

// ---------------------------------------------------------
// PWM を 0→255 または 255→0 に 2秒かけて変化させる
// ---------------------------------------------------------
void pwm_ramp(uint8_t start, uint8_t end) {
    int16_t step = (end > start) ? 1 : -1;

    for (int16_t v = start; v != end; v += step) {
        TCA0.SINGLE.CMP0 = v;
        _delay_ms(2000.0 / 255.0);  // 約 7.8ms × 255 ≒ 2秒
    }
    TCA0.SINGLE.CMP0 = end;
}

// ---------------------------------------------------------
// エッジ検出（PA2, PA3）
// ---------------------------------------------------------
uint8_t wait_rising_edge(uint8_t pin_bm) {
    // LOW → HIGH の立ち上がりを待つ
    while (PORTA.IN & pin_bm);     // HIGH の間待つ
    while (!(PORTA.IN & pin_bm));  // LOW の間待つ
    return 1;
}

// ---------------------------------------------------------
// メイン
// ---------------------------------------------------------
int main(void) {
    // PA2, PA3 を入力
    PORTA.DIRCLR = PIN2_bm | PIN3_bm;

    pwm_init();

    while (1) {
        // PA2 が短時間 HIGH → PWM 0→100%
        if (wait_rising_edge(PIN2_bm)) {
            pwm_ramp(0, 255);
        }

        // PA3 が短時間 HIGH → PWM 100→0%
        if (wait_rising_edge(PIN3_bm)) {
            pwm_ramp(255, 0);
        }
    }
}
