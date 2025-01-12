#!/usr/bin/env python3

from sipyco.pc_rpc import simple_server_loop
from .message import MICROSTEPPING_MODES
import RPi.GPIO as GPIO
from time import sleep
import json
import os

class StepperMotorControl:
    def __init__(self, step_pin, dir_pin, ms1, ms2, ms3, data_file="motor_position.json"):
        # Pin Definitions
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.ms1 = ms1
        self.ms2 = ms2
        self.ms3 = ms3
        self.data_file = data_file  # File to store the position data

        self.current_position = 0  # Always indicates absolute position
        self.home_position = 0
        self.saved_positions = {}  # Dictionary to store saved positions with custom names
        self.load_positions()

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.ms1, GPIO.OUT)
        GPIO.setup(self.ms2, GPIO.OUT)
        GPIO.setup(self.ms3, GPIO.OUT)
        GPIO.output(self.step_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)

    def load_positions(self):
        """Load the saved positions from a file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.current_position = data.get("current_position", 0)
                self.home_position = data.get("home_position", 0)
                self.saved_positions = data.get("saved_positions", {})

    def save_positions(self):
        """Save the current, home, and saved positions to a file."""
        data = {
            "current_position": self.current_position,
            "home_position": self.home_position,
            "saved_positions": self.saved_positions
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)
        print("Saved positions:", data)  # Debug print to confirm write

    def set_position_zero(self):
        """Set the current position to zero."""
        self.current_position = 0
        self.save_positions()
        print("Current position has been set to zero.")

    def set_microstepping(self, mode):
        """
        Set the microstepping mode.
        :param mode: Microstepping mode (0 to 5 for full step to thirty-second step)
        """
        if mode in MICROSTEPPING_MODES:
            GPIO.output(self.ms1, MICROSTEPPING_MODES[mode][0])
            GPIO.output(self.ms2, MICROSTEPPING_MODES[mode][1])
            GPIO.output(self.ms3, MICROSTEPPING_MODES[mode][2])
            print(f"Microstepping mode set to {mode}")
        else:
            print(f"Invalid microstepping mode: {mode}")

    def step_motor(self, steps: int, delay: float = 0.02):
        """
        Control the stepper motor.
        :param steps: Number of steps to move the motor (positive for one direction, negative for the opposite)
        :param delay: Delay between each step pulse (seconds)
        """
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        GPIO.output(self.dir_pin, direction)

        for _ in range(abs(steps)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)

        # Update position based on direction
        self.current_position += steps  # Add negative or positive value
        self.save_positions()

    def move_to_absolute(self, target_position, delay=0.02):
        """
        Move the motor to an absolute position.
        :param target_position: The target absolute position in steps
        :param delay: Delay between each step pulse (seconds)
        """
        steps_to_move = target_position - self.current_position
        self.step_motor(steps_to_move, delay)

    def move_relative(self, step_offset, delay=0.02):
        """
        Move the motor by a relative offset from the current position.
        :param step_offset: Number of steps to move relative to current position (positive or negative)
        :param delay: Delay between each step pulse (seconds)
        """
        self.step_motor(step_offset, delay)

    def set_home(self):
        """
        Set the current position as the home position.
        """
        self.home_position = self.current_position
        self.save_positions()  
        print(f"Home position set at {self.home_position} steps.")

    def go_to_home(self, delay=0.02):
        """
        Move the motor to the home position.
        :param delay: Delay between each step pulse (seconds)
        """
        if self.home_position != self.current_position:
            self.move_to_absolute(self.home_position, delay)
            print(f"Moved to home position at {self.home_position} steps.")
        else:
            print(f"Already at the home position ({self.home_position} steps).")

    def get_current_position(self):
        """
        Retrieve the current position of the stepper motor.
        :return: The current position in steps.
        """
        print(f"Current position: {self.current_position} steps")
        return self.current_position

    def save_position(self, name):
        """
        Save the current position with a custom name.
        :param name: The name to associate with the current position
        """
        if not isinstance(name, str):
            name = str(name)
    
        self.saved_positions[name] = self.current_position
        self.save_positions()  # Save the named position
        print(f"Position '{name}' saved at {self.current_position} steps.")

    def go_to_saved_position(self, name, delay=0.02):
        """
        Move the motor to a previously saved position by name.
        :param name: The name of the saved position to move to
        :param delay: Delay between each step pulse (seconds)
        """
        if name in self.saved_positions:
            target_position = self.saved_positions[name]
            steps_to_move = target_position - self.current_position
            direction = 1 if steps_to_move > 0 else 0
            self.step_motor(abs(steps_to_move), delay)
            print(f"Moved to saved position '{name}' at {target_position} steps.")
        else:
            print(f"Error: Saved position '{name}' not found.")

    def cleanup(self):
        GPIO.cleanup()
        self.save_positions() 
        print("GPIO cleanup completed.")
