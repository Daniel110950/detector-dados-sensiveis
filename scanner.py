import os 
import re


PADROES = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "SENHA": r"(?i)\bsenha\s*[:=]\s*\S+",
    "API_KEY": r"(?i)\bapi[_-]?key\s*[:=]\s*\S+",
}

# 🟢 ADICIONAR AQUI (logo abaixo de PADROES)

def mascarar_valor(tipo: str, valor: str) -> str:
    v = valor.strip()

    if tipo == "SENHA":
        return re.sub(r"(?i)(\bsenha\s*[:=]\s*)(\S+)", r"\1****", v)

    if tipo == "API_KEY":
        return re.sub(
            r"(?i)(\bapi[_-]?key\s*[:=]\s*)(\S+)",
            lambda m: m.group(1) + _mascarar_token(m.group(2)),
            v
        )

    if tipo == "EMAIL":
        return _mascarar_email(v)

    return "****"


def _mascarar_token(token: str) -> str:
    if len(token) <= 4:
        return "****"
    return token[:4] + "****"


def _mascarar_email(email: str) -> str:
    if "@" not in email:
        return "****"
    usuario, dominio = email.split("@", 1)
    prefixo = usuario[:2] if len(usuario) > 2 else usuario[:1]
    return f"{prefixo}****@{dominio}"


def ler_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
     return f.read()  # retorna o conteúdo do arquivo como string



# 🟢 ADICIONAR (nova detectar com mascaramento)
def detectar(texto):
    achados = {}
    for tipo, padrao in PADROES.items():
        encontrados = re.findall(padrao, texto)
        achados[tipo] = [mascarar_valor(tipo, v) for v in encontrados]
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




