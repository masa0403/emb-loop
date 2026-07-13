#include <avr/io.h>
#include "logger.h"

void tester_run();

int main(void) {
    logger_init();
    tester_run();
    while (1);
}
