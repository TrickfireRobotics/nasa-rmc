import asyncio
import asyncio
import threading

import moteus
from rclpy.node import Node

from utility.color_text import ColorCodes

from . import moteus_motor


class MoteusThreadManager:
    CONNECTION_TIMEOUT_IN_SECONDS = 0.1
    GENERAL_TIMEOUT = 0.05

    """
    This creates a new thread called "moteus_thread" to run all
    of the asyncio methods required by the Moteus library
    This creates a new thread called "moteus_thread" to run all
    of the asyncio methods required by the Moteus library
    """

    def __init__(self, ros_node: Node):
        self._name_to_moteus_motor: dict[str, moteus_motor.MoteusMotor] = {}
        self._name_to_moteus_controller: dict[str, moteus.Controller] = {}  # Used by the thread
        self._ros_node = ros_node
        self._moteus_thread: threading.Thread | None = None
        self._should_moteus_thread_loop = True  # No thread safety, but it works lololol
        self._should_reconnect = True  # No thread safety, but it works lololol

    def addMotor(self, can_id: int, motor_name: str) -> None:
        """
        Adds a motor to the list to attempt to connect to
        """
        # Create motor
        motor = moteus_motor.MoteusMotor(can_id, motor_name, self._ros_node)
        self._name_to_moteus_motor[motor_name] = motor

    def start(self) -> None:
    def start(self) -> None:
        """
        Starts a new thread. New motors cannot be added after this is called
        Starts a new thread. New motors cannot be added after this is called
        """

        self._moteus_thread = threading.Thread(
            target=self.threadEntry, name="moteus_thread", daemon=True
        )
        self._moteus_thread.start()

    def reconnectMotors(self) -> None:
        self._should_reconnect = True

        self._moteus_thread = threading.Thread(
            target=self.threadEntry, name="moteus_thread", daemon=True
        )
        self._moteus_thread.start()

    def reconnectMotors(self) -> None:
        self._should_reconnect = True

    def terminateAllThreads(self) -> None:
    def terminateAllThreads(self) -> None:
        """
        Gracefully shuts down the motors by calling set_stop().
        Terminates the thread.
        Does not clean up this class
        Gracefully shuts down the motors by calling set_stop().
        Terminates the thread.
        Does not clean up this class
        """
        self._should_moteus_thread_loop = False
        if self._moteus_thread is not None:
            self._moteus_thread.join()

    def threadEntry(self) -> None:
        self._should_moteus_thread_loop = False
        if self._moteus_thread is not None:
            self._moteus_thread.join()

    def threadEntry(self) -> None:
        """
        The entry of the thread that launches the asyncio loop
        The entry of the thread that launches the asyncio loop
        """
        self._ros_node.get_logger().info(
            ColorCodes.BLUE_OK + "Moteus Thread Launched" + ColorCodes.ENDC
        )
        asyncio.run(self.startLoop())

    async def tryToShutdownMotor(self, motor_name: str) -> None:
        self._ros_node.get_logger().info(
            ColorCodes.WARNING_YELLOW
            + f'Unexpectedly trying to turn off motor "{motor_name}" (CANID '
            + str(self._name_to_moteus_motor[motor_name].canID)
            + ")"
            + ColorCodes.ENDC
        )

        try:
            await asyncio.wait_for(
                self._name_to_moteus_controller[motor_name].set_stop(),
                timeout=self.GENERAL_TIMEOUT,
            )
            self._ros_node.get_logger().info(
                ColorCodes.GREEN_OK
                + f'Stopped motor "{motor_name}" (CANID '
                + str(self._name_to_moteus_motor[motor_name].can_id)
                + ")"
                + ColorCodes.ENDC
            )
        except asyncio.TimeoutError:
            self._ros_node.get_logger().info(
                ColorCodes.FAIL_RED
                + f'FAILED TO "set_stop" MOTOR. TIMED OUT "{motor_name}" (CANID '
                + str(self._name_to_moteus_motor[motor_name].can_id)
                + ")"
                + ColorCodes.ENDC
            )
            del self._name_to_moteus_controller[motor_name]
            del self._name_to_moteus_motor[motor_name]
        except RuntimeError as error:
            self._ros_node.get_logger().info(ColorCodes.FAIL_RED + str(error) + ColorCodes.ENDC)
            del self._name_to_moteus_controller[motor_name]
            del self._name_to_moteus_motor[motor_name]

    async def startLoop(self) -> None:
    async def startLoop(self) -> None:
        """
        The main loop of the whole system.
        Reads/sends data to/from the Moteus controllers.

        This can handle the following edge cases
        ----------
        1) Motor faults
            A) set_stop() the motor or
            B) Remove the motor from the list of motors
        2) CAN Bus disconnection
            A) Remove the motor from the list of motors
        3) Reconnect to Moteus Controllers


        The main loop of the whole system.
        Reads/sends data to/from the Moteus controllers.

        This can handle the following edge cases
        ----------
        1) Motor faults
            A) set_stop() the motor or
            B) Remove the motor from the list of motors
        2) CAN Bus disconnection
            A) Remove the motor from the list of motors
        3) Reconnect to Moteus Controllers


        """
        # Connect the motor for the first time
        await self.connectToMoteusControllers()

        while self._should_moteus_thread_loop:
            if self._should_reconnect:
        while self._should_moteus_thread_loop:
            if self._should_reconnect:
                await self.connectToMoteusControllers()


            # Go through each Moteus Controller to send data
            for name, controller in self._name_to_moteus_controller.copy().items():
                motor = self._name_to_moteus_motor[name]

                try:
                    # Check for faults
                    result_from_moteus = await asyncio.wait_for(
                        controller.query(), self.GENERAL_TIMEOUT
                    )

                    if result_from_moteus.values[moteus.Register.FAULT] != 0:
                        self._ros_node.get_logger().info(
                            ColorCodes.FAIL_RED
                            + f"FAULT CODE: {result_from_moteus.values[moteus.Register.FAULT]} FOR "
                            + f'"{name}" (CANID {motor.can_id})'
                            + ColorCodes.ENDC
                        )
                        await self.tryToShutdownMotor(name)
                        continue

                    if motor.setStop is True:
                        await asyncio.wait_for(controller.set_stop(), self.GENERAL_TIMEOUT)

                    else:
                        result_from_moteus = await asyncio.wait_for(
                            controller.set_position(
                                position=motor.position,
                                velocity=motor.velocity,
                                feedforward_torque=motor.feedforward_torque,
                                kp_scale=motor.kp_scale,
                                kd_scale=motor.kd_scale,
                                maximum_torque=motor.max_torque,
                                watchdog_timeout=motor.watchdog_timeout,
                                velocity_limit=motor.velocity_limit,
                                accel_limit=motor.accel_limit,
                                fixed_voltage_override=motor.fixed_voltage_override,
                                query=True,
                            ),
                            self.GENERAL_TIMEOUT,
                        )

                    motor.publishData(result_from_moteus)

                except asyncio.TimeoutError:
                    self._ros_node.get_logger().info(
                        ColorCodes.FAIL_RED
                        + f'FAILED TO SEND/READ DATA TO MOTEUS MOTOR: "{name}" {motor.can_id}) '
                        + "CAN-FD bus disconnected?"
                        + ColorCodes.ENDC
                    )
                    del self._name_to_moteus_controller[name]
                    del self._name_to_moteus_motor[name]

            await asyncio.sleep(0.02)


        # When we exit the while loop, via ctrl-c, we set_stop() all the motors
        # Watch out for the arm
        for name, controller in self._name_to_moteus_controller.items():
            await controller.set_stop()

    async def connectToMoteusControllers(self) -> None:

    async def connectToMoteusControllers(self) -> None:
        """
        Connect to the Moteus motors.
        There is a timeout until we give up trying to connect
        Connect to the Moteus motors.
        There is a timeout until we give up trying to connect
        """
        self._name_to_moteus_controller = {}
        self._should_reconnect = False

        for key, motor in self._name_to_moteus_motor.items():
            qr = moteus.QueryResolution()
            qr.power = moteus.F32
            qr.q_current = moteus.F32
            qr.d_current = moteus.F32
            controller = moteus.Controller(motor.can_id, query_resolution=qr)

            try:
                # Reset the controller
                self._ros_node.get_logger().info(
                    "Connecting to motor with name: " + str(motor.name)
                )
                await asyncio.wait_for(
                    controller.query(), timeout=self.CONNECTION_TIMEOUT_IN_SECONDS
                )  # Try to get data, if timeout then cannot connect
                self._name_to_moteus_controller[key] = controller
                await controller.set_stop()
                self._ros_node.get_logger().info(
                    ColorCodes.GREEN_OK
                    + f'Moteus motor controller connected: "{motor.name}" (CANID {motor.can_id})'
                    + ColorCodes.ENDC
                )

            except asyncio.TimeoutError:
                self._ros_node.get_logger().info(
                    ColorCodes.FAIL_RED
                    + "FAILED TO CONNECT TO MOTEUS CONTROLLER WITH CANID "
                    + str(motor.can_id)
                    + ColorCodes.ENDC
                )
            except RuntimeError as error:
                self._ros_node.get_logger().info(
                    ColorCodes.FAIL_RED
                    + "ERROR WHEN set_stop() IS CALLED. MOST LIKELY CANNOT FIND CANBUS"
                    + ColorCodes.ENDC
                )
                self._ros_node.get_logger().info(
                    ColorCodes.FAIL_RED + str(error.with_traceback(None)) + ColorCodes.ENDC
                )
