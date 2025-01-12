import asyncio
import os
from dotenv import load_dotenv
from sipyco.pc_rpc import simple_server_loop

from .driver.stepper_motor import StepperMotorControl

def main():
    load_dotenv()
    motor = StepperMotorControl(step_pin=int(os.getenv("STEP_PIN")), 
                                dir_pin=int(os.getenv("DIRECTION_PIN")), 
                                ms1=int(os.getenv("MICROSTEPPING_PIN_0")), 
                                ms2=int(os.getenv("MICROSTEPPING_PIN_1")),
                                ms3=int(os.getenv("MICROSTEPPING_PIN_2")))
    try:
        simple_server_loop({
            "motor": motor
        }, "0.0.0.0", 4000)
    except KeyboardInterrupt:
        motor.cleanup()


if __name__ == "__main__":
    main()