# message.py

import RPi.GPIO as GPIO

MICROSTEPPING_MODES = {
    0: (GPIO.LOW, GPIO.LOW, GPIO.LOW),  # Full Step
    1: (GPIO.HIGH, GPIO.LOW, GPIO.LOW), # Half Step
    2: (GPIO.LOW, GPIO.HIGH, GPIO.LOW), # Quarter Step
    3: (GPIO.HIGH, GPIO.HIGH, GPIO.LOW), # Eighth Step
    4: (GPIO.LOW, GPIO.LOW, GPIO.HIGH), # Sixteenth Step
    5: (GPIO.HIGH, GPIO.HIGH, GPIO.HIGH) # Thirty-Second Step
}
