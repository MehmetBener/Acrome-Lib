**Category:** SMD Applications → Interactive

# **Morse Code Transmitter**

The Morse Code Transmitter turns the basic “blinking light” demonstration into a polished desktop app that transmits Morse code. Using an RGB LED module and a Buzzer module driven by an SMD Red, the project converts any text you type into audible \+ visual Morse code. A simple Tkinter GUI lets you enter the text, follow progress on a bar, and see the exact “dot-dash” string before you send it.

**About Tools and Materials:**

SMD Red

SMD USB Gateway

Arduino Gateway Module

RGB LED Module

Buzzer Module

# **Step 1: Hardware and Software Overview**

1. SMD

The SMD acts as a bridge between the script and the modules. It is responsible for interpreting the commands the script sends and translating them into actions that actuate the [RGB LED Module](https://docs.acrome.net/electronics/add-on-modules/rgb-led-module) and the [Buzzer Module](https://docs.acrome.net/electronics/add-on-modules/buzzer-module).

2. RGB LED Module

Flashes white light for each dot or dash so you can “see” the code in real time. Long flashes for dashes and short flashes for dots.

3. Buzzer Module

Generating short and long beeps that match the LED flashes adds an audible feedback to the user.

4. SMD Libraries

The official Acrome SMD Python library handles low-level serial communication, device scanning, and module control, letting you focus on the Morse logic and GUI.

## **Project Key Features**

* **Visual \+ Audible Morse Output**

Every symbol is simultaneously flashed and beeped for clear feedback.

* **Real-time Progress Indicator**

A GUI progress bar moves from 0 % to 100 % as the message transmits.

* **Dot-dash Visualization**

The dots and dashes get visualized in the Tkinter UI. 

* **Adjustable Timing**

Modify the DOT\_DURATION constant to speed up or slow down transmission.

# **Step 2: Assemble**

**Getting Started**

1. **Hardware Setup**  
* Connect the SMD to the PC or Arduino board using [USB Gateway Module](https://acrome.gitbook.io/acrome-smd-docs/electronics/gateway-modules/usb-gateway-module) or [Arduino Gateway Module](https://acrome.gitbook.io/acrome-smd-docs/electronics/gateway-modules/arduino-gateway-module).  
* Connect the the [RGB LED Module](https://docs.acrome.net/electronics/add-on-modules/rgb-led-module) and the [Buzzer Module](https://docs.acrome.net/electronics/add-on-modules/buzzer-module) to the SMD using an RJ-45 cable.  
* Make sure that the SMD is powered and all connections are correct.

# **Step 3: Run & Test**

1. **Install Libraries and Run the Script**  
* Install necessary libraries such as Tkinter, serial and acrome-smd.  
* Execute the script, initiating the Morse Code Transmitter project and opening the Tkinter UI where you can enter your text.  
2. **Experience the Morse Transmission**  
* Observe the synchronized light and sound for each dot and dash.  
* Write longer texts to experience longer Morse transmissions.  
3. **Customize and Experiment**  
   * Experiment with changing symbol timings to create “fast” or “slow” Morse.  
   * Explore switching LED colors
