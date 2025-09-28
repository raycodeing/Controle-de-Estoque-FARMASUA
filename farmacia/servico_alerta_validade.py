# servico_alerta_validade.py
from PyQt5.QtWidgets import QWidget, QMessageBox
from estoque import Estoque

class AlertaValidadeService:
    def __init__(self, estoque: Estoque, parent_ui: QWidget, meses_alerta: int = 6):
        self.estoque = estoque
        self.parent_ui = parent_ui
        self.meses_alerta = meses_alerta

    def verificar_alertas(self):
        meds_alerta = []
        for m in self.estoque.listar():
            if m.esta_proximo_vencimento(self.meses_alerta):
                meds_alerta.append(m)
        return meds_alerta

    def mostrar_alertas(self):
        meds_alerta = self.verificar_alertas()
        for m in meds_alerta:
            QMessageBox.warning(
                self.parent_ui,
                "Atenção",
                f"Medicamento '{m.nome_comercial}' está a {self.meses_alerta} meses ou menos do vencimento "
                f"({m.validade.strftime('%d/%m/%Y')})"
            )
