# notificacao.py
from PyQt5.QtWidgets import QMessageBox, QWidget

def notificar_sucesso(parent: QWidget, mensagem: str):
    QMessageBox.information(parent, "Sucesso", mensagem)

def notificar_erros(parent: QWidget, mensagem: str):
    QMessageBox.warning(parent, "Erro", mensagem)

def confirmar(parent: QWidget, mensagem: str) -> bool:
    resp = QMessageBox.question(parent, "Confirmar", mensagem, QMessageBox.Yes | QMessageBox.No)
    return resp == QMessageBox.Yes
