# main_gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QHeaderView, QFileDialog
)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush
from PyQt5.QtCore import Qt, QDate, QTimer, QSize

from medicamento import Medicamento
from estoque import Estoque
from classe_farmaco import ClasseFarmaco
from notificacao import notificar_sucesso, notificar_erros, confirmar
from servico_alerta_validade import AlertaValidadeService


CLASSES_MEDICAMENTO = {cf.value: cf for cf in ClasseFarmaco}
VIAS = list(Medicamento.VIAS_PERMITIDAS)


class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.estoque = Estoque()
        self.setWindowTitle("Controle de Estoque de Medicamentos")
        self.resize(950, 750)

        try:
            with open("styles/estilo.qss", "r", encoding="utf-8") as f:
                estilo = f.read()
                self.setStyleSheet(estilo)
        except Exception as e:
            print("Não foi possível carregar estilo:", e)

        self.alerta_service = AlertaValidadeService(self.estoque, parent_ui=self, meses_alerta=6)

        self.init_ui()

        self.timer_alerta = QTimer(self)
        self.timer_alerta.setInterval(60 * 1000)  # checa validade a cada minuto
        self.timer_alerta.timeout.connect(self.alerta_service.mostrar_alertas)
        self.timer_alerta.start()

    def init_ui(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        form_layout = QGridLayout()
        button_layout = QHBoxLayout()
        search_layout = QHBoxLayout()
        table_layout = QVBoxLayout()

        self.label_logo = QLabel()
        self.label_logo.setFixedSize(120, 120)
        try:
            pix = QPixmap("resources/logo3.jpeg")
            pix = pix.scaled(self.label_logo.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_logo.setPixmap(pix)
        except Exception as e:
            print("Não foi possível carregar logo:", e)
        top_layout.addWidget(self.label_logo)
        top_layout.addStretch()

        self.input_codigo = QLineEdit()
        self.input_codigo.setObjectName("inputCodigo")
        self.input_nome_comercial = QLineEdit()
        self.input_nome_comercial.setObjectName("inputNomeComercial")
        self.input_nome_genérico = QLineEdit()
        self.input_nome_genérico.setObjectName("inputNomeGenerico")

        self.combo_classe = QComboBox()
        self.combo_classe.setObjectName("comboClasse")
        for nome in CLASSES_MEDICAMENTO.keys():
            self.combo_classe.addItem(nome)

        self.combo_via = QComboBox()
        self.combo_via.setObjectName("comboVia")
        for via in VIAS:
            self.combo_via.addItem(via)

        self.date_validade = QDateEdit()
        self.date_validade.setObjectName("dateValidade")
        self.date_validade.setCalendarPopup(True)
        self.date_validade.setDisplayFormat("dd/MM/yyyy")
        self.date_validade.setDate(QDate.currentDate())

        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Pesquisar por nome...")
        self.input_search.setObjectName("inputSearch")
        self.combo_search_classe = QComboBox()
        self.combo_search_classe.setObjectName("comboSearchClasse")
        self.combo_search_classe.addItem("Todas as classes")
        for nome in CLASSES_MEDICAMENTO.keys():
            self.combo_search_classe.addItem(nome)

        # montar o layout de formulário
        form_layout.addWidget(QLabel("Código:"), 0, 0)
        form_layout.addWidget(self.input_codigo, 0, 1)
        form_layout.addWidget(QLabel("Nome Comercial:"), 1, 0)
        form_layout.addWidget(self.input_nome_comercial, 1, 1)
        form_layout.addWidget(QLabel("Nome Genérico:"), 2, 0)
        form_layout.addWidget(self.input_nome_genérico, 2, 1)
        form_layout.addWidget(QLabel("Classe:"), 3, 0)
        form_layout.addWidget(self.combo_classe, 3, 1)
        form_layout.addWidget(QLabel("Via Administração:"), 4, 0)
        form_layout.addWidget(self.combo_via, 4, 1)
        form_layout.addWidget(QLabel("Validade:"), 5, 0)
        form_layout.addWidget(self.date_validade, 5, 1)

        btn_cadastrar = QPushButton("Cadastrar")
        btn_cadastrar.setObjectName("btnCadastrar")
        btn_cadastrar.clicked.connect(self.cadastrar_medicamento)

        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.setObjectName("btnAtualizar")
        btn_atualizar.clicked.connect(self.atualizar_dados_do_formulario)

        btn_limpar = QPushButton("Limpar Campos")
        btn_limpar.setObjectName("btnLimpar")
        btn_limpar.clicked.connect(self.limpar_formulario)

        button_layout.addWidget(btn_cadastrar)
        button_layout.addWidget(btn_atualizar)
        button_layout.addWidget(btn_limpar)
        button_layout.addStretch()

        btn_search = QPushButton("")
        btn_search.setObjectName("btnPesquisar")
        btn_search.setIcon(QIcon("resources/pesquisar.svg"))
        btn_search.setIconSize(QSize(20, 20))
        btn_search.clicked.connect(self.pesquisar)

        btn_imprimir = QPushButton("")
        btn_imprimir.setObjectName("btnImprimir")
        btn_imprimir.setIcon(QIcon("resources/imprimir.svg"))
        btn_imprimir.setIconSize(QSize(20, 20))
        btn_imprimir.clicked.connect(self.imprimir_listagem)

        search_layout.addWidget(self.input_search)
        search_layout.addWidget(self.combo_search_classe)
        search_layout.addWidget(btn_search)
        search_layout.addWidget(btn_imprimir)
        search_layout.addStretch()

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels([
            "Código", "Nome Comercial", "Nome Genérico",
            "Classe", "Via", "Validade", "Editar", "Excluir"
        ])
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        table_layout.addWidget(self.tabela)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)

    def cadastrar_medicamento(self):
        try:
            codigo = self.input_codigo.text().strip()
            nome_com = self.input_nome_comercial.text().strip()
            nome_gen = self.input_nome_genérico.text().strip()
            classe_nome = self.combo_classe.currentText()
            via = self.combo_via.currentText()
            validade_qdate = self.date_validade.date()
            validade = validade_qdate.toPyDate()

            if not codigo or not nome_com or not nome_gen:
                notificar_erros(self, "Por favor, preencha todos os campos obrigatórios.")
                return

            classe_enum = CLASSES_MEDICAMENTO.get(classe_nome)
            if classe_enum is None:
                notificar_erros(self, "Classe de medicamento inválida.")
                return

            med = Medicamento(codigo, nome_com, nome_gen, via, validade, classe_enum)
            self.estoque.adicionar(med)
            self.atualizar_tabela(self.estoque.listar())
            notificar_sucesso(self, "Medicamento cadastrado com sucesso.")
            self.limpar_formulario()

        except Exception as e:
            notificar_erros(self, str(e))

    def atualizar_dados_do_formulario(self):
        codigo = self.input_codigo.text().strip()
        if not codigo:
            notificar_erros(self, "Código é necessário para atualizar.")
            return
        nome_com = self.input_nome_comercial.text().strip()
        nome_gen = self.input_nome_genérico.text().strip()
        via = self.combo_via.currentText()
        validade_qdate = self.date_validade.date()
        validade = validade_qdate.toPyDate()
        classe_nome = self.combo_classe.currentText()

        if not nome_com or not nome_gen:
            notificar_erros(self, "Preencha todos os campos obrigatórios para edição.")
            return

        classe_enum = CLASSES_MEDICAMENTO.get(classe_nome)
        if classe_enum is None:
            notificar_erros(self, "Classe de medicamento inválida.")
            return

        try:
            sucesso = self.estoque.editar(
                codigo,
                nome_comercial=nome_com,
                nome_generico=nome_gen,
                via_administracao=via,
                validade=validade,
                classe=classe_enum
            )
            if sucesso:
                notificar_sucesso(self, "Medicamento atualizado com sucesso.")
                self.atualizar_tabela(self.estoque.listar())
                self.limpar_formulario()
            else:
                notificar_erros(self, "Não foi possível atualizar. Verifique se o código existe.")
        except Exception as e:
            notificar_erros(self, str(e))

    def editar_linha(self, row: int):
        codigo_item = self.tabela.item(row, 0)
        nome_com_item = self.tabela.item(row, 1)
        nome_gen_item = self.tabela.item(row, 2)
        classe_item = self.tabela.item(row, 3)
        via_item = self.tabela.item(row, 4)
        validade_item = self.tabela.item(row, 5)

        if not all([codigo_item, nome_com_item, nome_gen_item, classe_item, via_item, validade_item]):
            return

        codigo = codigo_item.text()
        nome_com = nome_com_item.text()
        nome_gen = nome_gen_item.text()
        classe_nome = classe_item.text()
        via = via_item.text()
        validade_qdate = QDate.fromString(validade_item.text(), "dd/MM/yyyy")

        self.input_codigo.setText(codigo)
        self.input_nome_comercial.setText(nome_com)
        self.input_nome_genérico.setText(nome_gen)
        idx_classe = self.combo_classe.findText(classe_nome)
        if idx_classe >= 0:
            self.combo_classe.setCurrentIndex(idx_classe)
        idx_via = self.combo_via.findText(via)
        if idx_via >= 0:
            self.combo_via.setCurrentIndex(idx_via)
        self.date_validade.setDate(validade_qdate)

    def excluir_linha(self, row: int):
        codigo_item = self.tabela.item(row, 0)
        if not codigo_item:
            return
        codigo = codigo_item.text()
        if confirmar(self, f"Tem certeza que deseja excluir o medicamento '{codigo}'?"):
            sucesso = self.estoque.excluir(codigo)
            if sucesso:
                notificar_sucesso(self, "Medicamento excluído com sucesso.")
                self.atualizar_tabela(self.estoque.listar())
            else:
                notificar_erros(self, "Erro ao excluir: código não encontrado.")

    def pesquisar(self):
        termo = self.input_search.text().strip()
        classe_nome = self.combo_search_classe.currentText()

        lista = self.estoque.listar()

        if termo:
            lista = self.estoque.buscar_por_nome(termo)

        if classe_nome != "Todas as classes":
            classe_enum = CLASSES_MEDICAMENTO.get(classe_nome)
            if classe_enum:
                lista = self.estoque.buscar_por_classe(classe_enum)

        self.atualizar_tabela(lista)

    def atualizar_tabela(self, lista_meds):
        self.tabela.setRowCount(0)

        cores = {
            ClasseFarmaco.ANALGESICO: QColor("#F5E981"),
            ClasseFarmaco.ANTIBIOTICO: QColor("#73FAFA"),
            ClasseFarmaco.ANTIINFLAMATORIO: QColor("#FFCEC8"),
            ClasseFarmaco.ANTIDEPRESSIVO: QColor("#A7A7FF"),
            ClasseFarmaco.ANSIOLITICO: QColor("#9FFF9F"),
            ClasseFarmaco.BENZODIAZEPINICO: QColor("#FFFF9C"),
            ClasseFarmaco.ANTIEMETICO: QColor("#FFB4CD"),
            ClasseFarmaco.HIPOGLICEMIANTE: QColor("#A0D3FF"),
            ClasseFarmaco.ANTIHIPERTENSIVO: QColor("#FFFFA0"),
            ClasseFarmaco.OPIODE: QColor("#FFB7B7"),
            ClasseFarmaco.ANTICOAGULANTE: QColor("#FDDA9A"),
            ClasseFarmaco.ESTATINA: QColor("#FCD89E"),
            ClasseFarmaco.BRONCODILADOR: QColor("#ABFFAB"),
            ClasseFarmaco.ANTIHISTAMINICO: QColor("#FFC28D"),
        }

        for med in lista_meds:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, QTableWidgetItem(med.codigo))
            self.tabela.setItem(row, 1, QTableWidgetItem(med.nome_comercial))
            self.tabela.setItem(row, 2, QTableWidgetItem(med.nome_generico))
            self.tabela.setItem(row, 3, QTableWidgetItem(med.classe.value))
            self.tabela.setItem(row, 4, QTableWidgetItem(med.via_administracao))
            self.tabela.setItem(row, 5, QTableWidgetItem(med.validade.strftime("%d/%m/%Y")))

            cor_fundo = cores.get(med.classe, QColor("white"))
            for col in range(6):
                item = self.tabela.item(row, col)
                if item:
                    item.setBackground(QBrush(cor_fundo))

            btn_editar = QPushButton("Editar")
            btn_editar.setObjectName(f"btnEditarLinha_{row}")
            btn_editar.clicked.connect(lambda _, r=row: self.editar_linha(r))

            btn_excluir = QPushButton("Excluir")
            btn_excluir.setObjectName(f"btnExcluirLinha_{row}")
            btn_excluir.clicked.connect(lambda _, r=row: self.excluir_linha(r))

            self.tabela.setCellWidget(row, 6, btn_editar)
            self.tabela.setCellWidget(row, 7, btn_excluir)

        self.alerta_service.mostrar_alertas()

    def limpar_formulario(self):
        self.input_codigo.clear()
        self.input_nome_comercial.clear()
        self.input_nome_genérico.clear()
        self.combo_classe.setCurrentIndex(0)
        self.combo_via.setCurrentIndex(0)
        self.date_validade.setDate(QDate.currentDate())

    def imprimir_listagem(self):
        path, _ = QFileDialog.getSaveFileName(self, "Salvar listagem", "", "Arquivo de texto (*.txt)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("Código;Nome Comercial;Nome Genérico;Classe;Via;Validade\n")
                    for row in range(self.tabela.rowCount()):
                        campos = []
                        for col in range(6):
                            item = self.tabela.item(row, col)
                            campos.append(item.text() if item else "")
                        f.write(";".join(campos) + "\n")
                notificar_sucesso(self, "Listagem salva com sucesso.")
            except Exception as e:
                notificar_erros(self, f"Erro ao salvar listagem: {e}")


def main():
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
