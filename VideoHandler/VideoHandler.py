from pynput import keyboard as kb
import threading
import time
import cv2
from PhotoHandler.PhotoHandler import PhotoHandler

class VideoHandler:
    def __init__(self, colors=False):
        self.colors = colors
        self.paused = False
        self.currFrame = 0
        self.lastKey = None
        self.keyLock = threading.Lock()

    def handleVideo(self, file):
        cap = cv2.VideoCapture(file)
        framerate = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        handler = PhotoHandler(self.colors)

        # Thread listener dei tasti
        key_thread = threading.Thread(target=self.keyListener)
        key_thread.daemon = True
        key_thread.start()

        skipFrame = 1

        while self.currFrame < frames:
            with self.keyLock:
                key = self.lastKey
                self.lastKey = None  # Reset

            if key == 'space':
                self.paused = not self.paused
            elif key == 'right':
                self.currFrame = min(self.currFrame + framerate * 5, frames - 1)
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.currFrame)
                self.paused = False
            elif key == 'left':
                self.currFrame = max(self.currFrame - framerate * 5, 0)
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.currFrame)
                self.paused = False

            if self.paused:
                time.sleep(0.1)
                continue

            ret, frame = cap.read()
            if not ret:
                break

            self.currFrame += 1
            if skipFrame > 1 and self.currFrame % skipFrame != 0:
                continue

            timeStart = time.time()
            handler.handlePhoto(False, frame, False)
            timeEnd = time.time()

            timeElapsed = timeEnd - timeStart
            timeToWait = 1 / framerate - timeElapsed
            skipFrame = int(1 + (-timeToWait * framerate)) if timeToWait < 0 else 1
            if timeToWait > 0:
                time.sleep(timeToWait)

            progress = int((self.currFrame / frames) * handler.finalMediaWidth)
            print('[' + ('#' * progress) + (' ' * (handler.finalMediaWidth - progress - 2)) + ']', end='\r')

        cap.release()
        cv2.destroyAllWindows()

    def keyListener(self):
        def on_press(key):
            try:
                k = key.char
            except AttributeError:
                k = key.name  # arrows, space, etc.
            with self.keyLock:
                if k in ['space', 'left', 'right']:
                    self.lastKey = k

        with kb.Listener(on_press=on_press) as listener:
            listener.join()
