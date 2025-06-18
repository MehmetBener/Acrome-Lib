**Category:** SMD Applications → Interactive

# **Simon Says Game**

A Python-based Simon Says memory game that uses an SMD Red gateway with the RGB LED Module and Buzzer Module for visual and audio feedback. The game presents an ever-growing sequence of colors that the player must repeat correctly to advance to the next round.

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

Depending on the game sequence, this module lights up in **Red**, **Green**, or **Blue**. It helps the player visually memorize the pattern.

3. Buzzer Module

Emits a **short beep** along with the LED flash for audio feedback. This pairing enhances the user’s memory and reaction.

4. SMD Libraries

The official Acrome SMD Python library handles low-level serial communication, device scanning, and module control, letting you focus on the Simon Says logic and GUI.

## **Project Key Features**

* **Visual \+ Audible Feedback**

Each color is accompanied by a synchronized flash and beep.

* **Growing Memory Challenge**

The sequence grows with each successful round, increasing difficulty.

* **Tkinter Graphical Interface**

Simple UI with buttons for Red, Green, and Blue, a start button, and a status message.

* **Built-in Hardware Warm-Up**

The RGB LED is initialized once before gameplay to bypass any first-flash issues.

# **Step 2: Assemble**

**Getting Started**

1. **Hardware Setup**  
* Connect the SMD to the PC or Arduino board using [the USB Gateway Module](https://acrome.gitbook.io/acrome-smd-docs/electronics/gateway-modules/usb-gateway-module) or [the Arduino Gateway Module](https://acrome.gitbook.io/acrome-smd-docs/electronics/gateway-modules/arduino-gateway-module).  
* Connect the [RGB LED Module](https://docs.acrome.net/electronics/add-on-modules/rgb-led-module) and the [Buzzer Module](https://docs.acrome.net/electronics/add-on-modules/buzzer-module) to the SMD using an RJ-45 cable.  
* Make sure that the SMD is powered and all connections are correct.

# **Step 3: Run & Test**

1. **Install Libraries and Run the Script**  
* Install necessary libraries such as Tkinter, serial, and acrome-smd.  
* Execute the script, initiating the Simon Says project and opening the Tkinter UI where you can enter your text.  
2. **Play the Simon Says Game**  
* Click **Start** to begin.  
* Watch the color sequence.  
* Repeat the sequence using the buttons.  
* If correct, the game adds one more color and continues.  
* If wrong, the game ends and can be restarted.
