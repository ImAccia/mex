import threading
import keyboard
import time
import cv2
from PhotoHandler.PhotoHandler import PhotoHandler

class VideoHandler:
    def __init__(self, colors = False):
        self.colors = colors
        self.paused = False
        self.currFrame = 0

    def handleVideo(self, file):
        # Prendo la larghezza e l'altezza della console

        # Prendo la larghezza e l'altezza del video
        cap = cv2.VideoCapture(file)
        framerate = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        handler = PhotoHandler(self.colors)

        # Converto il video in ASCII
        skipFrame = 1

        # Lancio un thread per la gestione del video, per metterlo in pausa e/o andare avanti o indietro
        vidMngr = threading.Thread(target=self.videoManager, args=(cap, frames, framerate))
        vidMngr.start()

        while self.currFrame < frames:
            self.currFrame += 1
            i = self.currFrame
            
            while self.paused:
                print('', end='\r')
                time.sleep(0.1)
            # Leggo il frame in scala di grigi
            ret, frame = cap.read()

            if not ret:
                break

            # Salto i frame se necessario
            if skipFrame > 1 and i % skipFrame != 0:
                continue

            timeStart = time.time()
            handler.handlePhoto(False, frame, False)
            timeEnd = time.time()

            # Calcolo il tempo impiegato per processare il frame
            timeElapsed = timeEnd - timeStart
            timeToWait = 1 / framerate - timeElapsed

            # Attendo il tempo necessario per mantenere il framerate
            if timeToWait > 0:
                time.sleep(timeToWait)
            else:
                rapporto = 1 + (-timeToWait * framerate)
                if rapporto > 1:
                    skipFrame = int(rapporto)
                else:
                    skipFrame = 1

            #mostro una barra di avanzamento del video, che occupa tutta la larghezza della console
            progress = int((i / frames) * handler.finalMediaWidth) 
            print('[' + ('#' * progress) + (' ' * (handler.finalMediaWidth - progress - 2)) + ']')

        cap.release()
        cv2.destroyAllWindows()
        vidMngr.join()

    def videoManager(self, cap, frames, framerate):
        while cap.isOpened():
            time.sleep(0.2)

            if keyboard.is_pressed('space'):
                self.paused = True
            else:
                if keyboard.is_pressed('right'):
                    self.paused = True
                    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    new_frame = min(current_frame + framerate * 5, frames - 1)
                    self.currFrame = new_frame
                    cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
                    self.paused = False
                else:
                    if keyboard.is_pressed('left'):
                        self.paused = True
                        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                        new_frame = max(current_frame - framerate * 5, 0)
                        self.currFrame = new_frame
                        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
                        self.paused = False
            
            print('', end='\r')

            while self.paused:
                print('', end='\r')
                time.sleep(0.2)
                if keyboard.is_pressed('space'):
                    self.paused = False
                    break


