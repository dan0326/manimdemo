import re
from manimlib import *

def copy_frame_positioning(self):
    frame = self.frame
    center = frame.get_center()
    height = frame.get_height()
    angles = frame.get_euler_angles()
    call = f"reorient("
    theta, phi, gamma = (angles / DEG).astype(int)
    call += f"{theta}, {phi}, {gamma}"
    call += f", {tuple(np.round(center, 2))}"
    call += ", {:.2f}".format(height)
    call += ")"
    pattern = r"np\.float32\(([^)]+)\)"
    call = re.sub(pattern, r"\1", call) # use regex to remove np.flaot()
    pyperclip.copy(call)