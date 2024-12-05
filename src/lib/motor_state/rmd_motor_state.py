"""
This module contains objects representing the RMD-X8 motor state and settings for `set_position`.
"""

from dataclasses import dataclass

from myactuator_rmd_py.actuator_state import MotorStatus1, MotorStatus2

from lib.json_msg import JsonMsg
from lib.motor_state.can_motor_state import CanMotorRunSettings, CANMotorState

DEGS_TO_REVS = 1 / 360


@dataclass(frozen=True, kw_only=True)
class RMDX8MotorState(CANMotorState, JsonMsg["RMDX8MotorState"]):
    """
    A dataclass representing the state of the RMD-X8 motor.
    """

    acceleration: float | None = None
    error_code: int | None = None
    """
    Current error code reported by the motor.
    """

    @classmethod
    def fromRMDX8Data(
        cls,
        can_id: int,
        motor_status_1: MotorStatus1,
        motor_status_2: MotorStatus2,
        power: float,
        acceleration: float,
    ) -> "RMDX8MotorState":
        """
        Creates an RMDX8MotorState from the RMD-X8 data response.
        """
        return cls(
            can_id=can_id,
            position=motor_status_2.shaft_angle * DEGS_TO_REVS,
            velocity=motor_status_2.shaft_speed * DEGS_TO_REVS,
            current=motor_status_2.current,
            temperature=motor_status_1.temperature,
            power=power,
            input_voltage=motor_status_1.voltage,
            acceleration=acceleration,
            error_code=motor_status_1.error_code.value,
        )


@dataclass(frozen=True, kw_only=True)
class RMDX8RunSettings(CanMotorRunSettings, JsonMsg["RMDX8RunSettings"]):
    """
    A dataclass representing the different settings while running an RMD-X8 motor.
    """
