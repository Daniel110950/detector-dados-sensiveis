import os 



def ler_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    return conteudo


arquivo = "exemplo.txt"

texto = ler_arquivo(arquivo)

print("Conteúdo do arquivo:")
print(texto)


