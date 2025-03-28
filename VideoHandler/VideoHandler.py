class VideoHandler:
    def __init__(self, colors = False):
        self.colors = colors

    def handleVideo(self, file):
        # Prendo la larghezza e l'altezza della console
        import cv2
        import time
        from PhotoHandler.PhotoHandler import PhotoHandler

        # Prendo la larghezza e l'altezza del video
        cap = cv2.VideoCapture(file)
        framerate = int(cap.get(cv2.CAP_PROP_FPS))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        handler = PhotoHandler(self.colors)

        # Converto il video in ASCII
        for i in range(frames):
            # Leggo il frame in scala di grigi
            ret, frame = cap.read()

            if not ret:
                break

            timeStart = time.time()
            handler.handlePhoto(False, frame, False)
            timeEnd = time.time()

            # Calcolo il tempo impiegato per processare il frame
            timeElapsed = timeEnd - timeStart
            timeToWait = 1 / framerate - timeElapsed

            # Attendo il tempo necessario per mantenere il framerate
            if timeToWait > 0:
                time.sleep(timeToWait)

        cap.release()
            

