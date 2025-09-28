# estoque.py
from typing import List
from medicamento import Medicamento
from classe_farmaco import ClasseFarmaco

class Estoque:
    def __init__(self):
        self._lista: List[Medicamento] = []

    def adicionar(self, med: Medicamento):
        if any(m.codigo == med.codigo for m in self._lista):
            raise ValueError(f"Medicamento com código '{med.codigo}' já existe no estoque.")
        self._lista.append(med)

    def listar(self) -> List[Medicamento]:
        return list(self._lista)

    def buscar_por_nome(self, nome: str) -> List[Medicamento]:
        termo = nome.lower().strip()
        return [
            m for m in self._lista
            if termo in m.nome_comercial.lower() or termo in m.nome_generico.lower()
        ]

    def buscar_por_classe(self, classe: ClasseFarmaco) -> List[Medicamento]:
        return [m for m in self._lista if m.classe == classe]

    def excluir(self, codigo: str) -> bool:
        for i, m in enumerate(self._lista):
            if m.codigo == codigo:
                del self._lista[i]
                return True
        return False

    def editar(self, codigo: str, **kwargs) -> bool:
        for m in self._lista:
            if m.codigo == codigo:
                if "nome_comercial" in kwargs:
                    m.alterar_nome_comercial(kwargs["nome_comercial"])
                if "nome_generico" in kwargs:
                    m.alterar_nome_generico(kwargs["nome_generico"])
                if "via_administracao" in kwargs:
                    m.alterar_via_administracao(kwargs["via_administracao"])
                if "validade" in kwargs:
                    m.alterar_validade(kwargs["validade"])
                if "classe" in kwargs:
                    nova_classe = kwargs["classe"]
                    if not isinstance(nova_classe, ClasseFarmaco):
                        raise ValueError("Classe inválida para medicamento.")
                    m._classe = nova_classe
                return True
        return False
