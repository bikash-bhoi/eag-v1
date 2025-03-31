import pyautogui
import win32gui
import time

# Get the handle of the Paint window
def get_paint_window():
    def callback(hwnd, extra):
        if "Paint" in win32gui.GetWindowText(hwnd):
            extra.append(hwnd)

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

# Get window position
hwnd = get_paint_window()
if hwnd:
    rect = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)
    print(f"Paint Window Coordinates: {rect}")

    # Wait for a click and get its position
    print("Click anywhere in the Paint window...")
    time.sleep(5)

    x, y = pyautogui.position()
    print(f"Mouse Click at: ({x}, {y}) relative to screen")

    # Convert to relative coordinates inside the Paint window
    rel_x, rel_y = x - rect[0], y - rect[1]
    print(f"Relative to Paint: ({rel_x}, {rel_y})")
else:
    print("Paint window not found!")
