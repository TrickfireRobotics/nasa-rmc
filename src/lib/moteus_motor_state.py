"""
This module contains objects representing the moteus motor state and settings for `set_position`.
"""

from dataclasses import dataclass
from typing import Any

import moteus

from lib.json_msg import JsonMsg


@dataclass(frozen=True)
class MoteusMotorState(JsonMsg["MoteusMotorState"]):
    """
    A dataclass representing the state of the moteus motor.
    """

    can_id = -1
    position: float | None = None
    velocity: float | None = None
    torque: float | None = None
    temperature: float | None = None
    power: float | None = None
    input_voltage: float | None = None
    q_current: float | None = None
    d_current: float | None = None

    @classmethod
    def fromMoteusData(cls, moteus_result: Any) -> "MoteusMotorState":
        """
        Creates a MoteusMotorState from a moteus result.
        """
        dict_ = {
            "position": moteus_result.values[moteus.Register.POSITION],
            "velocity": moteus_result.values[moteus.Register.VELOCITY],
            "torque": moteus_result.values[moteus.Register.TORQUE],
            "temperature": moteus_result.values[moteus.Register.TEMPERATURE],
            "power": moteus_result.values[moteus.Register.POWER],
            "input_voltage": moteus_result.values[moteus.Register.VOLTAGE],
            "q_current": moteus_result.values[moteus.Register.Q_CURRENT],
            "d_current": moteus_result.values[moteus.Register.D_CURRENT],
        }

        return cls(**dict_)


@dataclass(frozen=True)
class MoteusRunSettings(JsonMsg["MoteusRunSettings"]):
    """
    A dataclass representing the different settings while running a moteus motor.
    """

    position: float | None = None
    velocity: float | None = None
    feedforward_torque: float | None = None
    kp_scale: float | None = None
    kd_scale: float | None = None
    max_torque: float | None = None
    watchdog_timeout: float | None = None
    velocity_limit: float | None = None
    accel_limit: float | None = None
    fixed_voltage_override: float | None = None
    set_stop: bool = False
