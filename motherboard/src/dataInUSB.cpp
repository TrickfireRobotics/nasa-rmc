#include "../include/dataInUSB.hpp"

#define MAX_INPUT_BUFFER 200

DataInUSB::DataInUSB(){

}

void DataInUSB::printUSBMessageInt(char* msg){
    for (int index = 0; index < MAX_INPUT_BUFFER; index++){
        printf("[%d] = (%d)%c\n", index, (int)msg[index], msg[index]);
    }
}


 DataInUSB::MessageInContainer* DataInUSB::readNextUSBMessage(){
    char inputBuffer[MAX_INPUT_BUFFER];

    fgets(inputBuffer, sizeof(inputBuffer), stdin);

    std::string stringMessage(inputBuffer);

    //printUSBMessageInt(inputBuffer);

    int indexOfFirstSpace = stringMessage.find_first_of(" ");
    int indexOfCarriageFeed = stringMessage.find_first_of((char)13);

    if (indexOfCarriageFeed == -1) {
        indexOfCarriageFeed = 0;
    }
    else {
        indexOfCarriageFeed++;   
    }

    std::string commandID = stringMessage.substr(indexOfCarriageFeed, indexOfFirstSpace - indexOfCarriageFeed);
    printf("subtr[%d]: %s\n", commandID.size(), commandID.c_str());


    MessageInContainer* messageCOntainer;

    if (commandID == "stepper") {
        printf("stepper message\n");
    }
    else if (commandID == "pwm"){
        printf("pwm message\n");
    }
    else if(commandID == "light"){
        printf("light message\n");
    }
    else if(commandID == "config"){
        printf("config message\n");
    }
    else {
        printf("Unknown message\n");
    }

    //printf("%s\n", inputBuffer);
    printf("----\n\n");

    return NULL;

}





