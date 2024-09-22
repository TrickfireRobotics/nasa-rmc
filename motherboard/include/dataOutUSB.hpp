#ifndef DATA_OUT_USB_HPP
#define DATA_OUT_USB_HPP

#include <string>
#include "FreeRTOS.h"
#include "queue.h"
#include "semphr.h"

class DataOutUSB{



private:


public:
    QueueHandle_t dataToHostQueue;
    SemaphoreHandle_t dataMutex;

    inline static DataOutUSB* myObject = NULL;

    DataOutUSB();

    void writeToHost(std::string);
    void publish();

    static DataOutUSB* getObject();

    

    struct DataOutContainer{
        const std::string* stdString;
        int arrayLength;
    };

};


#endif