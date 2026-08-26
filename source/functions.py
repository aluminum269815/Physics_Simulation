import os
from PyQt5.QtGui import QPixmap, QBitmap, QRegion

def load_image(path):
    full_path = os.path.abspath('./assets/' + path)
    pixmap = QPixmap(full_path)

    image = pixmap.toImage()
    mask = QBitmap.fromImage(image.createAlphaMask())
    region = QRegion(mask)
    rect = region.boundingRect()

    if rect.isValid() and not rect.isEmpty():
        pixmap = pixmap.copy(rect)

    return pixmap
