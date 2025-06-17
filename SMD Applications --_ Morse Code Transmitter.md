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

## **Project Wiring Diagram**

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

# **Codes:**

## **Python Code:**

import os, sys  
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(\_\_file\_\_), '..')))

import time  
import threading  
import tkinter as tk  
from tkinter import ttk, messagebox  
from serial.tools.list\_ports import comports  
from platform import system  
from smd.red import Master, Red

\# Morse-code timing  
DOT\_DURATION   \= 0.2  
DASH\_DURATION  \= DOT\_DURATION \* 3  
SYMBOL\_PAUSE   \= DOT\_DURATION  
LETTER\_PAUSE   \= DOT\_DURATION \* 3  
WORD\_PAUSE     \= DOT\_DURATION \* 7

\# Morse lookup  
def build\_morse\_map():  
   return {  
       'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',  
       'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',  
       'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',  
       'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',  
       'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',  
       'Z': '--..',  
       '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',  
       '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'  
   }  
MORSE\_CODE \= build\_morse\_map()

\# Hardware layer  
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

class MorseHardware:  
   def \_\_init\_\_(self, port, baud\=115200, smd\_id\=0, led\_id\=5, buzzer\_id\=5):  
       self.master \= Master(port, baud)  
       self.master.attach(Red(smd\_id))  
       self.master.scan\_modules(smd\_id)  
       self.smd\_id \= smd\_id  
       self.led\_id \= led\_id  
       self.buzzer\_id \= buzzer\_id

   def led\_on(self):  
       self.master.set\_rgb(self.smd\_id, self.led\_id, 255, 255, 255)

   def led\_off(self):  
       self.master.set\_rgb(self.smd\_id, self.led\_id, 0, 0, 0)

   def beep(self, dur):  
       \# dur in seconds  
       ms \= int(dur \* 1000)  
       \# Start beep  
       self.master.set\_buzzer(self.smd\_id, self.buzzer\_id, ms)  
       time.sleep(dur)  
       \# Stop beep  
       self.master.set\_buzzer(self.smd\_id, self.buzzer\_id, 0)

   def close(self):  
       ser \= getattr(self.master, 'serial', None)  
       if ser and hasattr(ser, 'close'):  
           ser.close()

\# Morse logic  
def transmit\_symbol(symbol, hw):  
   dur \= DOT\_DURATION if symbol \== '.' else DASH\_DURATION  
   hw.led\_on()  
   hw.beep(dur)  
   hw.led\_off()  
   time.sleep(SYMBOL\_PAUSE)

def transmit\_message(msg, hw, on\_progress\=None):  
   cleaned \= msg.strip().upper()  
   symbols \= \[sym for ch in cleaned if ch \!= ' ' for sym in MORSE\_CODE.get(ch, '')\]  
   total \= len(symbols)  
   count \= 0  
   for word in cleaned.split():  
       for ch in word:  
           for sym in MORSE\_CODE.get(ch, ''):  
               transmit\_symbol(sym, hw)  
               count \+= 1  
               if on\_progress and total:  
                   on\_progress(int(count / total \* 100))  
           time.sleep(LETTER\_PAUSE \- SYMBOL\_PAUSE)  
       time.sleep(WORD\_PAUSE \- LETTER\_PAUSE)  
   if on\_progress:  
       on\_progress(100)

\# GUI  
def to\_morse\_string(msg):  
   words \= \[\]  
   for word in msg.strip().upper().split():  
       letters \= \[MORSE\_CODE.get(ch, '') for ch in word\]  
       words.append(' '.join(filter(None, letters)))  
   return ' / '.join(words)

class MorseGUI(tk.Tk):  
   def \_\_init\_\_(self):  
       super().\_\_init\_\_()  
       self.title("Morse Code Transmitter")  
       self.resizable(False, False)

       port \= find\_usb\_port()  
       if not port:  
           messagebox.showerror("Error", "No USB gateway detected.")  
           self.destroy()  
           sys.exit(1)  
       self.hw \= MorseHardware(port)

       ttk.Label(self, text\="Enter message:").grid(row\=0, column\=0, padx\=8, pady\=(10, 2), sticky\="w")  
       self.msg\_var \= tk.StringVar()  
       entry \= ttk.Entry(self, textvariable\=self.msg\_var, width\=42)  
       entry.grid(row\=1, column\=0, columnspan\=2, padx\=8, sticky\="ew")  
       entry.focus()  
       self.msg\_var.trace\_add("write", self.\_update\_code)

       ttk.Label(self, text\="Morse code:").grid(row\=2, column\=0, padx\=8, pady\=(6, 2), sticky\="w")  
       self.code\_lbl \= tk.Label(self, text\="", font\=("Courier", 10), justify\="left", wraplength\=300)  
       self.code\_lbl.grid(row\=3, column\=0, columnspan\=2, padx\=8, sticky\="w")

       self.tx\_btn \= ttk.Button(self, text\="Transmit", command\=self.\_start)  
       self.tx\_btn.grid(row\=4, column\=0, padx\=8, pady\=10, sticky\="e")  
       self.progress \= ttk.Progressbar(self, mode\="determinate", length\=200)  
       self.progress.grid(row\=4, column\=1, padx\=(0, 8), pady\=10, sticky\="w")  
       self.protocol("WM\_DELETE\_WINDOW", self.\_on\_close)

   def \_update\_code(self, \*\_):  
       self.code\_lbl.config(text\=to\_morse\_string(self.msg\_var.get()))

   def \_start(self):  
       msg \= self.msg\_var.get().strip()  
       if not msg:  
           messagebox.showinfo("Input", "Enter a message.")  
           return  
       self.tx\_btn.state(\["disabled"\])  
       self.progress\["value"\] \= 0  
       threading.Thread(target\=self.\_worker, args\=(msg,), daemon\=True).start()

   def \_worker(self, msg):  
       try:  
           transmit\_message(msg, self.hw, self.\_prog)  
       except Exception as e:  
           messagebox.showerror("Error", str(e))  
       finally:  
           self.tx\_btn.state(\["\!disabled"\])  
           self.progress\["value"\] \= 0

   def \_prog(self, p):  
       self.progress\["value"\] \= p

   def \_on\_close(self):  
       self.hw.close()  
       self.destroy()

