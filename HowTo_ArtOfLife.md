# ART OF LIFE - Documentation

Everything necessary for this project


# Hardware :

Plux Biosignals ECG Sensor : https://www.pluxbiosignals.com/products/electrocardiography-ecg-sensor?variant=40878841200831

Plux Biosignals EDA Sensor : https://www.pluxbiosignals.com/products/electrodermal-activity-eda-sensor

Plux Biosignals Breathing Sensor : https://www.pluxbiosignals.com/products/respiration-pzt

Plux Biosignals Bitalino card : https://www.pluxbiosignals.com/products/bitalino-revolution-plugged-kit-ble-bt

5 electrodes : https://www.pluxbiosignals.com/products/gelled-self-adhesive-disposable-ag-agcl-electrodes


# Softwares :

Visual Studio Code

MadMapper

loopMIDI

# How to set up ? 

You can find attached here the description of every step of the installation. You can learn how to correctly position the sensors on the user, how to launch the software and calibrate it, and how to set up the installation.


<img width="1500" alt="Template2" src="https://github.com/inesbnr/Art-Of-Life-Emotions-Management/assets/98738106/dda29e5b-5912-4d6b-8515-d4f848d9cb0a">



a. ECG Sensor

This sensor uses three electrodes placed on the user’s upper body. You must connect the three electrodes to the sensor to ensure qualitative data. The reference electrode can be placed around the left lowest rib for an easier installation.

 
b. EDA Sensor

This sensor uses two electrodes placed on one of the user’s hands. You must connect the two electrodes to ensure qualitative data.

 
c. Breathing Sensor

This sensor uses a stretchable band that must be placed around the user’s ribs and will detect when the user inhales and exhales.

 
2. Bitalino card & OpenSignals

a. Connecting the sensors to the Bitalino card

The Bitalino card is responsible for gathering all the data from the three sensors and sending them to the OpenSignals software. The card possesses multiple ports beginning with “A”, being the ones which the sensors need to be connected to. Make sure to connect the ECG Sensor to “A1”, the EDA Sensor to “A2” and the Breathing Sensor to “A3”. Then, turn on the card so it can connect to the OpenSignals software by Bluetooth.

 
b. Visualizing the data on OpenSignals

The OpenSignals software helps visualize the sensors’ data and send it to an external python program. These results need multiple actions to be done. Firstly, you need to connect the software to the card, then you can select which ports are connected to which sensors.

 
c. Sending the data to the Python program

The sensor data can be sent to a Python program using the Lab Streaming Layer. To do so, you need to activate the “Lab Streaming Layer” parameter in the “Integration” section of the settings (the button next to the one used for connecting to the Bitalino card).

3. Python & loopMIDI

   
a. The Python program

The Python program is responsible for converting the raw data into MIDI notes. For this purpose, the program receives the values from OpenSignals and detects when a pulse is happening or if the user is inhaling or exhaling. During these events, the program sends different MIDI notes to multiple programs to impact the visuals displayed. This program is called "ArtOfLife.py" and can be found on this GitHub repository. But before running the program, we must create virtual MIDI ports.
 
b. loopMIDI

For the Python program to be able to send MIDI notes, the computer needs to open virtual MIDI ports to receive the notes, and so is the role of loopMIDI. loopMIDI is a very simplistic software that can open personalized MIDI ports. You will need to create two ports that will link to the FL Studio software. Make sure to call them “loopMIDI Port FL” and “loopMIDI Port FL2”. Then, you must connect one port related to the MadMapper software. Make sure to call it “loopMIDI Port MM”. Only after that you can start running the Python program.

 
5.MadMapper

MadMapper (version 5.0.7) is the video-mapping software used in this project. The software will display predefined shaders which will react to the MIDI notes it receives from loopMIDI. The MadMapper file is called “Art_Of_Life_demo.mad” and can be found on this GitHub repository.

To ensure that the visual is displayed with the projector, once it is connected to your computer, make sure to set the "extend display" mode in your computer settings. Then click on the following icon, top left in madmapper :

Then click on "Video-output-1" and a new table with more information will appear at bottom left. Click on "Desktop Window"

This button lets you load a new window that you'll need to place on your "second screen", i.e. whatever the projector is projecting.
Now the visual projection is all set ! But let's make sure that the midi port are well connected to it.
As we are projecting onto a 3D wall, make sure to adjust the shape of the visuals to fit the structure. Select the "ArtOfLife" group and adjust its size along the size of the structure.

![Template2-2](https://github.com/inesbnr/Art-Of-Life-Emotions-Management/assets/98738106/18820710-9a32-43c8-9a69-be9f664e5078)


