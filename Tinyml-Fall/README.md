# TinyML Fall Detection System

A real-time fall detection system based on the QuecPython embedded platform, using the MPU6500 IMU sensor and random forest classifier.

## System Overview

This TinyML system applies machine learning directly on embedded hardware to detect movements in real time. It adopts a small sensor named MPU6500 to measure motion and rotation, and is currently optimized for X-axis and Y-axis movements.

## Features

- **Real-time Detection**: Response time for motion detection is 150-300ms
- **Memory Efficiency**: Automatic buffer management with overflow prevention
- **False Alarm Prevention**: 3 consecutive consistent results are required before detection
- **Timer-based Processing**: Non-blocking hardware timer architecture
- **Motion Segregation**: Each motion is analyzed independently to avoid mutual interference

## Directory Structure

```plaintext
tinyml-Fall/
├── src
	├── _main.py              # Main application based on the timer system
	├── mpu6500.py            # MPU6500 sensor driver with m/s² scaling
	├── random_forest.py      # Pre-trained random forest model
	├── tinyml.py             # TinyML pipeline with anti-shake mechanism
├── LICENSE
├── README.md
└── README_zh.md
```

## Technical Details

- **Platform**: Quectel embedded module running MicroPython
- **Sensor**: MPU6500 6-axis IMU (3-axis accelerometer + 3-axis gyroscope)
- **Model**: Random forest classifier (3 categories: 0 = Static, 1 = Walking, 2 = Fall type)
- **Sampling**: 50Hz sensor reading, 20Hz inference
- **Detection**: 3 consecutive consistent results within a 450ms window
- **Data Format**: Accelerometer (m/s²), Gyroscope (deg/s)

## Current Status

- **X/Y-axis Motion** - Reliable operation and stable detection
- **Memory Management** - Buffer contamination issue has been resolved
- **Real-time Processing** - Timer-based architecture has been implemented
- **Anti-shake System** - False alarm prevention function works properly
- **Circular Motion** - Currently under development

## Quick Start

### Prerequisites

Before you start, please ensure you have the following prerequisites:

- **Hardware**:
  - One QuecPython development board
  - A computer (Windows 7, Windows 10, or Windows 11)
  - MPU6500 sensor
- **Software**:
  - Debugging tool [QPYcom](https://developer.quectel.com/wp-content/uploads/2024/09/QPYcom_V3.9.0.zip)
  - QuecPython firmware (The EG912U firmware can be found in the `fw` directory of the repository)
  - Python text editor (e.g., [VSCode](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/download/))

### Installation

1. **Clone the repository**:

```plaintext
git clone https://github.com/aaronchenzhihe/Tinyml-Fall.git
```

   2.**Flash the firmware**: Flash the firmware to the development board according to the [instructions](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/flash_firmware.html).

### Run the Application

1. **Hardware Connection**: Correctly connect the MPU6500 sensor to the I2C interface of the development board.
2. **Connect to the host computer via Type-C cable**.
3. Download the code to the device:
   - Launch the QPYcom debugging tool.
   - Connect the data cable to the computer.
   - Press the **PWRKEY** button on the development board to power it on.
   - Import all files in the `src` folder into the module's file system while maintaining the directory structure, following the [instructions](https://developer.quectel.com/doc/quecpython/Getting_started/en/4G/first_python.html).
4. Run the code
   - Select the `File` tab.
   - Select the `_main.py` script.
   - Right-click and select `Run` to execute the script.

## Usage

The system automatically detects motions in real time. When a motion is recognized, it outputs the classification result (0, 1, or 2) and clears all buffers to prevent interference from previous motions.

## Performance

- **Detection Latency**: Theoretical minimum of 150ms, actual 200-300ms
- **Memory Usage**: Total < 50KB
- **Accuracy**: Optimized for X/Y-axis movements