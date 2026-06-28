from datetime import date


class Abastecimento:
    _proximo_id = 1 # atributo contador (indice), PROTECTED

    def __init__(self, data: date, tipoCombustivel: str, litros: float,
                 valorTotal: float, kmNoMomento: float, motorista) -> None:
        if litros <= 0:
            raise ValueError("A quantidade de litros deve ser maior que zero.")
        if valorTotal < 0:
            raise ValueError("O valor total não pode ser negativo.")

        self.__id = Abastecimento._proximo_id
        Abastecimento._proximo_id += 1
        self.__data = data
        self.__tipoCombustivel = tipoCombustivel
        self.__litros = litros
        self.__valorTotal = valorTotal
        self.__kmNoMomento = kmNoMomento
        self.__motorista = motorista

    @property
    def valorTotal(self):
        # Permite que o Dashboard leia o valor para calcular o Custo por Km
        return self.__valorTotal

    @property
    def kmNoMomento(self):
        # Permite que o Veículo leia o km do abastecimento para atualizar o hodômetro (RNF06)
        return self.__kmNoMomento

    @property
    def litros(self):
        # Permite que a View mostre quantos litros foram comprados
        return self.__litros

    def getCustoLitro(self) -> float:
        if self.litros == 0:
            raise ZeroDivisionError("Litros não pode ser zero.")
        return self.valorTotal / self.litros

    def __repr__(self):
        return (f"Abastecimento(id={self.__id}, litros={self.__litros}, "
                f"valorTotal={self.__valorTotal}, kmNoMomento={self.__kmNoMomento})")