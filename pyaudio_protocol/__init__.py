
__version__ = "0.2.0"

try:
    import PyQt5
    HAVE_PyQt5 = True
except ImportError:
    HAVE_PyQt5 = False

try:
    import RPi.GPIO as GPIO
    HAVE_GPIO = True
except ImportError:
    HAVE_GPIO = False


if HAVE_PyQt5:
    from .core_gui import PyAudio_protocol
    print("Gui Mode")

if HAVE_GPIO:
    from .core_rpi_nogui import PyAudio_protocol_rpi

from .test_tools import list_audio_device, show_device_sr, test_simple_syncro_parallel
from .test_tools import get_sin
