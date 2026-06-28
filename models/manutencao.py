from datetime import date

TIPOS_VALIDOS = {"preventiva", "corretiva"}


class Manutencao:
    _proximo_id = 1

    def __init__(self, data: date, tipo: str, pecasTrocadas: str,
                 custoTotal: float, kmDaManutencao: float, oficina) -> None:
        if tipo.lower() not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido: {tipo!r}. Use: {sorted(TIPOS_VALIDOS)}.")
        if custoTotal < 0:
            raise ValueError("O custo total não pode ser negativo.")
        if kmDaManutencao < 0:
            raise ValueError("A quilometragem não pode ser negativa.")

        self.__id = Manutencao._proximo_id
        Manutencao._proximo_id += 1
        self.__data = data
        self.__tipo = tipo.lower()
        self.__pecasTrocadas = pecasTrocadas
        self.__custoTotal = custoTotal
        self.__kmDaManutencao = kmDaManutencao
        self.__oficina = oficina

    @property
    def id(self):
        return self.__id

    @property
    def custoTotal(self):
        # O Dashboard precisa ler este valor para o RF06
        return self.__custoTotal
    
    @property
    def tipo(self):
        return self.__tipo

    @property
    def kmDaManutencao(self):
        return self.__kmDaManutencao

    def __repr__(self):
        return f"Manutencao(ID: {self.__id}, Tipo: {self.__tipo}, Custo: R${self.__custoTotal})"