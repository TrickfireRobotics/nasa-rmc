#include "../include/dataInUSB.hpp"
#include "../include/dataOutUSB.hpp"

#define MAX_INPUT_BUFFER 200

DataInUSB::DataInUSB(){

}

void DataInUSB::printUSBMessageInt(char* msg){
    for (int index = 0; index < MAX_INPUT_BUFFER; index++){
        //std::string* str = new std::string( "[" + std::to_string(index) + "] = " + "(" + std::to_string((int)msg[index]) + ")" + msg[index] + "\n");
        //DataOutUSB::getObject()->writeToHost(str);
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

    //DataOutUSB::getObject()->writeToHost("what am i doing");


    MessageInContainer* messageCOntainer;

    if (commandID == "stepper") {
        //std::string* str = new std::string("stepper message\n");
        DataOutUSB::getObject()->writeToHost("stepper message\n");
    }
    else if (commandID == "pwm"){
        //std::string* str = new std::string("pwm message\n");
        DataOutUSB::getObject()->writeToHost("pwm message\n");
    }
    else if(commandID == "light"){
        //std::string* str = new std::string("light message\n");
        DataOutUSB::getObject()->writeToHost("light message\n");
    }
    else if(commandID == "config"){
        //std::string* str = new std::string("config message\n");
        DataOutUSB::getObject()->writeToHost("config message\n");
    }
    else {
        //std::string* str = new std::string("unkown message\n");
        DataOutUSB::getObject()->writeToHost("unkown message\n");
    }

    //printf("%s\n", inputBuffer);
    printf("----\n\n");

    return NULL;

}





