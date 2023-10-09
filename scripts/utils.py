"""Utility functions for the application."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QIcon

def change_icon_color(icon: QIcon, color: QColor) -> QIcon:
    pixmap = icon.pixmap(icon.availableSizes()[0])
    mask = pixmap.createMaskFromColor(QColor(0, 0, 0, 255), Qt.MaskMode.MaskOutColor)
    
    painter = QPainter(pixmap)
    painter.setPen(QColor(0, 0, 0, 0))
    painter.setBrush(color)
    painter.drawRect(pixmap.rect())
    
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
    painter.drawPixmap(pixmap.rect(), mask, mask.rect())
    painter.end()
    
    return QIcon(pixmap)
