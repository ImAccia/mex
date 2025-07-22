import math
import cv2
import numpy as np
import shutil
import os

class PhotoHandler:
    def __init__(self, colors=False):
        self.colors = colors
        self.cursed = False

        # Lista codici ansi per colori console
        self.colorsToAnsi = {
            'nero': '\033[30m',
            'rosso': '\033[31m',
            'verde': '\033[32m',
            'giallo': '\033[33m',
            'blu': '\033[34m',
            'magenta': '\033[35m',
            'ciano': '\033[36m',
            'bianco': '\033[37m',
            'reset': '\033[0m'
        }

        # Colori di riferimento (nome, valore BGR)
        self.colorsToPixel = {
            "nero": (-100, -100, -100),
            "rosso": (0, 0, 255),
            "verde": (0, 255, 0),
            "giallo": (0, 255, 255),
            "blu": (255, 0, 0),
            "magenta": (255, 0, 255),
            "ciano": (255, 255, 0),
            "bianco": (255, 255, 255)
        }

        self.charset = "·`'\".-:!~^*+<>io?vc)(}{JYXZOMW#@"

        self.finalMediaWidth = 0
        self.finalMediaHeight = 0
        self.consoleW = 0
        self.consoleH = 0
        self.calculateMediaSize = True

    def handlePhoto(self, file, frame=False, use_curses=False, x=False, y=False):
        self.cursed = use_curses
        if file:
            img = cv2.imread(file)
        else:
            img = frame

        if not use_curses:
            term_w, term_h = shutil.get_terminal_size((80, 24))
            ascii_str = self.getAscii(img, term_w, term_h)
            os.system('cls' if (os.name == 'nt' and not self.cursed) else 'clear')
            print(("\033[H" if (os.name == 'nt' and not self.cursed) else '') + ascii_str)
        else:
            # In modalità curses, restituisco la stringa
            return self.getAscii(img, x, y)

    def getAscii(self, frame, term_w, term_h):
        if self.consoleW != term_w or self.consoleH != term_h:
            self.consoleW = term_w
            self.consoleH = term_h
            self.calculateMediaSize = True

        if self.calculateMediaSize:
            imgHeight, imgWidth = frame.shape[:2]
            newWidth = term_w
            newHeight = int(imgHeight * newWidth / imgWidth)

            if newHeight > (term_h * 2) - 5:
                newHeight = (term_h * 2) - 5
                newWidth = int(imgWidth * newHeight / imgHeight)

            self.finalMediaWidth = newWidth
            self.finalMediaHeight = newHeight
            self.calculateMediaSize = False

        frame = cv2.resize(frame, (self.finalMediaWidth, self.finalMediaHeight))

        if not self.colors or self.cursed:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ascii_lines = []
        for y in range(0, self.finalMediaHeight - 1, 2):
            line = ""
            for x in range(self.finalMediaWidth):
                pixel = frame[y, x]
                pixelY2 = frame[y + 1, x]
                avg = (np.float32(pixel) + np.float32(pixelY2)) / 2

                if self.colors and not self.cursed:
                    # Trova il colore più vicino
                    ansiIdx = self.findColor(avg)
                    color = self.colorsToAnsi[ansiIdx]
                    index = int((avg[0] + avg[1] + avg[2]) / 3 / 510 * len(self.charset))
                else:
                    color = ''
                    index = int(avg / 510 * len(self.charset))

                char = color + self.charset[min(index, len(self.charset) - 1)]
                line += char
            ascii_lines.append(line)

        return '\n'.join(ascii_lines) + (self.colorsToAnsi['reset'] if (os.name == 'nt' and not self.cursed) else '') 

    def euclideanDistance(self, colore1, colore2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(colore1, colore2)))

    def findColor(self, pixel):
        colore_prossimo = min(
            self.colorsToPixel,
            key=lambda nome: self.euclideanDistance(pixel, self.colorsToPixel[nome])
        )
        return colore_prossimo
