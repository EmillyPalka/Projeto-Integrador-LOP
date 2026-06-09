#importação da biblioteca pandas para dados
import pandas as pd
import pywhatkit

#Lendo o arquivo csv
try:
    dados = pd.read_csv("Produtos.csv", sep=";")
except FileNotFoundError:
    print("Arquivo não encontrado.")

#Criação do HTML como uma variável
html = """
<html>
<head>
    <title>Estoque</title>
    
     <style>
        body{
            font-family: Arial, sans-serif;
            background-color: #ffeef5;
            padding: 30px;
        }

        h1{
            text-align: center;
            color: #d63384;
        }

        table{
            width: 80%;
            margin: auto;
            border-collapse: collapse;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }

        th{
            background-color: #ffb6d9;
            color: white;
            padding: 12px;
        }

        td{
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #f2f2f2;
        }

        tr:hover{
            background-color: #fff0f6;
        }

        .baixo{
            color: #ff4d6d;
            font-weight: bold;
        }

        .medio{
            color: #ff9f1c;
            font-weight: bold;
        }

        .alto{
            color: #2a9d8f;
            font-weight: bold;
        }
    </style>

</head>

<body>

    <br><h1>Produtos em estoque</h1><br><br>

    <table border="1">

        <tr>
            <th>Código</th>
            <th>Produto</th>
            <th>Quantidade Total</th>
            <th>Preço</th>
            <th>Status</th>
        </tr>
"""

# Somar a quantidade reservada com a disponível para definir nível de estoque
dados['Quantidade_Total'] = (
    dados['Qtde_Disponivel'] + dados['Qtde_Reservada']
)

# Função para status do nível do estoque
def verificar_status(qtd):
    if qtd < 50:
        return "Baixo"
    elif qtd >= 50 and qtd < 100:
        return "Médio"
    else:
        return "Alto"

# Criar coluna status
dados['Status'] = dados['Quantidade_Total'].apply(verificar_status)

# Percorre linha por linha do arquivo csv para gerar uma tabela em html
for index, linha in dados.iterrows():

    #Adicionando na variável do html a tabela com os dados
    html += f"""
        <tr>
            <td>{linha['Codigo']}</td>
            <td>{linha['Produto']}</td>
            <td>{linha['Quantidade_Total']}</td>
            <td>R$ {linha['Preco']}</td>
            <td>{linha['Status']}</td>
        </tr>
    """

html += """
    </table>

</body>
</html>
"""
# Criar a página html com os dados
with open("estoque.html", "w", encoding="utf-8") as arquivo:
    arquivo.write(html)

# Criar o excel
dados[['Codigo','Produto', 'Quantidade_Total', 'Preco', 'Status']].to_excel(
    "Relatorio_Estoque.xlsx",
    index=False
)

# Enviar mensagem no WhatsApp
pywhatkit.sendwhatmsg_instantly(
    phone_no="+5519991731974",
    message="O estoque foi atualizado com sucesso! O relatório já foi enviado por e-mail."
)

print("Mensagem enviada no WhatsApp!")

