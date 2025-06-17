def comparar_leitura(leitura, gabarito):
    acertos = 0
    total = 0

    for l_resp, l_gab in zip(leitura, gabarito):
        if l_resp in ['X', '-', ' ']:  # Ignora anuladas/brancos
            continue
        if l_resp == l_gab:
            acertos += 1
        total += 1

    return acertos, total