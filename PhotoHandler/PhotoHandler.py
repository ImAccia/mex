import math

class PhotoHandler:
    def __init__(self, colors = False):
        self.colors = colors

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

        # Colori di riferimento (nome, valore RGB)
        self.colorsToPixel = {
            "nero": (-150, -150, -150),
            "rosso": (255, 0, 0),
            "verde": (0, 255, 0),
            "giallo": (255, 255, 0),
            "blu": (0, 0, 255),
            "magenta": (255, 0, 255),
            "ciano": (0, 255, 255),
            "bianco": (255, 255, 255)
        }

    def handlePhoto(self, file, frame = False, colors = False):
        # Prendo la larghezza e l'altezza della console
        import os
        import cv2

        rows, columns = os.popen('stty size', 'r').read().split()

        # Prendo la larghezza e l'altezza dell'immagine con cv2
        if file:
            img = cv2.imread(file)
        else:
            img = frame
        imgHeight, imgWidth = img.shape[:2]

        charset = "·`'\".-:!~^*+<>io?vc)(}{JYXZOMW#@"

        # Mantengo l'aspect ratio dell'immagine e la ridimensiono in base all'altezza della console
        newHeight = int(rows)
        newWidth = int(imgWidth * newHeight / imgHeight)
        
        # Ridimensiono l'immagine
        img = cv2.resize(img, (newWidth, newHeight))

        if not self.colors:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Converto l'immagine in ASCII e la stampo a schermo
        toPrint = ''
        for y in range(0, newHeight - 1, 2):
            for x in range(newWidth):
                pixel = img[y, x]
                pixelY2 = img[y + 1, x]
                avg = (pixel + pixelY2) / 2

                if self.colors:
                    # Trova il colore più vicino
                    ansiIdx = self.findColor(avg)
                    color = self.colorsToAnsi[ansiIdx]
                    index = int((avg[0] + avg[1] + avg[2]) / 3 / 255 * len(charset))
                else:
                    color = ''
                    index = int(avg / 255 * len(charset))

                toPrint += color + charset[index]
            toPrint += '\n'

        # Stampo l'immagine a schermo sovrascrivendo il contenuto precedente, senza cancellarlo
        print("\033[H" + toPrint + self.colorsToAnsi['reset'])

    # Funzione per calcolare la distanza Euclidea
    def euclideanDistance(self, colore1, colore2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(colore1, colore2)))

    # Funzione per trovare il colore più vicino
    def findColor(self, pixel):
        colore_prossimo = min(self.colorsToPixel, key=lambda nome: self.euclideanDistance(pixel, self.colorsToPixel[nome]))
        return colore_prossimo
