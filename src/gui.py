from __future__ import annotations

import sys
from typing import List, Any

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDoubleSpinBox,
    QMessageBox,
    QTabWidget,
)
from PySide6.QtCore import Qt

from src.services import gestor_tareas, gestor_presupuestos
from src.services import gestor_inventario


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Gestor TPA")
        self.resize(900, 600)

        # ---------- CONTENEDOR PRINCIPAL ----------
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Encabezado
        header = QVBoxLayout()
        title = QLabel("Gestor TPA")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Tareas · Presupuestos · Inventario (conceptual)")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)

        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Crear pestañas
        self._build_tareas_tab()
        self._build_presupuestos_tab()
        self._build_inventario_tab()

        # Estilo general
        self._apply_style()
    # ------------------------------------------------------------------
    #                           ESTILO GLOBAL
    # ------------------------------------------------------------------
    def _apply_style(self) -> None:
        self.setStyleSheet(
        """
        /* ----- VENTANA PRINCIPAL ----- */
        QMainWindow {
            background-color: #fafafa;
        }

        QLabel {
            color: #1c1c1e;
            font-size: 13px;
        }

        /* ----- TÍTULOS ----- */
        QLabel#titleLabel {
            font-size: 28px;
            font-weight: 800;
            color: #111;
        }

        QLabel#subtitleLabel {
            font-size: 15px;
            color: #555;
        }

        /* ----- TABS ----- */
        QTabWidget::pane {
            border: 1px solid #d0d0d0;
            border-radius: 10px;
            background: #ffffff;
        }

        QTabBar::tab {
            padding: 10px 20px;
            background: #e9e9ec;
            color: #333;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 3px;
            font-size: 14px;
        }

        QTabBar::tab:selected {
            background: #ffffff;
            color: #000;
            font-weight: bold;
            border-bottom: 2px solid #007aff;
        }

        /* ----- TABLA (ESTILO MACOS SONOMA) ----- */
        QTableWidget {
            background: #ffffff;
            alternate-background-color: #f2f2f7;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            gridline-color: #e0e0e0;
            selection-background-color: #007aff;
            selection-color: #ffffff;
            color: #000000;
            font-size: 14px;
        }

        QHeaderView::section {
            background: #f7f7f9;
            color: #1c1c1e;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #d0d0d0;
            font-size: 13px;
            font-weight: 600;
        }

        QTableWidget::item {
            padding: 6px;
            color: #000000;
        }

        QTableWidget::item:hover {
            background: #e8f0ff;
            color: #000000;
        }

        /* ----- BOTONES ----- */
        QPushButton {
            background-color: #007aff;
            color: #ffffff;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 14px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #0a84ff;
            color: #ffffff;
        }

        QPushButton:pressed {
            background-color: #0060df;
            color: #ffffff;
        }

        QPushButton:disabled {
            background-color: #b5b5b8;
            color: #f2f2f2;
        }

        /* ----- CAMPOS DE TEXTO (actualizados con mejor legibilidad) ----- */
        QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
            background: #1c1c1e;       /* gris oscuro macOS */
            color: #ffffff;            /* texto blanco */
            border: 1px solid #3a3a3c; /* borde macOS */
            border-radius: 6px;
            padding: 6px;
            font-size: 13px;
        }

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #007aff;
            outline: none;
        }

        /* ----- MESSAGE BOX FIX (dark icons → light text) ----- */
        QMessageBox {
            background-color: #ffffff;
            color: #000000;
        }
        QMessageBox QLabel {
            color: #000000;
            font-size: 14px;
        }
        QMessageBox QPushButton {
            background-color: #007aff;
            color: #ffffff;
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 13px;
        }
        """
    )
    # ------------------------------------------------------------------
    #                           TAREAS
    # ------------------------------------------------------------------
    def _build_tareas_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Botonera superior
        btn_row = QHBoxLayout()
        self.btn_add_tarea = QPushButton("Añadir tarea")
        self.btn_completar_tarea = QPushButton("Marcar como completada")
        self.btn_eliminar_tarea = QPushButton("Eliminar tarea")

        self.btn_add_tarea.clicked.connect(self._on_add_tarea)
        self.btn_completar_tarea.clicked.connect(self._on_completar_tarea)
        self.btn_eliminar_tarea.clicked.connect(self._on_eliminar_tarea)

        btn_row.addWidget(self.btn_add_tarea)
        btn_row.addWidget(self.btn_completar_tarea)
        btn_row.addWidget(self.btn_eliminar_tarea)
        btn_row.addStretch()

        layout.addLayout(btn_row)

        # Tabla
        self.tbl_tareas = QTableWidget()
        self.tbl_tareas.setAlternatingRowColors(True)
        self.tbl_tareas.setColumnCount(4)
        self.tbl_tareas.setHorizontalHeaderLabels(["ID", "Título", "Prioridad", "Completada"])

        header = self.tbl_tareas.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tbl_tareas)

        self.tabs.addTab(tab, "Tareas")
        self._load_tareas()

    def _load_tareas(self) -> None:
        tareas = gestor_tareas.listar_tareas()
        self.tbl_tareas.setRowCount(len(tareas))

        for row, t in enumerate(tareas):
            self.tbl_tareas.setItem(row, 0, QTableWidgetItem(str(t.id)))
            self.tbl_tareas.setItem(row, 1, QTableWidgetItem(t.titulo))
            self.tbl_tareas.setItem(row, 2, QTableWidgetItem(t.prioridad))
            self.tbl_tareas.setItem(row, 3, QTableWidgetItem("Sí" if t.completada else "No"))

    def _on_add_tarea(self) -> None:
        dlg = TareaDialog(self)
        if dlg.exec() == QDialog.Accepted:
            data = dlg.get_data()
            gestor_tareas.agregar_tarea(
                data["titulo"],
                data["descripcion"],
                data["prioridad"],
            )
            self._load_tareas()

    def _on_completar_tarea(self) -> None:
        row = self.tbl_tareas.currentRow()
        if row < 0:
            QMessageBox.information(self, "Tareas", "Selecciona una tarea.")
            return
        tarea_id_item = self.tbl_tareas.item(row, 0)
        tarea_id = int(tarea_id_item.text())
        ok = gestor_tareas.marcar_completada(tarea_id)
        if not ok:
            QMessageBox.warning(self, "Tareas", "No se pudo marcar como completada.")
        self._load_tareas()

    def _on_eliminar_tarea(self) -> None:
        row = self.tbl_tareas.currentRow()
        if row < 0:
            QMessageBox.information(self, "Tareas", "Selecciona una tarea.")
            return
        tarea_id_item = self.tbl_tareas.item(row, 0)
        tarea_id = int(tarea_id_item.text())
        ok = gestor_tareas.eliminar_tarea(tarea_id)
        if not ok:
            QMessageBox.warning(self, "Tareas", "No se pudo eliminar la tarea.")
        self._load_tareas()
    # ------------------------------------------------------------------
    #                      PRESUPUESTOS
    # ------------------------------------------------------------------
    def _build_presupuestos_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        btn_row = QHBoxLayout()
        self.btn_add_presu = QPushButton("Añadir presupuesto")
        self.btn_delete_presu = QPushButton("Eliminar presupuesto")

        self.btn_add_presu.clicked.connect(self._on_add_presupuesto)
        self.btn_delete_presu.clicked.connect(self._on_delete_presupuesto)

        btn_row.addWidget(self.btn_add_presu)
        btn_row.addWidget(self.btn_delete_presu)
        btn_row.addStretch()

        layout.addLayout(btn_row)

        self.tbl_presu = QTableWidget()
        self.tbl_presu.setAlternatingRowColors(True)
        self.tbl_presu.setColumnCount(4)
        self.tbl_presu.setHorizontalHeaderLabels(["ID", "Concepto", "Monto", "Tipo"])

        header = self.tbl_presu.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tbl_presu)

        self.tabs.addTab(tab, "Presupuestos")
        self._load_presupuestos()

    def _load_presupuestos(self) -> None:
        datos: List[Any] = gestor_presupuestos.listar_presupuestos()
        self.tbl_presu.setRowCount(len(datos))

        for row, p in enumerate(datos):
            # Puede ser tupla o un objeto
            try:
                pid, concepto, monto, tipo = p.id, p.concepto, p.monto, p.tipo
            except AttributeError:
                pid, concepto, monto, tipo = p

            self.tbl_presu.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.tbl_presu.setItem(row, 1, QTableWidgetItem(str(concepto)))
            self.tbl_presu.setItem(row, 2, QTableWidgetItem(str(monto)))
            self.tbl_presu.setItem(row, 3, QTableWidgetItem(str(tipo)))

    def _on_add_presupuesto(self) -> None:
        dlg = PresupuestoDialog(self)
        if dlg.exec() == QDialog.Accepted:
            data = dlg.get_data()
            gestor_presupuestos.agregar_presupuesto(
                data["concepto"],
                data["monto"],
                data["tipo"],
            )
            self._load_presupuestos()

    def _on_delete_presupuesto(self) -> None:
        row = self.tbl_presu.currentRow()
        if row < 0:
            QMessageBox.information(self, "Presupuestos", "Selecciona un presupuesto.")
            return

        presu_id_item = self.tbl_presu.item(row, 0)
        presu_id = int(presu_id_item.text())

        try:
            ok = gestor_presupuestos.eliminar_presupuesto(presu_id)
        except AttributeError:
            QMessageBox.warning(
                self,
                "Presupuestos",
                "La eliminación no está implementada en gestor_presupuestos.",
            )
            return

        if not ok:
            QMessageBox.warning(self, "Presupuestos", "No se pudo eliminar.")
        self._load_presupuestos()

    # ------------------------------------------------------------------
    #                      INVENTARIO (CONCEPTUAL)
    # ------------------------------------------------------------------
    def _build_inventario_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Botonera superior
        btn_row = QHBoxLayout()
        self.btn_add_item = QPushButton("Añadir item")
        self.btn_update_item = QPushButton("Actualizar cantidad")
        self.btn_delete_item = QPushButton("Eliminar item")

        self.btn_add_item.clicked.connect(self._on_add_item)
        self.btn_update_item.clicked.connect(self._on_update_item)
        self.btn_delete_item.clicked.connect(self._on_delete_item)

        btn_row.addWidget(self.btn_add_item)
        btn_row.addWidget(self.btn_update_item)
        btn_row.addWidget(self.btn_delete_item)
        btn_row.addStretch()

        layout.addLayout(btn_row)

        # Tabla de inventario
        self.tbl_inv = QTableWidget()
        self.tbl_inv.setAlternatingRowColors(True)
        self.tbl_inv.setColumnCount(5)
        self.tbl_inv.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Precio", "Total"])

        header = self.tbl_inv.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tbl_inv)

        self.tabs.addTab(tab, "Inventario")
        self._load_inventario()

    def _load_inventario(self) -> None:
        datos = gestor_inventario.listar_inventario()
        self.tbl_inv.setRowCount(len(datos))

        for row, item in enumerate(datos):
            iid, nombre, cantidad, precio = item
            total = round(cantidad * precio, 2)

            self.tbl_inv.setItem(row, 0, QTableWidgetItem(str(iid)))
            self.tbl_inv.setItem(row, 1, QTableWidgetItem(str(nombre)))
            self.tbl_inv.setItem(row, 2, QTableWidgetItem(str(cantidad)))
            self.tbl_inv.setItem(row, 3, QTableWidgetItem(f"{precio:.2f}"))
            self.tbl_inv.setItem(row, 4, QTableWidgetItem(f"{total:.2f}"))

    def _on_add_item(self) -> None:
        dlg = InventarioDialog(self)
        if dlg.exec() == QDialog.Accepted:
            data = dlg.get_data()
            gestor_inventario.agregar_item(
                data["nombre"], data["cantidad"], data["precio"]
            )
            self._load_inventario()

    def _on_update_item(self) -> None:
        row = self.tbl_inv.currentRow()
        if row < 0:
            QMessageBox.information(self, "Inventario", "Selecciona un item.")
            return

        item_id = int(self.tbl_inv.item(row, 0).text())
        cantidad_actual = int(self.tbl_inv.item(row, 2).text())

        dlg = UpdateCantidadDialog(self, cantidad_actual)
        if dlg.exec() == QDialog.Accepted:
            nueva_cantidad = dlg.get_cantidad()
            gestor_inventario.actualizar_cantidad(item_id, nueva_cantidad)
            self._load_inventario()

    def _on_delete_item(self) -> None:
        row = self.tbl_inv.currentRow()
        if row < 0:
            QMessageBox.information(self, "Inventario", "Selecciona un item.")
            return

        item_id = int(self.tbl_inv.item(row, 0).text())
        ok = gestor_inventario.eliminar_item(item_id)

        if not ok:
            QMessageBox.warning(self, "Inventario", "No se pudo eliminar.")
        self._load_inventario()
