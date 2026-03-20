# TinyML Gesture Recognition System

A real-time gesture recognition system using MPU6500 IMU sensor and Random Forest classifier on Quectel embedded platform.

## System Overview

This TinyML system detects hand movements in real-time using machine learning directly on embedded hardware. The system uses a small sensor called MPU6500 that measures movement and rotation, currently optimized for X and Y axis movements.

## Features

- **Real-time Detection**: 150-300ms response time for gesture recognition
- **Memory Efficient**: Automatic buffer management with overflow prevention
- **False Positive Prevention**: Requires 3 consecutive results before detection
- **Timer-based Processing**: Non-blocking hardware timer architecture
- **Gesture Separation**: Each gesture analyzed independently without contamination

## Directory Structure

```plaintext
tinyml_qpy/
├── _main.py              # Main application with Timer-based system
├── mpu6500.py            # MPU6500 sensor driver with m/s² scaling
├── random_forest.py      # Pre-trained Random Forest model
├── tinyml.py             # TinyML pipeline with debounce mechanism
├── data_collect.py       # Data collection utility
└── README.md
```

## Technical Details

- **Platform**: Quectel embedded module running MicroPython
- **Sensor**: MPU6500 6-axis IMU (3-axis accelerometer + 3-axis gyroscope)
- **Model**: Random Forest classifier (4 classes: 0=no gesture, 1-3=gesture types)
- **Sampling**: 50Hz sensor reading, 20Hz inference
- **Detection**: 3 consecutive results within 450ms window
- **Data Format**: Accelerometer (m/s²), Gyroscope (deg/s)

## Current Status

- **X/Y axis movements** - Working reliably with stable detection
- **Memory management** - Buffer contamination issues resolved
- **Real-time processing** - Timer-based architecture implemented
- **Debounce system** - False positive prevention working
- **Circular movements** - Currently under development

## Usage

The system automatically detects gestures in real-time. When a gesture is recognized, it outputs the classification result (1, 2, or 3) and clears all buffers to prevent contamination from previous gestures.

## Performance

- **Detection Latency**: 150ms theoretical minimum, 200-300ms practical
- **Memory Usage**: <50KB total
- **Accuracy**: Optimized for X/Y axis movements

## References

- [TinyML: Machine Learning on ESP32 with MicroPython](https://dev.to/tkeyo/tinyml-machine-learning-on-esp32-with-micropython-38a6)
- [tinyml-esp GitHub Repository](https://github.com/tkeyo/tinyml-esp)