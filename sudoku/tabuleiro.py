from leitor import dicast
tabuleiro = [[0 for i in range(9)] for i in range(9)]

for lin,col,val in dicast:      #loop pra preencher o tabuleiro
    tabuleiro[lin][col] = val 

#funçao pra imprimir o tabuleiro bonitinho
def printar_tabuleiro(tab):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print('-' * 32)  # linha horizontal a cada 3 linhas

        linhaf = ''
        for j in range(9):
            if j % 3 == 0 and j != 0:
                linhaf += ' | ' #linha vertical a cada 3 colunas

            valor = tab[i][j]
            if valor == 0:
                linhaf += ' . '
            else:
                linhaf += f'\033[31m{str(valor):^3}\033[m'
        
        print(linhaf)


printar_tabuleiro(tabuleiro)