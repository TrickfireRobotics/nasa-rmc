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
#include "../include/dataOutUSB.hpp"



TaskHandle_t usbInTaskHandle;
TaskHandle_t usbOutTaskHandle;

QueueHandle_t dataToHostQueue;

void usbDataIn(void *param)
{
    while (!stdio_usb_connected())
    {
        sleep_ms(100);
    }
    printf("stdio_usb_connected()\n");

    DataInUSB dataIn;

    int counter = 0;

    while (true){
        printf("Enter String: ");

        dataIn.readNextUSBMessage();

        // std::string* heapstr = new std::string("what am I doing" + std::to_string(counter++) + "\n");
        // DataOutUSB::getObject()->writeToHost(heapstr);

        printf("\n");
    }
}

void usbDataOut(void *param){
    while (!stdio_usb_connected())
    {
        sleep_ms(200);
    }

    DataOutUSB usbOut;

    while(true){
        DataOutUSB::getObject()->publish();
        sleep_ms(2);
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

    xTaskCreate(usbDataIn, "USB_DATA_IN", configMINIMAL_STACK_SIZE * 2, NULL, 1, &usbInTaskHandle);
    xTaskCreate(usbDataOut, "USB_DATA_OUT", configMINIMAL_STACK_SIZE * 2, NULL, 2, &usbOutTaskHandle);

    vTaskStartScheduler();

    return 0;
}