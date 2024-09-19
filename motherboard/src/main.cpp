#include "pico/stdlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <pico/stdio_usb.h>
//#include "ff_stdio.h"


//FreeRTOS
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"



TaskHandle_t usbCommTaskHandle;

void usbComm(void *param)
{
    sleep_ms(500);
    printf("usbComm");
    sleep_ms(500);

    // while(!stdio_usb_connected())
    // {
    //     sleep_ms(100);
    // }
    // printf("stdio_usb_connected()\n");

    // uint16_t tokens = 0, year, month, day, hour, minute, second;
    // char inputBuffer[64];
    // while(tokens != 6)
    // {
    //     // Set the RTC date/time.
    //     printf("Enter the current time. e.g. 2022-10-05 19:45:19\n");
        
    //     tokens = scanf("%hu-%hu-%hu %hu:%hu:%hu", &year, &month, &day, &hour, &minute, &second);
    //     if(tokens != 6)
    //     {
    //         printf("Unable to parse date/time.\n");
    //         sleep_ms(1000);
    //     }
    // }


    while (!stdio_usb_connected())
    {
        sleep_ms(100);
    }
    printf("stdio_usb_connected()\n");

    sleep_ms(500);
    printf("Enter String: ");
    sleep_ms(500);
    char buf[50];
    scanf("%s",buf);

    while (true){


        printf("Output: %s\n", buf);
        printf("\n");

        

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


    xTaskCreate(usbComm, "USB_COMM_TASK", configMINIMAL_STACK_SIZE, NULL, 1, &usbCommTaskHandle);

    vTaskStartScheduler();

    return 0;
}