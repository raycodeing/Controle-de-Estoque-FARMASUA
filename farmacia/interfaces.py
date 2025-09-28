# interfaces.py
from typing import Protocol, Iterable
from medicamento import Medicamento
from classe_farmaco import ClasseFarmaco

class IEstoqueLeitura(Protocol):
    def listar(self) -> Iterable[Medicamento]:
        ...

    def buscar_por_nome(self, nome: str) -> list[Medicamento]:
        ...

    def buscar_por_classe(self, classe: ClasseFarmaco) -> list[Medicamento]:
        ...

class IEstoque(IEstoqueLeitura, Protocol):
    def adicionar(self, med: Medicamento):
        ...

    def editar(self, codigo: str, **kwargs) -> bool:
        ...

    def excluir(self, codigo: str) -> bool:
        ...
