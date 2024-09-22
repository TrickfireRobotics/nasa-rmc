#include "../include/dataOutUSB.hpp"


DataOutUSB::DataOutUSB(){
    dataToHostQueue = (xQueueCreate(512, sizeof(struct DataOutUSB::DataOutContainer)));
    dataMutex = xSemaphoreCreateMutex();
}


DataOutUSB* DataOutUSB::getObject(){
    if (DataOutUSB::myObject == NULL) {
        DataOutUSB::myObject = new DataOutUSB();
    }

    return DataOutUSB::myObject;
}


void DataOutUSB::writeToHost(std::string charMessage){
    xSemaphoreTake(DataOutUSB::getObject()->dataMutex, portMAX_DELAY);

    struct DataOutContainer target;
    target.stdString = new std::string(charMessage);
    target.arrayLength = -1;
    
    QueueHandle_t queue = DataOutUSB::getObject()->dataToHostQueue;

    xQueueSend(queue, &target, 10);
    xSemaphoreGive(DataOutUSB::getObject()->dataMutex);
}

void DataOutUSB::publish(){
    xSemaphoreTake(DataOutUSB::getObject()->dataMutex, portMAX_DELAY);
    struct DataOutUSB::DataOutContainer out;

    if (xQueueReceive(dataToHostQueue, &out, 10)) {
        printf("%s", out.stdString->c_str());
        delete out.stdString;
    }
    xSemaphoreGive(DataOutUSB::getObject()->dataMutex);
}