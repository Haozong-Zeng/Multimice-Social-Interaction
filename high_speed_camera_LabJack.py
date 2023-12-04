import os

#import board
#import digitalio
#import tempfile
from datetime import datetime
import stapipy as st
import time
import numpy as np
import u3 # This is using LabJack on laptop to do sync!
import io
import pandas as pd
from pathlib import Path
#import cv2

#Device:LabJack U3
d = u3.U3()

#trigger pin is connected to raspberry pi
#trigger_pin = digitalio.DigitalInOut(board.C0)
#trigger_pin.direction = digitalio.Direction.INPUT

#camera_pin = digitalio.DigitalInOut(board.C1)
#camera_pin.direction = digitalio.Direction.INPUT



# Number of images to grab
duration = 200
fps = 300
number_of_images_to_grab = round(duration * fps)

# Path to save the video
savepath = r"C:\Users\Haozong\OneDrive\Dual Brain\Whisker"

# Maximum number of frames in one video file
maximum_frame_count_per_file = 100_000

# Number of video files
video_files_count = 1

# Timestamps and frame number streams
s_timestamp = io.StringIO()
s_frame_n = io.StringIO()


def videofiler_callback(handle=None, context=None):
    """
    Callback to handle events from Video Filer.

    :param handle: handle that trigger the callback.
    :param context: user data passed on during callback registration.
    """
    callback_type = handle.callback_type
    videofiler = handle.module
    if callback_type == st.EStCallbackType.StApiIPVideoFilerOpen:
        print("Open:", handle.data['filename'])
    elif callback_type == st.EStCallbackType.StApiIPVideoFilerClose:
        print("Close:", handle.data['filename'])
    elif callback_type == st.EStCallbackType.StApiIPVideoFilerError:
        print("Error:", handle.error[1])
        context['error'] = True


if __name__ == "__main__":
    try:
        
        # Initialize StApi before using.
        st.initialize()
        
        # Create a system object for device scan and connection.
        st_system = st.create_system()

        # Connect to first detected device.
        st_device = st_system.create_first_device()

        # Display DisplayName of the device.
        print('Device=', st_device.info.display_name)

        # Get the acquisition fps of the camera.
        acquisition_frame_rate = st_device.remote_port.nodemap.get_node(
            "AcquisitionFrameRate")        
        acquisition_frame_rate.value = fps

        # Create PyStVideoFiler
        st_videofiler = st.create_filer(st.EStFilerType.Video)

        # Register a callback function.
        callback_info = {'error': False}
        videofiler_cb = st_videofiler.register_callback(videofiler_callback,
                                                        callback_info)

        # Configure the video file settings.
        st_videofiler.maximum_frame_count_per_file = \
            maximum_frame_count_per_file
        st_videofiler.video_file_format = st.EStVideoFileFormat.AVI1
        st_videofiler.video_file_compression = \
            st.EStVideoFileCompression.MotionJPEG
        st_videofiler.fps = fps

        # Register video files
        sep = "-"
        date = datetime.today().strftime('%Y%m%d')
        filename = sep.join((date, "whisker"))
        st_videofiler.register_filename(savepath + "/" + filename + ".avi")

        # Create a datastream object for handling image stream data.
        st_datastream = st_device.create_datastream()

        #print("Trigger received. Waiting for record")
        #while not camera_pin.value:
        #    pass

        print("waiting for trigger")
        while d.getDIState(ioNum=0):
            pass
        # Start the image acquisition of the host (local machine) side.
        st_datastream.start_acquisition(number_of_images_to_grab)

        # Start the image acquisition of the camera side.
        st_device.acquisition_start()

        first_frame = True
        first_timestamp = 0
        framesize = 720*540
        print(number_of_images_to_grab * framesize * 8)
        frame_number = 0
        while st_datastream.is_grabbing:

            if callback_info['error']:
                break
            with st_datastream.retrieve_buffer() as st_buffer:
                # Check if the acquired data contains image data.
                if st_buffer.info.is_image_present:
                    # Create an image object.
                    st_image = st_buffer.get_image()
                    
                    # Display the information of the acquired image data.
                    print("BlockID={0} Size={1} x {2} {3:.2f} fps".format(
                          st_buffer.info.frame_id,
                          st_image.width, st_image.height,
                          st_datastream.current_fps))

                    # Calculate frame number in case of frame drop.
                    frame_no = 0
                    current_timestamp = st_buffer.info.timestamp
                    if first_frame:
                        first_frame = False
                        delta = 0
                        first_timestamp = current_timestamp
                    else:
                        delta = current_timestamp - first_timestamp
                        tmp = delta * fps / 1000000000.0
                        frame_no = int(tmp + 0.5)

                    # Add the image data to video file.
                    st_videofiler.register_image(st_image, frame_no)
                    
                    # Add the timestamp and frame number to stream
                    s_timestamp.write(str(delta / 1000000000.0) + ' ')
                    s_frame_n.write(str(frame_number)+ ' ')
                    frame_number += 1
                else:
                    # If the acquired data contains no image data.
                    print("Image data does not exist.")


        # Stop the image acquisition of the camera side
        st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        st_datastream.stop_acquisition()
        
        # Save the timestamps and frame numbers
        timestamps = s_timestamp.getvalue()
        timestamps = timestamps.split()
        frames = s_frame_n.getvalue()
        frames = frames.split()
        df = pd.DataFrame({'frame number':frames, 'timestamp':timestamps})
        df['timestamp'] = df['timestamp'].astype(float) + float(df['timestamp'][2])
        df.iloc[0, 1] = 0
        file_path = Path(savepath + '/' + sep.join((date, "whisker-timestamp.csv")))  
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path)
        print('done')
    except Exception as exception:
        print(exception)


