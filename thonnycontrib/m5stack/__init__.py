from thonny.plugins.micropython import MicroPythonProxy, MicroPythonConfigPage,\
    add_micropython_backend
from thonny import get_workbench, get_runner
import os
import subprocess
from thonny.ui_utils import SubprocessDialog
from thonny.running import get_frontend_python
from time import sleep

class M5StackProxy(MicroPythonProxy):
    pass

class M5StackConfigPage(MicroPythonConfigPage):
    def _get_usb_driver_url(self):
        return "https://docs.m5stack.com/#/en/related_documents/establish_serial_connection"

def load_plugin():
    add_micropython_backend("M5Stack", M5StackProxy, "MicroPython on M5Stack", M5StackConfigPage)

    def m5burner():
        pass
        
    get_workbench().add_command("m5burner", "device", "Open M5Burner...",
                                m5burner,
                                group=40)
    