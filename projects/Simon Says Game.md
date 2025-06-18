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

## **Project Wiring Diagram**

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

# **Codes:**

## **Python Code:**

\#\#\# projects/simon\_says\_game.py

import os, sys  
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(\_\_file\_\_), '..')))

import time  
import random  
import tkinter as tk  
from tkinter import ttk, messagebox  
from serial.tools.list\_ports import comports  
from platform import system  
from smd.red import Master, Red

\# ─── Hardware Layer ───────────────────────────────────────────────────────────  
def find\_usb\_port():  
   ports \= list(comports())  
   os\_name \= system()  
   usb\_names \= {  
       "Windows": \["USB Serial Port"\],  
       "Linux": \["/dev/ttyUSB"\],  
       "Darwin": \["/dev/tty.usbserial", "/dev/tty.usbmodem", "/dev/cu.usbserial"\]  
   }  
   for port, desc, hwid in sorted(ports):  
       if any(name in port or name in desc for name in usb\_names.get(os\_name, \[\])):  
           return port  
   return None

class Device:  
   def \_\_init\_\_(self, port, baud\=115200, smd\_id\=0, led\_id\=5, buzzer\_id\=5):  
       self.master \= Master(port, baud)  
       self.master.attach(Red(smd\_id))  
       self.master.scan\_modules(smd\_id)  
       self.smd\_id \= smd\_id  
       self.led\_id \= led\_id  
       self.buzzer\_id \= buzzer\_id

   def led\_color(self, r, g, b):  
       self.master.set\_rgb(self.smd\_id, self.led\_id, r, g, b)

   def led\_off(self):  
       self.led\_color(0, 0, 0)

   def beep(self, duration\=0.2):  
       ms \= int(duration \* 1000)  
       self.master.set\_buzzer(self.smd\_id, self.buzzer\_id, ms)  
       time.sleep(duration)  
       self.master.set\_buzzer(self.smd\_id, self.buzzer\_id, 0)

   def close(self):  
       ser \= getattr(self.master, 'serial', None)  
       if ser and hasattr(ser, 'close'):  
           ser.close()

\# ─── Simon Says GUI ────────────────────────────────────────────────────────────  
COLORS \= \[  
   ("Red",   (255, 0,   0)),  
   ("Green", (0,   255, 0)),  
   ("Blue",  (0,   0,   255))  
\]

class SimonSaysApp(tk.Tk):  
   def \_\_init\_\_(self, device):  
       super().\_\_init\_\_()  
       self.title("Simon Says Game")  
       self.resizable(False, False)  
       self.device \= device

       self.sequence \= \[\]  
       self.user\_index \= 0  
        
       self.device.led\_color(\*COLORS\[0\]\[1\])  
       self.device.beep(0.8)  
       self.device.led\_off()  
       time.sleep(1.0)  
        
       self.\_build\_ui()  
      

   def \_build\_ui(self):  
       btn\_frame \= ttk.Frame(self)  
       btn\_frame.pack(pady\=10)

       self.buttons \= \[\]  
       for i, (name, color) in enumerate(COLORS):  
           hexc \= "\#%02x%02x%02x" % color  
           btn \= tk.Button(btn\_frame, text\=name, bg\=hexc, width\=8,  
                           command\=lambda i\=i: self.\_user\_press(i))  
           btn.grid(row\=0, column\=i, padx\=5)  
           self.buttons.append((btn, color))

       control \= ttk.Frame(self)  
       control.pack(pady\=5)

       self.status \= ttk.Label(self, text\="Press Start to play")  
       self.status.pack(pady\=(0,5))

       self.start\_btn \= ttk.Button(control, text\="Start", command\=self.\_start\_game)  
       self.start\_btn.pack()

   def \_start\_game(self):  
       self.sequence.clear()  
       self.\_next\_round()

   def \_next\_round(self):  
       self.start\_btn.config(state\="disabled")  
       self.user\_index \= 0  
       self.sequence.append(random.randrange(len(COLORS)))  
       self.status.config(text\=f"Round {len(self.sequence)} – watch...")  
       \# schedule playback on main thread  
       self.after(500, self.\_play\_sequence, 0)

   def \_play\_sequence(self, idx):  
       if idx \< len(self.sequence):  
           color\_idx \= self.sequence\[idx\]  
           self.\_flash(color\_idx)  
           \# schedule next flash  
           self.after(700, self.\_play\_sequence, idx\+1)  
       else:  
           self.status.config(text\="Your turn")

   def \_flash(self, idx):  
       \_, color \= self.buttons\[idx\]  
       self.device.led\_color(\*color)  
       self.device.beep(0.2)  
       \# turn off after short delay  
       self.after(200, self.device.led\_off)

   def \_user\_press(self, idx):  
       if not self.sequence:  
           return  
       self.\_flash(idx)  
       if idx \== self.sequence\[self.user\_index\]:  
           self.user\_index \+= 1  
           if self.user\_index \== len(self.sequence):  
               \# correct full sequence  
               self.status.config(text\="Correct\! Next round...")  
               self.after(500, self.\_next\_round)  
       else:  
           self.status.config(text\="Wrong\! Game Over")  
           self.start\_btn.config(state\="enabled")  
           self.sequence.clear()

