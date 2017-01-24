import os
import time
import msvcrt
from datetime import datetime
import pyscreenshot as ImageGrab


class ScreenShotter(object):

    def __init__(self, delay_in_seconds = 0.1, folder = r'C:\Documents'):
        self.delay_in_seconds = delay_in_seconds
        self.folder = folder
        if not os.path.isdir(self.folder):
            os.makedirs(self.folder)
        self.time_of_last_single_press = None
        self.time_of_last_double_press = None
    # have to screenshot and get key input

    # have to be able to detect number of key-presses in the last x seconds

    def screenshot_to_file(self, fname):
        ImageGrab.grab_to_file(os.path.join(*[self.folder, fname]))


    def get_seconds_since_single_press(self):
        return datetime.now().time() - self.time_of_last_single_press


    def get_seconds_since_double_press(self):
        return datetime.now().time() - self.time_of_last_double_press


    def run_screenshotter(self):
        file_counter = 0
        while True:
            with open(os.path.join([self.folder, 'data.txt'])) as txt_file:
                fname = 'screenshot_%s.png' % str(file_counter).zfill(4)
                try:
                    if msvcrt.kbhit() and msvcrt.getch() == 'SPACEBAR': #not sure of actual equality element
                        self.time_of_last_single_press = datetime.now().time()
                    self.screenshot_to_file(fname)
                    txt_file.write(self.get_seconds_since_single_press())
                    txt_file.write(self.get_seconds_since_double_press())
                    time.sleep(self.delay_in_seconds)
                except KeyboardInterrupt:
                    print('ending screenshotter...')
                    break

    # need to get some keystroke value here
    def get_keystroke_status(self):
        pass