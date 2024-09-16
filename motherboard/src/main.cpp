#include "pico/stdlib.h"
#include <stdio.h>
#include <stdlib.h>

//FreeRTOS
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

TaskHandle_t helloWorldTaskHandle;

void helloWorld(void *param)
{

    while (true){
    sleep_ms(1000);
    printf("This means that freertos is working");
    sleep_ms(1000);
    }
}

int main(int argc, char** argv) {
    stdio_init_all();

    // This is the LED
    gpio_init(25);
    gpio_set_dir(25, GPIO_OUT);

    // Blink 5 times in 10 seconds
    for (int index = 0; index < 10; index++) {
        gpio_put(25,index % 2);
        sleep_ms(1000);
        printf("%d \n", index);
    }

    xTaskCreate(helloWorld, "HELLO_WORLD_TASK",128,NULL, 1, &helloWorldTaskHandle);

    vTaskStartScheduler();

    return 0;
}