import curses
import cv2
import time
from PhotoHandler.PhotoHandler import PhotoHandler

class VideoHandler:
    def __init__(self, colors=False):
        self.colors = colors
        self.paused = False
        self.currFrame = 0

    def handleVideo(self, file):
        curses.wrapper(self._handleVideo, file)

    def _handleVideo(self, stdscr, file):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        cap = cv2.VideoCapture(file)
        if not cap.isOpened():
            stdscr.addstr(0, 0, "Errore nell'apertura del file video.")
            stdscr.refresh()
            time.sleep(2)
            return

        framerate = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        handler = PhotoHandler(self.colors)
        skipFrame = 1

        while self.currFrame < frames:
            try:
                key = stdscr.getch()
            except:
                key = -1

            if key == ord('q'):
                break
            elif key == ord(' '):
                self.paused = not self.paused
            elif key == curses.KEY_RIGHT:
                self.paused = True
                self.currFrame = min(self.currFrame + framerate * 5, frames - 1)
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.currFrame)
            elif key == curses.KEY_LEFT:
                self.paused = True
                self.currFrame = max(self.currFrame - framerate * 5, 0)
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.currFrame)

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

            max_y, max_x = stdscr.getmaxyx()
            ascii_output = handler.handlePhoto(file=None, frame=frame, use_curses=True, x=max_x, y=max_y)
            ascii_lines = ascii_output.splitlines()

            stdscr.clear()

            for idx, line in enumerate(ascii_lines):
                if idx >= max_y - 2:
                    break
                stdscr.addstr(idx, 0, line[:max_x-1])

            # Barra di avanzamento
            progress_width = min(handler.finalMediaWidth, max_x - 2)
            progress_chars = int((self.currFrame / frames) * progress_width)
            bar = '[' + ('#' * progress_chars).ljust(progress_width) + ']'
            stdscr.addstr(min(len(ascii_lines), max_y - 2), 0, bar)

            stdscr.refresh()

            timeEnd = time.time()
            timeElapsed = timeEnd - timeStart
            timeToWait = 1 / framerate - timeElapsed
            if timeToWait > 0:
                time.sleep(timeToWait)
                skipFrame = 1
            else:
                skipFrame = int(1 + (-timeToWait * framerate))

        cap.release()
        cv2.destroyAllWindows()
