import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF


def load_styles() -> str:
    with open("style.css", "r", encoding="utf-8") as file:
        return file.read()


class SchemaWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.flow = 50
        self.diam = 4
        self.col_height = 0.5

    def update_params(self, flow, diam, col_height):
        self.flow = flow
        self.diam = diam
        self.col_height = col_height
        self.update()

    def _draw_arrow_head(self, painter, x, y, direction, size=6):
        """Рисует наконечник размерной стрелки"""
        if direction == "up":
            pts = [QPointF(x, y), QPointF(x - size / 2, y + size), QPointF(x + size / 2, y + size)]
        elif direction == "down":
            pts = [QPointF(x, y), QPointF(x - size / 2, y - size), QPointF(x + size / 2, y - size)]
        painter.setBrush(QBrush(QColor("#f1c40f")))
        painter.drawPolygon(QPolygonF(pts))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()


        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#262730"), 2))
        painter.drawRoundedRect(0, 0, w, h, 12, 12)


        painter.setPen(QColor("#8b949e"))
        painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
        painter.drawText(25, 28, "СХЕМА ПАРАМЕТРОВ ЛИНИИ")

        base_y = h - 30


        col_x = int(w * 0.08)
        col_w = 56
        col_h = 135
        col_y = base_y - col_h

        painter.setBrush(QBrush(QColor("#238636")))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(col_x, col_y, col_w, col_h, 4, 4)

        painter.setPen(QPen(QColor("#3fb950"), 2.5))
        painter.drawLine(col_x, base_y, col_x, col_y)
        painter.drawLine(col_x, col_y, col_x + col_w, col_y)
        painter.drawLine(col_x + col_w, col_y, col_x + col_w, base_y)


        painter.save()
        painter.translate(col_x + col_w / 2 + 4, col_y + col_h / 2)
        painter.rotate(-90)
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(QRectF(-55, -12, 110, 24), Qt.AlignCenter, "КОЛОННА")
        painter.restore()


        dim_x = col_x + col_w + 18
        painter.setPen(QPen(QColor("#f1c40f"), 2))
        painter.drawLine(dim_x - 6, col_y, dim_x + 6, col_y)
        painter.drawLine(dim_x - 6, base_y, dim_x + 6, base_y)
        painter.drawLine(dim_x, col_y + 2, dim_x, base_y - 2)
        self._draw_arrow_head(painter, dim_x, col_y, "up")
        self._draw_arrow_head(painter, dim_x, base_y, "down")


        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        painter.drawText(dim_x + 12, int((col_y + base_y) / 2 + 5), f"H = {self.col_height} м")


        mid_x = int(w * 0.48)


        line_w = 210
        painter.setPen(QPen(QColor("#c9d1d9"), 2.5))
        painter.drawLine(mid_x - line_w // 2, base_y, mid_x + line_w // 2, base_y)


        box_w, box_h = 58, 38
        box1_x = mid_x - 75
        box2_x = mid_x + 18
        box_y = base_y - box_h - 3

        for bx in (box1_x, box2_x):
            painter.setBrush(QBrush(QColor("#1f6feb")))
            painter.setPen(QPen(QColor("#58a6ff"), 2))
            painter.drawRoundedRect(bx, box_y, box_w, box_h, 4, 4)


        nozzle_w = 22
        nozzle_x = box1_x + (box_w - nozzle_w) // 2
        nozzle_top = col_y
        nozzle_bottom = box_y - 16

        painter.setBrush(QBrush(QColor("#388bfd")))
        painter.setPen(Qt.NoPen)
        painter.drawRect(nozzle_x, nozzle_top, nozzle_w, nozzle_bottom - nozzle_top)

        painter.setPen(QPen(QColor("#79c0ff"), 2.5))
        painter.drawLine(nozzle_x, nozzle_top, nozzle_x, nozzle_bottom)
        painter.drawLine(nozzle_x + nozzle_w, nozzle_top, nozzle_x + nozzle_w, nozzle_bottom)


        arrow_x = nozzle_x + nozzle_w + 14
        painter.setPen(QPen(QColor("#f1c40f"), 2))
        painter.drawLine(arrow_x, nozzle_top + 6, arrow_x, nozzle_bottom - 2)
        self._draw_arrow_head(painter, arrow_x, nozzle_bottom, "down")

        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        painter.drawText(arrow_x + 10, int((nozzle_top + nozzle_bottom) / 2 + 5), f"V = {self.flow} л/ч")


        right_x = int(w * 0.80)
        pipe_w = 120
        pipe_h = 34
        pipe_center_y = int((col_y + base_y) / 2)
        pipe_top = pipe_center_y - pipe_h // 2
        pipe_bottom = pipe_center_y + pipe_h // 2

        painter.setBrush(QBrush(QColor("#388bfd")))
        painter.setPen(Qt.NoPen)
        painter.drawRect(right_x, pipe_top, pipe_w, pipe_h)

        painter.setPen(QPen(QColor("#79c0ff"), 2.5))
        painter.drawLine(right_x, pipe_top, right_x + pipe_w, pipe_top)
        painter.drawLine(right_x, pipe_bottom, right_x + pipe_w, pipe_bottom)

        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(
            QRectF(right_x, pipe_top, pipe_w, pipe_h),
            Qt.AlignCenter,
            "ТРУБА"
        )


        d_arrow_x = right_x - 16
        painter.setPen(QPen(QColor("#f1c40f"), 2))
        painter.drawLine(d_arrow_x - 6, pipe_top, d_arrow_x + 6, pipe_top)
        painter.drawLine(d_arrow_x - 6, pipe_bottom, d_arrow_x + 6, pipe_bottom)
        painter.drawLine(d_arrow_x, pipe_top + 2, d_arrow_x, pipe_bottom - 2)
        self._draw_arrow_head(painter, d_arrow_x, pipe_top, "up", size=5)
        self._draw_arrow_head(painter, d_arrow_x, pipe_bottom, "down", size=5)


        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        painter.drawText(
            QRectF(d_arrow_x - 140, pipe_center_y - 14, 128, 28),
            Qt.AlignRight | Qt.AlignVCenter,
            f"d = {self.diam} мм"
        )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, check_one_, check_two_, check_three_):
        super().__init__()

        self.check_one = check_one_
        self.check_two = check_two_
        self.check_three = check_three_

        uic.loadUi("main.ui", self)
        self.setStyleSheet(load_styles())

        schema_layout = QtWidgets.QVBoxLayout(self.schema_placeholder)
        schema_layout.setContentsMargins(0, 0, 0, 0)
        self.schema = SchemaWidget()
        schema_layout.addWidget(self.schema)

        self.slider_1.setRange(50, 1000)
        self.slider_1.setValue(50)

        self.slider_2.setRange(4, 20)
        self.slider_2.setValue(4)

        self.slider_3.setRange(5, 50)
        self.slider_3.setValue(5)

        self.slider_1.valueChanged.connect(self.on_params_changed)
        self.slider_2.valueChanged.connect(self.on_params_changed)
        self.slider_3.valueChanged.connect(self.on_params_changed)
        self.on_params_changed()

        self.set_status("wait", "ОЖИДАНИЕ РАСЧЕТА")
        self.btn_calc.clicked.connect(self.calculate)

    def set_status(self, state, text):
        self.label_status.setText(text)
        self.label_status.setProperty("status", state)
        self.label_status.style().unpolish(self.label_status)
        self.label_status.style().polish(self.label_status)

    def on_params_changed(self):
        flow = self.slider_1.value()
        diam = self.slider_2.value()
        col_h = round(self.slider_3.value() / 10.0, 1)

        self.label_1.setText(f"Расход: {flow} л/ч")
        self.label_2.setText(f"Диаметр трубки: {diam} мм")
        self.label_3.setText(f"Высота колонны: {col_h} м")

        self.schema.update_params(flow, diam, col_h)

    def calculate(self):
        flow = self.slider_1.value() / (3.6 * 10 ** 6)
        diam = self.slider_2.value() / 1000.0
        col_h = round(self.slider_3.value() / 10.0, 1)

        pressure = self.check_one(diam, col_h, 6, flow)
        saturation = self.check_two(flow, diam)
        min_level = self.check_three(flow)

        a = []
        b = []
        if pressure >= 0.4:
            a.append(2)
            b.append(f"Насос выдержит")
        elif pressure < 0.4 and pressure >= 0.1:
            a.append(1)
            b.append(f"")
        else:
            a.append(0)
            b.append(f"")

        if saturation >= 96:
            a.append(2)
            b.append(f"")
        elif saturation < 96 and saturation >= 90:
            a.append(1)
            b.append(f"")
        else:
            a.append(0)
            b.append(f"")

        #0.08 М

        if min_level <= 0.04:
            a.append(2)
            b.append(f"")
        elif min_level > 0.04 and min_level <= 0.07:
            a.append(1)
            b.append(f"")
        else:
            a.append(0)
            b.append(f"")

        can_work = min(a)

        if can_work == 2:
            self.set_status("green", "ПАРАМЕТРЫ В НОРМЕ")
        elif can_work == 0:
            self.set_status("yellow", "ЕСТЬ РИСК")
        else:
            self.set_status("red", "РАБОТАТЬ НЕЛЬЗЯ")



        self.label_main_res.setText(f"Насыщение газом: % — ГОДИТСЯ")
        self.label_details.setText(
            f"Остаточное давление в норме: {pressure[1]} бар (запас достаточный)\n"
            f"Минимальный уровень жидкости в баке розлива что бы не было пены: {min_level} м"
        )

        #
        # if pressure[0]:
        #     self.set_status("green", "ПАРАМЕТРЫ В НОРМЕ")
        #     self.label_main_res.setText(f"Насыщение газом: % — ГОДИТСЯ")
        #     self.label_details.setText(
        #         f"Остаточное давление в норме: {pressure[1]} бар (запас достаточный)\n"
        #         f"Минимальный уровень жидкости в баке розлива что бы не было пены: {min_level} м"
        #     )
        # else:
        #     self.set_status("red", "СИСТЕМА НЕРАБОТОСПОСОБНА")
        #     self.label_main_res.setText(f"Насыщение газом: % — ГОДИТСЯ")
        #     self.label_details.setText(
        #         f"Давление не в норме: не хватает {-(pressure[1])} бар нужно поставить более мощные насосы\n"
        #         f"Первый брак: {0} литра (слить перед пуском)"
        #     )


        # if col_h >= 1.5 and diam >= 10 and flow <= 400:
        #     self.set_status("green", "ЗЕЛЕНЫЙ — ПАРАМЕТРЫ В НОРМЕ")
        #     self.label_main_res.setText("Насыщение газом: 96% — ГОДИТСЯ")
        #     self.label_details.setText(
        #         f"Остаточное давление в норме: {pressure} бар (запас достаточный)\n"
        #         f"Первый брак: {brack_volume} литра (слить перед пуском)"
        #     )
        # elif col_h >= 0.5 and diam >= 4:
        #     self.set_status("yellow", "ЖЕЛТЫЙ — ЕСТЬ РИСК")
        #     self.label_main_res.setText("Насыщение газом: 78% — ДОПУСТИМО")
        #     self.label_details.setText(
        #         f"Остаточное давление: {pressure} бар (на грани).\n"
        #         f"Первый брак: {brack_volume} литра (слить в канализацию)."
        #     )
        # else:
        #     self.set_status("red", "КРАСНЫЙ — СИСТЕМА НЕРАБОТОСПОСОБНА")





