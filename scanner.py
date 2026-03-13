import os 
import re


PADROES = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "SENHA": r"(?i)\bsenha\s*[:=]\s*\S+",
    "API_KEY": r"(?i)\bapi[_-]?key\s*[:=]\s*\S+",
}



def ler_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
     return f.read()  # retorna o conteúdo do arquivo como string



def detectar(texto):
    achados = {}
    for tipo, padrao in PADROES.items():
        achados[tipo] = re.findall(padrao, texto)
    return achados



if __name__ == "__main__":
    arquivo = "exemplo.txt"
    texto = ler_arquivo(arquivo)
    achados = detectar(texto)

    print(f"Arquivo analisado: {arquivo}\n")
   
    for tipo, itens in achados.items():
        if itens:
            print(f"[{tipo}] encontrado:")
            for i in itens:
                print(" -", i)
            print()
        else:
            print(f"[{tipo}] nada encontrado.\n")




