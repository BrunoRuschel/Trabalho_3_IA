from typing import Iterable, Set, Tuple


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """

    def __init__(self, estado: str, pai: "Nodo", acao: str, custo: int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __eq__(self, other):
        """Dois nodos são iguais se seus estados são iguais."""
        return self.estado == other.estado and isinstance(other, Nodo)

    def __hash__(self):
        """Retorna o hash do estado do nodo."""
        return hash(self.estado)


def sucessor(estado: str) -> Set[Tuple[str, str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    actions: Set[Tuple[str, str]] = set()

    for i, caractere in enumerate(estado):
        if caractere == "_":
            if (i % 3) < 2:  # posições 0,1,3,4,6,7
                novo_estado = list(estado)
                novo_estado[i], novo_estado[i + 1] = novo_estado[i + 1], novo_estado[i]
                actions.add(("direita", "".join(novo_estado)))
            if (i % 3) > 0:  # posições 1,2,4,5,7,8
                novo_estado = list(estado)
                novo_estado[i], novo_estado[i - 1] = novo_estado[i - 1], novo_estado[i]
                actions.add(("esquerda", "".join(novo_estado)))
            if i <= 5:  # posições 0,1,2,3,4,5
                novo_estado = list(estado)
                novo_estado[i], novo_estado[i + 3] = novo_estado[i + 3], novo_estado[i]
                actions.add(("abaixo", "".join(novo_estado)))
            if i >= 3:  # posições 3,4,5,6,7,8
                novo_estado = list(estado)
                novo_estado[i], novo_estado[i - 3] = novo_estado[i - 3], novo_estado[i]
                actions.add(("acima", "".join(novo_estado)))
    return actions


def expande(nodo: Nodo) -> Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    sucessores = sucessor(nodo.estado)
    nodos_sucessores = set()

    for acao, novo_estado in sucessores:
        nodo_nodo = Nodo(
            estado=novo_estado,
            pai=nodo,
            acao=acao,
            custo=nodo.custo + 1,
        )
        nodos_sucessores.add(nodo_nodo)
    return nodos_sucessores


def astar_hamming(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_manhattan(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


# opcional,extra
def bfs(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


# opcional,extra
def dfs(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


# opcional,extra
def astar_new_heuristic(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
