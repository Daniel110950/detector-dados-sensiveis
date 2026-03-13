import os 
import re


PADROES = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "SENHA": r"(?i)\bsenha\s*[:=]\s*\S+",
    "API_KEY": r"(?i)\bapi[_-]?key\s*[:=]\s*\S+",
  
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "TELEFONE": r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}\b",
    "CARTAO": r"\b(?:\d[ -]*?){13,19}\b",
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

    if tipo == "CPF":
        return _mascarar_cpf(v)

    if tipo == "TELEFONE":
        return _mascarar_telefone(v)

    if tipo == "CARTAO":
        return _mascarar_cartao(v)


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


def _somente_digitos(s: str) -> str:
    return re.sub(r"\D", "", s)


def _mascarar_cpf(cpf: str) -> str:
    d = _somente_digitos(cpf)
    if len(d) != 11:
        return "****"
    # 123.456.789-00 -> ***.***.***-00
    return "***.***.***-" + d[-2:]


def _mascarar_telefone(tel: str) -> str:
    d = _somente_digitos(tel)
    if len(d) < 8:
        return "****"
    # mantém só os 2 últimos dígitos
    return "****" + d[-2:]


def _mascarar_cartao(cartao: str) -> str:
    d = _somente_digitos(cartao)
    if len(d) < 13 or len(d) > 19:
        return "****"
    # mantém últimos 4
    return "**** **** **** " + d[-4:]


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