if \_\_name\_\_ \== '\_\_main\_\_':  
   MorseGUI().mainloop()

# **Arduino Code:**

\#include \<Acrome-SMD.h\>  
\#include \<ctype.h\>          // toupper()

\#define SMD\_ID       0      // master ID on the SMD bus  
\#define BAUDRATE     115200 // USB (and Serial Monitor) baud  
\#define LED\_ID       5      // port number of RGB LED Module  
\#define BUZZER\_ID    5      // port number of Buzzer Module

Red master(SMD\_ID, Serial, BAUDRATE);

/\* \---------- Morse\-code timing (milliseconds) \---------- \*/  
const uint16\_t DOT\_DURATION   \= 200;  
const uint16\_t DASH\_DURATION  \= DOT\_DURATION \* 3;  
const uint16\_t SYMBOL\_PAUSE   \= DOT\_DURATION;  
const uint16\_t LETTER\_PAUSE   \= DOT\_DURATION \* 3;  
const uint16\_t WORD\_PAUSE     \= DOT\_DURATION \* 7;

/\* \---------- Lookup table: A–Z, 0–9 \---------- \*/  
struct MorsePair { char ch; const char \*code; };  
const MorsePair MORSE\_TABLE\[\] PROGMEM \= {  
 { 'A', ".-"   }, { 'B', "-..." }, { 'C', "-.-." }, { 'D', "-.."  }, { 'E', "."    },  
 { 'F', "..-." }, { 'G', "--."  }, { 'H', "...." }, { 'I', ".."   }, { 'J', ".---" },  
 { 'K', "-.-"  }, { 'L', ".-.." }, { 'M', "--"   }, { 'N', "-."   }, { 'O', "---"  },  
 { 'P', ".--." }, { 'Q', "--.-" }, { 'R', ".-."  }, { 'S', "..."  }, { 'T', "-"    },  
 { 'U', "..-"  }, { 'V', "...-" }, { 'W', ".--"  }, { 'X', "-..-" }, { 'Y', "-.--" },  
 { 'Z', "--.." },  
 { '0', "-----"}, { '1', ".----"}, { '2', "..---"}, { '3', "...--"}, { '4', "....-"},  
 { '5', "....."}, { '6', "-...."}, { '7', "--..."}, { '8', "---.."}, { '9', "----."}  
};  
const uint8\_t TABLE\_LEN \= sizeof(MORSE\_TABLE) / sizeof(MORSE\_TABLE\[0\]);

/\* Look up a character – returns nullptr if unsupported \*/  
const char\* morseLookup(char c) {  
 c \= toupper(c);  
 for (uint8\_t i \= 0; i \< TABLE\_LEN; \++i) {  
   if (pgm\_read\_byte(&MORSE\_TABLE\[i\].ch) \== c)  
     return (const char\*)pgm\_read\_word(&MORSE\_TABLE\[i\].code);  
 }  
 return nullptr;  
}

/\* \---------- Low\-level helpers \---------- \*/  
void ledOn()  { master.setRGB(LED\_ID, 255, 255, 255); }  
void ledOff() { master.setRGB(LED\_ID, 0, 0, 0); }

void beep(uint16\_t durMs) {  
 master.setBuzzer(BUZZER\_ID, durMs);   // buzzer auto\-stops after durMs  
 delay(durMs);  
}

void transmitSymbol(char sym) {  
 uint16\_t dur \= (sym \== '.') ? DOT\_DURATION : DASH\_DURATION;  
 ledOn();  
 beep(dur);  
 ledOff();  
 delay(SYMBOL\_PAUSE);  
}

/\* \---------- Transmit an entire message \---------- \*/  
void transmitMessage(const char \*msg) {  
 while (\*msg) {  
   char c \= \*msg\++;  
   if (c \== ' ') {                       // space → word gap  
     delay(WORD\_PAUSE \- LETTER\_PAUSE);  
     continue;  
   }  
   const char \*pattern \= morseLookup(c);  
   if (\!pattern) continue;               // skip unsupported chars  
   while (\*pattern) {  
     transmitSymbol(\*pattern\++);  
   }  
   delay(LETTER\_PAUSE \- SYMBOL\_PAUSE);   // gap between letters  
 }  
}

/\* \---------- Setup & Main Loop \---------- \*/  
void setup() {  
 Serial.begin(BAUDRATE);  
 while (\!Serial) ;                       // wait for PC

 master.begin();  
 master.scanModules();  
 Serial.println(F("=== SMD Morse Code Transmitter \==="));  
 Serial.println(F("Type a line of text and press ENTER.\\n"));  
}

String line \= "";

void loop() {  
 // Collect one line from Serial Monitor  
 while (Serial.available()) {  
   char ch \= Serial.read();  
   if (ch \== '\\n' || ch \== '\\r') {  
     if (line.length() \> 0) {  
       Serial.print(F("Sending: \\"")); Serial.print(line); Serial.println('"');  
       transmitMessage(line.c\_str());  
       Serial.println(F("Done.\\n"));  
       line \= "";  
     }  
   } else {  
     line \+\= ch;  
   }  
 }  
}