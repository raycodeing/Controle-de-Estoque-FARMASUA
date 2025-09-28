# medicamento.py
from datetime import date
from classe_farmaco import ClasseFarmaco

class Medicamento:
    VIAS_PERMITIDAS = {
        "Oral", "Sublingual", "Retal",
        "Subcutânea", "Intramuscular", "Intravenosa"
    }

    def __init__(
        self,
        codigo: str,
        nome_comercial: str,
        nome_generico: str,
        via_administracao: str,
        validade: date,
        classe: ClasseFarmaco
    ):
        if not codigo or not codigo.strip():
            raise ValueError("Código não pode estar vazio.")
        if not nome_comercial or not nome_comercial.strip():
            raise ValueError("Nome comercial não pode estar vazio.")
        if not nome_generico or not nome_generico.strip():
            raise ValueError("Nome genérico não pode estar vazio.")
        via = via_administracao.strip()
        if via not in Medicamento.VIAS_PERMITIDAS:
            raise ValueError(f"Via de administração inválida: {via}. Permitidas: {Medicamento.VIAS_PERMITIDAS}")
        if not isinstance(validade, date):
            raise ValueError("Validade deve ser uma data.")
        if not isinstance(classe, ClasseFarmaco):
            raise ValueError("Classe de medicamento inválida.")

        self._codigo = codigo.strip()
        self._nome_comercial = nome_comercial.strip()
        self._nome_generico = nome_generico.strip()
        self._via_administracao = via
        self._validade = validade
        self._classe = classe

    # propriedades de leitura
    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nome_comercial(self) -> str:
        return self._nome_comercial

    @property
    def nome_generico(self) -> str:
        return self._nome_generico

    @property
    def via_administracao(self) -> str:
        return self._via_administracao

    @property
    def validade(self) -> date:
        return self._validade

    @property
    def classe(self) -> ClasseFarmaco:
        return self._classe

    # métodos de alteração 
    def alterar_nome_comercial(self, novo_nome: str):
        if not novo_nome or not novo_nome.strip():
            raise ValueError("Nome comercial não pode estar vazio.")
        self._nome_comercial = novo_nome.strip()

    def alterar_nome_generico(self, novo_nome: str):
        if not novo_nome or not novo_nome.strip():
            raise ValueError("Nome genérico não pode estar vazio.")
        self._nome_generico = novo_nome.strip()

    def alterar_via_administracao(self, nova_via: str):
        via = nova_via.strip()
        if via not in Medicamento.VIAS_PERMITIDAS:
            raise ValueError(f"Via inválida: {via}. Permitidas: {Medicamento.VIAS_PERMITIDAS}")
        self._via_administracao = via

    def alterar_validade(self, nova_validade: date):
        if not isinstance(nova_validade, date):
            raise ValueError("Validade deve ser uma data.")
        self._validade = nova_validade

    def esta_proximo_vencimento(self, meses: int = 6) -> bool:
        hoje = date.today()
        if self._validade <= hoje:
            return False
        delta_meses = (self._validade.year - hoje.year) * 12 + (self._validade.month - hoje.month)
        return delta_meses <= meses

    def __str__(self):
        return (f"{self.codigo} - {self.nome_comercial} ({self.nome_generico}), "
                f"{self.via_administracao}, validade: {self.validade.strftime('%d/%m/%Y')}, "
                f"classe: {self.classe.value}")
