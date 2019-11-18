from thonny.plugins.micropython import MicroPythonProxy, MicroPythonConfigPage,\
    add_micropython_backend
from thonny import get_workbench, get_runner, ui_utils
import os
import subprocess
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
from thonny.ui_utils import SubprocessDialog
from thonny.running import get_interpreter_for_subprocess
from time import sleep
import json
import threading

INDEX_BASE_URL = "https://thonny.org/m5stack/firmwares"

class M5StackProxy(MicroPythonProxy):
    pass

class M5StackConfigPage(MicroPythonConfigPage):
    def _get_usb_driver_url(self):
        return "https://docs.m5stack.com/#/en/related_documents/establish_serial_connection"

class M5Burner(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self._firmware_infos = {}
        
        self.title("M5Burner")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, ipadx=15, ipady=15)
        
        ttk.Label(main_frame, text="Baud rate").grid(row=1, column=0, padx=(15,5), pady=(15,5))
        self.baud_combo = ttk.Combobox(main_frame, 
                                       exportselection=False,
                                       state="readonly",
                                       values = ["a", "b", "c"])
        self.baud_combo.grid(row=1, column=1, columnspan=2, padx=(5,15), pady=(15,5))
        
        ttk.Label(main_frame, text="Firmware").grid(row=2, column=0, padx=(15,5), pady=5)
        self.firmware_combo = ttk.Combobox(main_frame, 
                                           exportselection=False,
                                           state="readonly",
                                           values=[],
                                           height=15)
        self.firmware_combo.grid(row=2, column=1, columnspan=2, padx=(5,15), pady=5)
        
        threading.Thread(target=self._download_infos, daemon=True).start()
        
        self._update_state()
    
    def _download_infos(self):
        url = INDEX_BASE_URL + "/firmware.json"
        with urlopen(url) as f:
            data = json.load(f)
        infos = {}
        for spec in data:
            infos[spec["name"]] = spec
        
        self._firmware_infos = infos
        
        
    
    def _update_state(self):
        if self._firmware_infos:
            option_values = self.firmware_combo.cget("values")
            if not option_values:
                print(self._firmware_infos)
                option_values = list(sorted(self._firmware_infos.keys()))
                self.firmware_combo.configure(values=option_values)
            
        self.after(300, self._update_state)

def load_plugin():
    add_micropython_backend("M5Stack", M5StackProxy, "MicroPython on M5Stack", M5StackConfigPage)

    def open_m5burner():
        dlg = M5Burner(get_workbench())
        ui_utils.show_dialog(dlg)
        
    get_workbench().add_command("m5burner", "device", "Open M5Burner...",
                                open_m5burner,
                                group=40)
    