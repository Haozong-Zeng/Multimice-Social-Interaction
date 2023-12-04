# Parts Required for Constructing the Rig
This table contains a list of parts required to build the experimental setup. These parts are divided into those that can be purchased and those that need to be customized. Customized parts can be obtained by simply providing CAD files to 3D printing and CNC manufacturers, and the processing costs are not high.  
## Parts to be purchased
1. 4 Raspberry Pi 4b - Connecting to Pi cameras for brain imaging; GPIO for synchronization, controlling the stepper motor & LEDs. Other versions of Raspberry Pi might require extra modification.  
2. 1 LabJack LabJack U3-LV - Connection to a computer with the high-speed camera (OMRON STC-MBS43U3V) to provide GPIO for synchronization.  
3. 1 OMRON STC-MBS43U3V camera - Recording whisker movements at high fps.  
4. 3 Raspberry Pi Cameras (OmniVision OV5647 CMOS sensor) - Recording GCaMP images.  
5. 3 MIPI cables - Connecting the camera to Raspberry Pi.  
6. 3 Triple-bandpass filters (Chroma 69013m) - One for each GCaMP imaging camera for signal correction.  
7. 3 Short blue, 447.5nm Royal Blue Luxeon Rebel LED SP-01-V4 with Thorlabs FB 440-10 nm band pass filters - Providing information about hemodynamic changes.  
8. 3 Long blue, 470nm Luxeon Rebel LED SP-01-B6 with Chroma 480/30nm band pass filters - Triggering GCaMP fluorescence.  
9. 2 Fosa 140 LED Waterproof Infrared Night Vision Lights - For behavior recording, photoresistor needs to be replaced or shielded.  
10. 4 Transistor-transistor logic (TTL) output power supply units - Synchronously turning on the LEDs with GPIO signals.  
11. 1 30fps Webcam (HBV‑W202012HD) - Recording forelimbs and torso movements.  
12. 1 Stepper Motor
13. 1 Motor Driven Industrial Slide Rail (Mei Ke Chuan Dong) - Manipulating the positions of the mice.
14. Optic Posts, Post Clamps, Optic Breadboards - Flexible, check CAD files for more details.
## Parts to be customized
1. Pi Camera Holders
