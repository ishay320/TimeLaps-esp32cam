# Time laps for es32-cam

# The files

| name | What it does |
|------|--------------|
| `main.cpp` | The code for esp32 |
| `dependency.bat` | Installs python virtual env with `requirements.txt` |
| `combinepics.py` | Code to combine the pics |
| `gst.txt` | Snippet for gstreamer | 
| `light_trace.py` | Code to combine pics to light path |

# Installation
1. Make sure that the virtual env is not in the main folder (bug in pio).
1. Use `platformIO` to install the `main.cpp` file on the esp32.
1. Connect the esp32 to power with sd card installed and it will run.
1. Run `dependency.bat` to install the virtual env.
1. Run `dependency.py` to combine the photos.
1. Run Gstreamer to combine the photos to video.
