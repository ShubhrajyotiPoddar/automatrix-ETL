# %%
import pyautogui
import time
from pywinauto import Application
from pywinauto.findwindows import find_elements
import os
import pygetwindow as gw
import PIL
from datetime import datetime, timedelta
import ctypes
import argparse
import pyperclip

# --- CONFIGURATION & CREDENTIALS (REDACTED) ---
ERP_USERNAME = "REDACTED_ERP_USER"
ERP_PASSWORD = "REDACTED_ERP_PASSWORD"
ERP_SHORTCUT_PATH = r"X:\REDACTED_PATH\MAIN_ERP_TREE_SHORTCUT.lnk"
WINDOW_TITLE = ' Lighthouse ERP - A Software By Lighthouse Systems Pvt. Ltd., Nagpur'
# ----------------------------------------------

# %%
def focus_lighthouse_window():
    try:
        windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        if windows:
            window = windows[0]
            window.activate()  # Bring to front and focus
            print(f"Focused window: {window.title}")
            window.resizeTo(1366, 768)
            window.moveTo(0, 0)
            return window
        else:
            print("ERP window not found!")
            return None
    except Exception as e:
        print(f"Error focusing window: {e}")
        return None


# %%
def login_gui():
    time.sleep(2)
    # Using redacted credential variable
    pyautogui.write(ERP_USERNAME, 0.5) 
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    # Using redacted credential variable
    pyperclip.copy(ERP_PASSWORD)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.press('enter')
    # ... sequence of enters for login ...
    for _ in range(5):
        time.sleep(1.5)
        pyautogui.press('enter')
    time.sleep(3)
    pyautogui.press('enter')
    return

# %%
def get_coordinates():
    print("Move mouse to field and wait...")
    time.sleep(5)
    x1, y1 = pyautogui.position()
    print("x: ",x1,"y: ", y1)

# %%
curr_dt = datetime.now()
from_dt = curr_dt - timedelta(days=2)
filename1 = f"PUR {from_dt.day}{from_dt.strftime('%b').upper()}-{curr_dt.day}{curr_dt.strftime('%b').upper()}"
filename2 = f"GRN {from_dt.day}{from_dt.strftime('%b').upper()}-{curr_dt.day}{curr_dt.strftime('%b').upper()}"
filename3 = f"ISSUE {from_dt.day}{from_dt.strftime('%b').upper()}-{curr_dt.day}{curr_dt.strftime('%b').upper()}"
from_dt_str = from_dt.strftime("%d-%m-%Y")

