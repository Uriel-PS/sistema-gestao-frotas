from dataclasses import dataclass, field

# RF06

@dataclass # automatização do __repr__ e __init__
class Relatorio:
    placa: str
    custoPorKm: float
    mediaConsumo: float
    totalGastoCombustivel: float = 0.0
    totalGastoManutencao: float = 0.0
    detalhes: list = field(default_factory=list)


class Dashboard:
    def calcularCustoPorKm(self, v) -> float:
        custos_variaveis = sum(a.valorTotal for a in v.abastecimentos)
        custos_fixos = sum(m.custoTotal for m in v.manutencoes)

        if v.kmAtual == 0:
            raise ZeroDivisionError(
                "Não é possível calcular o CPK: veículo não rodou nenhum km."
            )
        return (custos_fixos + custos_variaveis) / v.kmAtual # fórmula CPK

    def calcularMediaConsumo(self, v) -> float:

        def extrair_quilometragem(abastecimento):
            return abastecimento.kmNoMomento
        
        abastecimentos_ordenados = sorted(v.abastecimentos, key=extrair_quilometragem)

        if len(abastecimentos_ordenados) < 2:
            raise ValueError(
                "São necessários ao menos dois abastecimentos para calcular a média."
            )

        distancia = abastecimentos_ordenados[-1].kmNoMomento - abastecimentos_ordenados[0].kmNoMomento
        litros = sum(a.litros for a in abastecimentos_ordenados[1:])

        if litros == 0:
            raise ZeroDivisionError("Total de litros consumidos é zero.")
        
        return distancia / litros
    

    def gerarRelatorio(self, v) -> Relatorio:
        detalhes = []

        try: #try catch
            cpk = self.calcularCustoPorKm(v)
        except ZeroDivisionError as e:
            cpk = 0.0
            detalhes.append(str(e))

        try:
            media = self.calcularMediaConsumo(v)
        except (ZeroDivisionError, ValueError) as e:
            media = 0.0
            detalhes.append(str(e))

        return Relatorio(
            placa=v.placa,
            custoPorKm=cpk,
            mediaConsumo=media,
            totalGastoCombustivel=sum(a.valorTotal for a in v.abastecimentos),
            totalGastoManutencao=sum(m.custoTotal for m in v.manutencoes),
            detalhes=detalhes,
        )