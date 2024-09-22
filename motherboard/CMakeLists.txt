# As it says, require a minimum value of cmake
cmake_minimum_required(VERSION 3.12)

# Set some variables for C and CPP
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

include (FreeRTOS-Kernel/portable/ThirdParty/GCC/RP2040/pico_sdk_import.cmake)
include (FreeRTOS-Kernel/portable/ThirdParty/GCC/RP2040/FreeRTOS_Kernel_import.cmake)

# Include the pico-sdk stuff
include("../pico-sdk/external/pico_sdk_import.cmake")

# Create the project called "pico_motherboard"
project(pico_motherboard C CXX ASM)

add_compile_definitions(DEBUG)

pico_sdk_init()

add_executable(${PROJECT_NAME}
    ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/dataInUSB.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/dataOutUSB.cpp
)

target_include_directories(${PROJECT_NAME} PRIVATE 
        include
)

# create map/bin/hex/uf2 files.
pico_add_extra_outputs(${PROJECT_NAME})
pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 0)

# Pull in our pico_stdlib which pulls in commonly used features (gpio, timer-delay etc)
target_link_libraries(${PROJECT_NAME}
    pico_stdlib 
    FreeRTOS-Kernel 
    FreeRTOS-Kernel-Heap4 
    #tinyusb_device
)


