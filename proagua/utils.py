def get_hierarquia(ponto, amostragem: int):
    pontos = []

    while ponto is not None:
        coletas = ponto.coletas.filter(amostragem=amostragem)

        pontos.append({
            "id": ponto.id,
            "nome": str(ponto),
            "edificacao": ponto.edificacao,
            "ambiente": ponto.ambiente,
            "coletas": coletas
        })

        ponto = ponto.pai

    return pontos