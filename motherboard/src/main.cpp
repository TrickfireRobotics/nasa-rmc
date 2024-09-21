#include "pico/stdlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <pico/stdio_usb.h>
//#include "ff_stdio.h"


//FreeRTOS
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#include "../include/dataInUSB.hpp"



TaskHandle_t usbCommTaskHandle;

void usbComm(void *param)
{
    sleep_ms(500);
    printf("usbComm");
    sleep_ms(500);

    while (!stdio_usb_connected())
    {
        sleep_ms(100);
    }
    printf("stdio_usb_connected()\n");

    DataInUSB dataIn;

    while (true){
        sleep_ms(500);
        printf("Enter String: ");
        sleep_ms(500);

        dataIn.readNextUSBMessage();


        char buf[15];
        //scanf("%*s",buf);
        //fgets(buf, sizeof(buf),stdin);
        // if(fgets(buf, sizeof(buf),stdin) != NULL){
        //     for (int index = 0; index < 15; index++) {
        //         //printf("buf[%d] = %d\n", index, (int)buf[index]);
        //         printf("[%d] = (%d)%c\n", index, (int)buf[index], buf[index]);
        //     }

        // }
        // else {
        //     printf("NULL\n");
        // }


        // printf("Output: %s\n", buf);
        // printf("\n");

        

        sleep_ms(500);
    }
}




void tenSecDebugLED(){
    // Blink 5 times in 10 seconds
    for (int index = 0; index < 10; index++) {
        gpio_put(25,index % 2);
        sleep_ms(1000);
        printf("%d \n", index);
    }
}

void onBootInit(){
    stdio_init_all();

    // This is the LED
    gpio_init(25);
    gpio_set_dir(25, GPIO_OUT);
}

int main(int argc, char** argv) {
    onBootInit();

    #if (DEBUG)
        tenSecDebugLED();
    #endif


    xTaskCreate(usbComm, "USB_COMM_TASK", configMINIMAL_STACK_SIZE * 2, NULL, 1, &usbCommTaskHandle);

    vTaskStartScheduler();

    return 0;
}