# ----------------------------------------------------------------------
#                    DIÁLOGOS MODALES
# ----------------------------------------------------------------------
class TareaDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Nueva tarea")
        self.setModal(True)
        self.resize(400, 260)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit, QTextEdit, QComboBox {
                background: #ffffff;
                color: #000000;
                border: 1px solid #c9c9c9;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #007aff;
                color: #ffffff;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)

        lbl_titulo = QLabel("Título")
        self.edit_titulo = QLineEdit()

        lbl_desc = QLabel("Descripción")
        self.edit_desc = QTextEdit()
        self.edit_desc.setFixedHeight(80)

        lbl_prio = QLabel("Prioridad")
        self.combo_prio = QComboBox()
        self.combo_prio.addItems(["alta", "media", "baja"])
        self.combo_prio.setCurrentText("media")

        layout.addWidget(lbl_titulo)
        layout.addWidget(self.edit_titulo)
        layout.addWidget(lbl_desc)
        layout.addWidget(self.edit_desc)
        layout.addWidget(lbl_prio)
        layout.addWidget(self.combo_prio)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)

        layout.addLayout(btn_row)

    def get_data(self) -> dict:
        return {
            "titulo": self.edit_titulo.text().strip(),
            "descripcion": self.edit_desc.toPlainText().strip(),
            "prioridad": self.combo_prio.currentText(),
        }


class PresupuestoDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Nuevo presupuesto")
        self.setModal(True)
        self.resize(400, 260)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
                background: #ffffff;
                color: #000000;
                border: 1px solid #c9c9c9;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #007aff;
                color: #ffffff;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)

        lbl_concepto = QLabel("Concepto")
        self.edit_concepto = QLineEdit()

        lbl_monto = QLabel("Monto (€)")
        self.spin_monto = QDoubleSpinBox()
        self.spin_monto.setDecimals(2)
        self.spin_monto.setMinimum(0.0)
        self.spin_monto.setMaximum(10_000_000.0)
        self.spin_monto.setValue(0.0)

        lbl_tipo = QLabel("Tipo")
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["ingreso", "gasto"])
        
        layout.addWidget(lbl_concepto)
        layout.addWidget(self.edit_concepto)
        layout.addWidget(lbl_monto)
        layout.addWidget(self.spin_monto)
        layout.addWidget(lbl_tipo)
        layout.addWidget(self.combo_tipo)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)

        layout.addLayout(btn_row)

    def get_data(self) -> dict:
        return {
            "concepto": self.edit_concepto.text().strip(),
            "monto": float(self.spin_monto.value()),
            "tipo": self.combo_tipo.currentText(),
        }


# ----------------------------------------------------------------------
#                    INVENTARIO DIALOGS
# ----------------------------------------------------------------------
class InventarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir item")
        self.setModal(True)
        self.resize(400, 260)
        self.setStyleSheet(parent.styleSheet())

        layout = QVBoxLayout(self)

        lbl_nombre = QLabel("Nombre")
        self.edit_nombre = QLineEdit()

        lbl_cantidad = QLabel("Cantidad")
        self.spin_cantidad = QDoubleSpinBox()
        self.spin_cantidad.setDecimals(0)
        self.spin_cantidad.setMinimum(0)
        self.spin_cantidad.setMaximum(1_000_000)

        lbl_precio = QLabel("Precio (€)")
        self.spin_precio = QDoubleSpinBox()
        self.spin_precio.setDecimals(2)
        self.spin_precio.setMinimum(0.0)
        self.spin_precio.setMaximum(1_000_000.0)

        layout.addWidget(lbl_nombre)
        layout.addWidget(self.edit_nombre)
        layout.addWidget(lbl_cantidad)
        layout.addWidget(self.spin_cantidad)
        layout.addWidget(lbl_precio)
        layout.addWidget(self.spin_precio)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)

        layout.addLayout(btn_row)

    def get_data(self) -> dict:
        return {
            "nombre": self.edit_nombre.text().strip(),
            "cantidad": int(self.spin_cantidad.value()),
            "precio": float(self.spin_precio.value())
        }


class UpdateCantidadDialog(QDialog):
    def __init__(self, parent=None, cantidad_actual=0):
        super().__init__(parent)
        self.setWindowTitle("Actualizar cantidad")
        self.setModal(True)
        self.resize(300, 180)
        self.setStyleSheet(parent.styleSheet())

        layout = QVBoxLayout(self)

        lbl = QLabel("Nueva cantidad")
        self.spin_cantidad = QDoubleSpinBox()
        self.spin_cantidad.setDecimals(0)
        self.spin_cantidad.setMinimum(0)
        self.spin_cantidad.setMaximum(1_000_000)
        self.spin_cantidad.setValue(cantidad_actual)

        layout.addWidget(lbl)
        layout.addWidget(self.spin_cantidad)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)

        layout.addLayout(btn_row)

    def get_cantidad(self) -> int:
        return int(self.spin_cantidad.value())


# ----------------------------------------------------------------------
#                           MAIN
# ----------------------------------------------------------------------
def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

