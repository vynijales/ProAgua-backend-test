def get_hierarquia(ponto, amostragem: int): 

    while ponto != None:
        coletas = ponto.coletas.filter(amostragem=amostragem)
        
        if coletas.count() == 0:
            break

        pontos = []

        pontos.append({
            "edificacao": ponto.edificacao,
            "ambiente": ponto.ambiente,
            "coletas": coletas
        })

        ponto = ponto.pai

    return pontos
