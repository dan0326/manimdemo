from manimlib import *

def copy_frame_positioning(self):
    frame = self.frame
    center = frame.get_center()
    height = frame.get_height()
    angles = frame.get_euler_angles()
    call = f"reorient("
    theta, phi, gamma = (angles / DEG).astype(int)
    call += f"{theta}, {phi}, {gamma}"
    if any(center != 0):
        call += f", {tuple(np.round(center, 2))}"
    if height != FRAME_HEIGHT:
        call += ", {:.2f}".format(height)
    call += ")"
    pyperclip.copy(call)