\# ─── Main ─────────────────────────────────────────────────────────────────────  
if \_\_name\_\_ \== '\_\_main\_\_':  
   port \= find\_usb\_port()  
   if not port:  
       print("No USB gateway detected.")  
       sys.exit(1)

   device \= Device(port)  
   app \= SimonSaysApp(device)  
   app.protocol("WM\_DELETE\_WINDOW", lambda: (device.close(), app.destroy()))  
   app.mainloop()

# **Arduino Code:**

// Simon Says Game \- Arduino Standalone Version  
// Hardware: Acrome SMD Arduino Gateway Module \+ RGB LED Module \+ Buzzer Module

\#include \<AcromeSMD.h\>  // You need Acrome's Arduino SMD library

\#define SMD\_ID 0  
\#define LED\_ID 5  
\#define BUZZER\_ID 5

// Setup SMD and modules  
SMDRed smd;  
uint8\_t sequence\[100\];  
uint8\_t userIndex \= 0;  
uint8\_t currentLength \= 0;  
bool userTurn \= false;

const uint8\_t COLORS\[3\]\[3\] \= {  
  {255, 0, 0},  // Red  
  {0, 255, 0},  // Green  
  {0, 0, 255}   // Blue  
};

// Button pins (connect external buttons to these digital pins)  
const int buttonPins\[3\] \= {2, 3, 4};

void setup() {  
  Serial.begin(115200);  
  smd.begin();

  smd.attachModule(SMD\_ID, LED\_ID, RGB);  
  smd.attachModule(SMD\_ID, BUZZER\_ID, BUZZER);

  for (int i \= 0; i \< 3; i++) {  
    pinMode(buttonPins\[i\], INPUT\_PULLUP);  
  }

  // Hardware init blink \+ beep  
  flashColor(0, 300);  
  delay(1000);  
    
  startNewGame();  
}

void loop() {  
  if (userTurn) {  
    for (int i \= 0; i \< 3; i++) {  
      if (digitalRead(buttonPins\[i\]) \== LOW) {  
        delay(200); // debounce  
          
        flashColor(i, 200);  
        if (i \== sequence\[userIndex\]) {  
          userIndex++;  
          if (userIndex \== currentLength) {  
            Serial.println("Correct\! Next round...");  
            delay(500);  
            nextRound();  
          }  
        } else {  
          Serial.println("Wrong\! Game Over.");  
          delay(1000);  
          startNewGame();  
        }  
      }  
    }  
  }  
}

void startNewGame() {  
  currentLength \= 0;  
  userIndex \= 0;  
  nextRound();  
}

void nextRound() {  
  if (currentLength \< sizeof(sequence)) {  
    sequence\[currentLength\] \= random(0, 3);  
    currentLength++;  
    playSequence();  
    userIndex \= 0;  
    userTurn \= true;  
  }  
}

void playSequence() {  
  userTurn \= false;  
  Serial.print("Round ");  
  Serial.println(currentLength);  
  delay(500);  
  for (int i \= 0; i \< currentLength; i++) {  
    flashColor(sequence\[i\], 200);  
    delay(500);  
  }  
}

void flashColor(uint8\_t colorIndex, uint16\_t duration) {  
  smd.setRGB(SMD\_ID, LED\_ID, COLORS\[colorIndex\]\[0\], COLORS\[colorIndex\]\[1\], COLORS\[colorIndex\]\[2\]);  
  smd.setBuzzer(SMD\_ID, BUZZER\_ID, duration);  
  delay(duration);  
  smd.setRGB(SMD\_ID, LED\_ID, 0, 0, 0);  
}  
