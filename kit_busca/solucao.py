from typing import Iterable, Set, Tuple
import heapq

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

    def __lt__(self, other):
        # necessário porque heapq compara dois nodos se f é igual para mais de um nodo, na hora de
        # inserir na fila de prioridades,
        return self.custo < other.custo  # desempata pelo custo real


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


def distancia_hamming(estado: str) -> int:
    objetivo = "12345678_"
    distancia = 0
    for i in range(len(objetivo)):
        if objetivo[i] != estado[i] and estado[i] != "_":
            distancia += 1
    return distancia


def reconstruir_caminho(nodo: Nodo) -> list[str]:
    """reconstrói o caminho de ações do nó objetivo até o nó raiz"""
    caminho = []

    if nodo.pai is None:
        return None

    while nodo.pai is not None:
        caminho.append(nodo.acao)
        nodo = nodo.pai
    return caminho[::-1]  # inverte o caminho


def astar_hamming(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    explorados = set()
    fronteira = []
    heapq.heappush(fronteira, (0, Nodo(estado, None, None, 0)))

    while True:
        if not fronteira:
            return None
        _, v = heapq.heappop(fronteira)

        if v.estado == "12345678_":  # objetivo
            return reconstruir_caminho(v)

        if v not in explorados:
            explorados.add(v)
            sucessores = expande(v)
            for nodo_sucessor in sucessores:
                g = nodo_sucessor.custo
                h = distancia_hamming(nodo_sucessor.estado)
                f = g + h
                heapq.heappush(fronteira, (f, nodo_sucessor))


def manhattan(estado: str) -> int:
    """
    Calcula a soma das distâncias de Manhattan de todas as peças do estado.
    A distância Manhattan é a soma das distâncias verticais e horizontais
    de cada peça até a posição correta.
    """

    objetivo = "12345678_"
    return sum(
        abs(i // 3 - objetivo.index(char) // 3) + abs(i % 3 - objetivo.index(char) % 3)
        for i, char in enumerate(estado) if char != '_'
    )

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
    objetivo = "12345678_"

    if estado == objetivo:
        return []

    fronteira = []
    estados_explorados = set()
    heapq.heappush(fronteira, (manhattan(estado), Nodo(estado, None, None, 0)))

    while fronteira:
        _, nodo_atual = heapq.heappop(fronteira)

        if nodo_atual.estado in estados_explorados:
            continue
        estados_explorados.add(nodo_atual.estado)

        if nodo_atual.estado == objetivo:
            caminho = []
            while nodo_atual.pai is not None:
                caminho.insert(0, nodo_atual.acao)
                nodo_atual = nodo_atual.pai
            return caminho

        for acao, estado_sucessor in sucessor(nodo_atual.estado):
            if estado_sucessor not in estados_explorados:
                custo = nodo_atual.custo + 1
                nodo_sucessor = Nodo(estado_sucessor, nodo_atual, acao, custo)
                f = custo + manhattan(estado_sucessor)
                heapq.heappush(fronteira, (f, nodo_sucessor))

    return None


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
