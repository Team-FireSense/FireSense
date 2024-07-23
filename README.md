# FireSense

FireSense is an advanced fire detection system leveraging the power of computer vision and artificial intelligence to detect fires in real-time. This project aims to enhance safety and early fire detection in various environments, potentially saving lives and reducing property damage.

## Table of Contents

- [Introduction](#introduction)
- [Goal of the Project](#goal-of-the-project)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Team Organization](#team-organization)
- [Milestones](#milestones)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

Wildfires have taken the forefront of environmental-related issues as increased incidences have occurred, such as the Australian bushfires and Amazon rainforest fires. In order to detect these fires before they spread out of control, drones can be implemented due to their capabilities to be remotely and safely controlled while also having cameras and sensors. 

## Goal of the Project

At the core, the project aims to act as an early warning system for authorities to be able to react promptly to wildfire threats. To achieve this, our group is creating a scalable drone system that can effectively detect the location and size of a fire.

## Features

- Real-time fire detection using computer vision.
- Scalable system for single or multiple drones.

## Installation

### Software Requirements

- Ubuntu 20.04.2.0 LTS (dual boot or VM setup)
- Python 3.8
- Gazebo
- PX4 and MAVSDK
- TensorFlow (install via `pip3 install TensorFlow`)

### Hardware Requirements

- Computer running Ubuntu (preferably natively or on a dual boot, but a VM like VMware should also work)
- The computer should meet the minimum spec requirements for Gazebo

### Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/Team-FireSense/FireSense.git
   cd FireSense
   ```

2. Set up Gazebo and PX4:
   ```sh
   sudo apt install gazebo11 libgazebo11-dev
   git clone https://github.com/PX4/PX4-Autopilot.git --recursive
   cd PX4-Autopilot
   DONT_RUN=1 make px4_sitl_default gazebo
   ```

3. Set the position of the drone:
   ```sh
   export PX4_HOME_LAT=0
   export PX4_HOME_LON=0
   export PX4_HOME_ALT=0
   ```

4. Start the simulation:
   ```sh
   make px4_sitl gazebo___firesense8
   ```

## Usage

1. Open two terminals.
2. In the first terminal, navigate to the project directory and start the main script:
   ```sh
   cd FireSense
   python3 main.py
   ```
3. In the second terminal, monitor the output of the drone as it functions, which will indicate if it detects a fire.

## Technologies Used

- **Computer Vision**: High-accuracy and confidence fire detection using neural networks.
- **Gazebo**: Simulation environment.
- **PX4**: Drone control software.

## Team Organization

- **Ashok Sathiyamoorthy**: Swarm Algorithms, Python Implementation, Gazebo Simulation, Robotics (Drone)
- **Akash Savitala**: Concept Generation, Python Implementation (Cohort Intelligence)
- **Pavan Kumar**: Software, Robotics, Concept Generation
- **Thomas Deng**: CV, Swarm, Control, Simulation, Collision Avoidance
- **Hardiv Harshakumar**: Computer Vision, Sensor Fusion, Swarming, Neural Networks

## Milestones

- Formulate project idea - July 10 (Completed)
- Preliminary research - July 18
- Set up simulation - July 18
- Design drone “hardware” in ROS - Jul 21
- Implement Sensors - Jul 23
- Implement Control - Jul 25
- Implement Computer Vision algorithm - Jul 28
- Achieve successful completion of fire detection task (Project FireSense) - August 3
- Finish Final Project Presentation (End of Class) - August 5

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank our mentors and the open-source community for their support and resources that made this project possible.
