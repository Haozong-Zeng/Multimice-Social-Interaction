# Parts Required for Constructing the Rig
This table contains a list of parts required to build the experimental setup. These parts are divided into those that can be purchased and those that need to be customized. Customized parts can be obtained by simply providing CAD files to 3D printing and CNC manufacturers, and the processing costs are not high.  
## Parts to be purchased
**1**. 4 Raspberry Pi 4b - Connecting to Pi cameras for brain imaging; GPIO for synchronization, controlling the stepper motor & LEDs. Other versions of Raspberry Pi might require extra modification.  
**2**. 1 LabJack LabJack U3-LV - Connection to a computer with the high-speed camera (OMRON STC-MBS43U3V) to provide GPIO for synchronization.  
**3**. 1 OMRON STC-MBS43U3V camera - Recording whisker movements at high fps.  
**4**. 1 Full-band Beam Splitter (Reflection/Transmission Ratio 80%/20%) from Edmund Optics - Recording whisker & limbs.  
**5**. 1 Computer - Recording behavior data at high fps.  
**6**. 3 Raspberry Pi Cameras (OmniVision OV5647 CMOS sensor) - Recording GCaMP images.  
**7**. 3 MIPI cables - Connecting the camera to Raspberry Pi.  
**8**. 3 Triple-bandpass filters (Chroma 69013m) - One for each GCaMP imaging camera for signal correction.  
**9**. 3 Short blue, 447.5nm Royal Blue Luxeon Rebel LED SP-01-V4 with Thorlabs FB 440-10 nm band pass filters - Providing information about hemodynamic changes.  
**10**. 3 Long blue, 470nm Luxeon Rebel LED SP-01-B6 with Chroma 480/30nm band pass filters - Triggering GCaMP fluorescence.  
**11**. 2 Fosa 140 LED Waterproof Infrared Night Vision Lights - For behavior recording, photoresistor needs to be replaced or shielded.  
**12**. 4 Transistor-transistor logic (TTL) output power supply units - Synchronously turning on the LEDs with GPIO signals.  
**13**. 1 30fps Webcam (HBV‑W202012HD) - Recording forelimbs and torso movements.  
**14**. 1 Stepper Motor  
**15**. 1 Motor Driven Industrial Slide Rail with Supports (Mei Ke Chuan Dong) - Manipulating the positions of the mice.  
**16**. Various Optic Posts, Post Clamps, Optic Breadboards - Flexible, check CAD files for more details.  
## Parts to be customized
**1**. 3 Pi Camera Holders - Holding the GCaMP imaging Pi cameras; 3D printing.  
**2**. 6 Head-fixing Clamps & Bars - Head-fixing the mice; CNC or other metal processing.  
**3**. 3 Transparent Acrylic Tubes - Head-fixing the mice; any mechanical processing that works.  
**4**. 3 Bases that holds the Tubes - Head-fixing the mice; 3D printing.  
**5**. 1 Beam Splitter Holder - Holding the beam splitter; 3D printing.  
**6**. 1 Whisker Imaging Background - A board providing white background for better imaging quality and easier whisker tracking.
**7**. 2 Flexible Rail Adaptor - Fixing the Mouse Tube or other structure on the rail, allowing some spacial adjustments.
