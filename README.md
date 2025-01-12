# 🚀 Stepper Motor Driver

*(Note: These instructions and the build process are designed to work only on a Raspberry Pi.)*

## 📝 Introduction
This project provides a robust software interface for controlling any **4-wire bidirectional stepper motor** commonly used in industrial applications. The package allows users to issue commands over a network or serial interface using the **NDSP (Network Distributed Step Protocol)** server. By combining the power of Python, GPIO control, and the `sipyco_rpctool` command-line tool, this system enables precise and flexible stepper motor control for robotics, automation systems, and research applications.

---

## 🎥 Demo Video
[![Stepper Motor Control Demo](https://img.youtube.com/vi/3hwh1JNyjAE/0.jpg)](https://youtu.be/3hwh1JNyjAE)

Click the image to view the demo.

---

## 📖 Overview
The software package enables stepper motor control via both local and remote commands:
- **Local control:** Using Python scripts to control motor movement.
- **Remote control:** Interacting with the motor over a network using RPC (Remote Procedure Call) commands via the `sipyco_rpctool`.

With this package, you can:
- Control any 4-wire stepper motor in the industry.
- Perform microstepping for smoother and precise movement.
- Issue absolute and relative movement commands.
- Save and load custom positions for repeatable actions.
- Move to a defined "home" position.

---

## ⚙️ Prerequisites
- Python 3.7+ (ensure `python3` is available on your system)
- [Poetry](https://python-poetry.org/docs/#installation) installed (for dependency management)

---

## 🔧 Setup Instructions

### 1️⃣ Create and Activate a Virtual Environment
It’s a best practice to work inside a virtual environment to isolate the project’s dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies via Poetry

With the virtual environment activated:
```bash
poetry install
```
This command will install all dependencies specified in `pyproject.toml` and `poetry.lock`. If you make changes or add new dependencies, run:

```bash
poetry update
```

---

## ▶️ Usage Instructions

To activate the NDSP server through which the stepper motor can be interacted with, use:
```bash
python3 -m src.aqctl_stepper_motor
```

---

## 🌐 SiPyCo Usage

To call stepper motor commands by sending RPC commands to the NDSP server:
```bash
# List available targets (if unsure)
sipyco_rpctool <host> <port> list-targets 

# List available methods for a specific target (e.g., "motor_controller")
sipyco_rpctool <host> <port> list-methods

# Call a specific method (e.g., "step_motor" with 100 steps)
sipyco_rpctool <host> <port> call step_motor 100

# Call a method with arguments (e.g., "move_to_absolute" with position 5000 and delay 0.01)
sipyco_rpctool <host> <port> call move_to_absolute 5000 0.01
```

**Explanation:**

* `<host>`: Replace with the hostname or IP address of the machine running the NDSP server.
* `<port>`: Replace with the port number that the NDSP server is listening on.

This format provides a clear and concise way to use `sipyco_rpctool` to interact with the stepper motor controller via the NDSP server.

## 🛠️ API Reference

The `StepperMotorControl` class provides methods to control a stepper motor connected to a Raspberry Pi’s GPIO pins. It manages the motor’s current position, supports microstepping configurations, and allows saving/retrieving custom positions.

---

## ⚙️ Motor Control API

### 📜 Methods

#### 🔄 `load_positions()`
Loads the current position, home position, and saved positions from the data file (if it exists).

#### 💾 `save_positions()`
Saves the current position, home position, and all saved positions to the data file.

#### 🏁 `set_position_zero()`
Sets the current position to zero and updates the data file.

#### ⚙️ `set_microstepping(mode)`
Configures the microstepping mode for the stepper driver.

**Parameters:**
* `mode` (int): The microstepping mode index defined in `MICROSTEPPING_MODES`.

#### ➡️ `step_motor(steps, delay=0.02)`
Performs the specified number of step pulses. Updates the current position accordingly and saves positions to file.

**Parameters:**
* `steps` (int): Number of steps to move the motor. Positive values move in one direction; negative values in the opposite.
* `delay` (float, optional): Delay between step pulses in seconds. Defaults to 0.02.

#### 🧭 `move_to_absolute(target_position, delay=0.02)`
Moves the motor to a specified absolute position, calculating how many steps are needed from the current position.

**Parameters:**
* `target_position` (int): The absolute position in steps to move the motor to.
* `delay` (float, optional): Delay between step pulses. Defaults to 0.02.

#### 🔄 `move_relative(step_offset, delay=0.02)`
Moves the motor relative to its current position.

**Parameters:**
* `step_offset` (int): Number of steps to move relative to the current position (positive or negative).
* `delay` (float, optional): Delay between steps. Defaults to 0.02.

#### 🏠 `set_home()`
Sets the current position as the home position and saves it to the data file.

#### 🏠 `go_to_home(delay=0.02)`
Moves the motor to the previously defined home position.

**Parameters:**
* `delay` (float, optional): Delay between steps. Defaults to 0.02.

#### 📍 `get_current_position()`
Retrieves the motor's current position from memory.

**Returns:**
* `int`: The current absolute position in steps.

#### 💾 `save_position(name)`
Saves the current position under a custom name for future retrieval.

**Parameters:**
* `name` (str): A unique name under which to save the current position.

#### 📌 `go_to_saved_position(name, delay=0.02)`
Moves the motor to a position that was previously saved using `save_position()`.

**Parameters:**
* `name` (str): The name of the saved position to move to.
* `delay` (float, optional): Delay between steps. Defaults to 0.02.

#### 🧹 `cleanup()`
Cleans up GPIO resources and saves the current state before exiting. This should be called upon completion of motor operations to ensure a safe shutdown.

---

