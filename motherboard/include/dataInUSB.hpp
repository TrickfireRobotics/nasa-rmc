#ifndef DATA_IN_USB_HPP
#define DATA_IN_USB_HPP

#include <string>

class DataInUSB{

enum MessageType {STEPPER = 0, PWM = 1, LIGHT = 2, CONFIG = 3};


struct MessageInContainer{
    void* message;
    MessageType messageType;
};

struct StepperMessage{
    int targetBoard; // 0,1,2,3,4,5
    double targetPosition; // in revolutions
    double targetVelocity; // in revolutions per sec
    int ms3;
    int ms2;
    int ms1;
    bool enable;
    int reset;
};

struct PWMMessage{
    int targetPort; // 0,1,2,3,4,5
    double targetDuty; // [0.0,1.0]
    double targetFrequency; //
};

struct LightMessage{
    int targetColor; // "r,g,b"
    bool targetState; // 1 -> ON 0 -> OFF
};

struct ConfigMessage{


};


private:

    void printUSBMessageInt(char* msg);

public:
    DataInUSB();

    MessageInContainer* readNextUSBMessage();

    

    

};


#endif 