# %%
def purchase_order():
    pyautogui.click(615, 573)
    time.sleep(3)
    pyautogui.click(717, 167)
    time.sleep(2)
    pyautogui.press('backspace', presses=5)
    pyautogui.write('06.208.01%', interval= 0.2)
    pyautogui.press('enter', presses=2)
    time.sleep(2)
    pyautogui.click(983,572)
    time.sleep(5)
    pyautogui.click(994, 122)
    time.sleep(5)

    pyautogui.click(727, 169)
    pyautogui.press('backspace', presses=5)
    pyautogui.write('R152%')
    pyautogui.press('enter', presses=2)
    
    pyautogui.press('enter')
    button_location = pyautogui.locateOnScreen('./template/show_button.png', confidence=0.7)
    pyautogui.click(button_location)
    time.sleep(3)
    pyautogui.click(202, 272)
    time.sleep(2)
    pyautogui.press('end')
    pyautogui.press('backspace', presses=15)
    time.sleep(2)
    pyautogui.typewrite(from_dt_str, 0.2)
    time.sleep(2)
    pyautogui.click(508, 627)
    time.sleep(2)
    pyautogui.click(910, 641)
    time.sleep(2)
    pyautogui.press('d', presses=4, interval=0.5)
    pyautogui.press('enter')
    time.sleep(3)
    button_location = pyautogui.locateOnScreen('./template/print_button.png', confidence=0.9)
    pyautogui.click(button_location)
    time.sleep(3)
    pyperclip.copy(filename1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(7)
    pyautogui.press('enter')
    time.sleep(5)
    button_location = pyautogui.locateOnScreen('./template/exit_button.png', confidence=0.9)
    pyautogui.click(button_location)
    return 


# %%
def grn_engine():
    pyautogui.click(615, 573)
    time.sleep(3)
    pyautogui.click(717, 167)
    time.sleep(2)
    pyautogui.press('backspace', presses=5)
    pyautogui.write('06.212.02%', interval= 0.2)
    pyautogui.press('enter', presses=2)
    time.sleep(2)
    pyautogui.click(983,572)
    time.sleep(5)
    pyautogui.click(994, 122)
    time.sleep(5)
    pyautogui.click(727, 169)
    pyautogui.press('backspace', presses=5)
    pyautogui.write('R74%')
    pyautogui.press('enter', presses=2)
    time.sleep(2)
    button_location = pyautogui.locateOnScreen('./template/show_button.png', confidence=0.7)
    pyautogui.click(button_location)
    time.sleep(3)
    pyautogui.click(202, 272)
    time.sleep(2)
    pyautogui.press('end')
    pyautogui.press('backspace', presses=15)
    time.sleep(2)
    pyautogui.typewrite(from_dt_str, 0.2)
    time.sleep(2)
    pyautogui.click(508, 627)
    time.sleep(2)
    pyautogui.click(910, 641)
    time.sleep(2)
    pyautogui.press('d', presses=4, interval=0.5)
    pyautogui.press('enter')
    time.sleep(3)
    button_location = pyautogui.locateOnScreen('./template/print_button.png', confidence=0.9)
    pyautogui.click(button_location)
    time.sleep(3)
    pyperclip.copy(filename2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(7)
    pyautogui.press('enter')
    time.sleep(5)
    button_location = pyautogui.locateOnScreen('./template/exit_button.png', confidence=0.9)
    pyautogui.click(button_location)
    return 


# %%
def issue_engine():
    pyautogui.click(615, 573)
    time.sleep(3)
    pyautogui.click(717, 167)
    time.sleep(2)
    pyautogui.press('backspace', presses=5)
    pyautogui.write('06.218.02%', interval= 0.2)
    pyautogui.press('enter', presses=2)
    time.sleep(3)
    pyautogui.click(986, 567)
    time.sleep(2)
    pyautogui.click(994, 122)
    time.sleep(5)
    pyautogui.click(727, 169)
    pyautogui.press('backspace', presses=5)
    pyautogui.write('R153%')
    pyautogui.press('enter', presses=2)
    time.sleep(2)
    button_location = pyautogui.locateOnScreen('./template/show_button.png', confidence=0.7)
    pyautogui.click(button_location)
    time.sleep(3)
    pyautogui.click(202, 272)
    time.sleep(2)
    pyautogui.press('end')
    pyautogui.press('backspace', presses=15)
    time.sleep(2)
    pyautogui.typewrite(from_dt_str, 0.2)
    time.sleep(2)
    pyautogui.click(508, 627)
    time.sleep(2)
    pyautogui.click(910, 641)
    time.sleep(2)
    pyautogui.press('d', presses=4, interval=0.5)
    pyautogui.press('enter')
    time.sleep(3)
    button_location = pyautogui.locateOnScreen('./template/print_button.png', confidence=0.9)
    pyautogui.click(button_location)
    time.sleep(3)
    pyperclip.copy(filename3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(10)
    pyautogui.press('enter')
    time.sleep(5)
    button_location = pyautogui.locateOnScreen('./template/exit_button.png', confidence=0.9)
    pyautogui.click(button_location)
    return 

def run_all():
    issue_engine()
    time.sleep(2)
    grn_engine()
    time.sleep(2)
    purchase_order()

# %%

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--select', type=str, help='Condition to execute specific function')
args = parser.parse_args()
function_map = {
        'ISSUE': issue_engine,
        'GRN': grn_engine,
        'PUR': purchase_order
    }

# Start the application using the redacted path
os.startfile(ERP_SHORTCUT_PATH)
time.sleep(3)

window = focus_lighthouse_window()
pyautogui.PAUSE = 0.5

if window:
    print("window found and executing")
    login_gui()
    time.sleep(5)
    if args.select:
        function_map[args.select]()
    else:
        run_all()
    # Quit Application
    pyautogui.keyDown('ctrl')
    pyautogui.press('q')
    pyautogui.keyUp('ctrl')