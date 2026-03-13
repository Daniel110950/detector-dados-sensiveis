# 🔐 Detector de Dados Sensíveis

Ferramenta em Python para **detecção e mascaramento de dados sensíveis** em arquivos de texto.
O projeto evoluiu de um script simples para um **plugin com interface web**, mantendo foco em **segurança da informação**.

---

## 📌 Objetivo

Identificar possíveis dados sensíveis em arquivos de texto **sem nunca expor os valores reais**, aplicando mascaramento antes de qualquer exibição.

---

## ✅ Funcionalidades

- Leitura de arquivos `.txt`
- Detecção por expressões regulares (Regex)
- **Mascaramento automático** dos dados sensíveis
- Execução via terminal **ou** interface web
- Upload de arquivos pelo navegador (FastAPI)

---

## 🔎 Tipos de Dados Detectados e Mascarados

| Tipo       | Exemplo Original              | Saída Mascarada        |
|------------|-------------------------------|------------------------|
| Email      | maria.silva@empresa.com       | ma****@empresa.com     |
| Senha      | Senha: MinhaSenha@123         | Senha: ****            |
| API Key    | API_KEY=sk-TESTE-ABC123       | API_KEY=sk-T****       |
| CPF        | 123.456.789-00                | ***.***.***-00         |
| Telefone   | (81) 91234-5678               | ****78                 |
| Cartão     | 4111 1111 1111 1111           | **** **** **** 1111    |

---

## 🏗️ Estrutura do Projeto

``

detector-dados-sensiveis/
│
├── scanner.py          # Lógica de detecção e mascaramento
├── plugin.py           # API FastAPI (plugin web)
├── templates/
│   └── upload.html     # Interface de upload
├── assets/
│   └── plugin-ui.png   # Imagem do plugin
├── exemplo.txt         # Arquivo de teste
├── README.md
└── .gitignore



---

## ▶️ Como Usar (Script)

```bash
python scanner.py

O script irá analisar o arquivo configurado e exibir os dados já mascarados.

 Instalar dependências
pip install fastapi uvicorn python-multipart

 Subir o servidor
 python -m uvicorn plugin:app --reload
``
Acessar no navegador
http://127.0.0.1:8000

