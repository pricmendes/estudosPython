# neste codigo ele imprime na tela os cpfs duplicados e informa quantos foram inseridos
import pandas as pd
import pyodbc as pyodbc
import numpy as np

# Conexão usando a autenticação do Windows
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=PCM\SERVERTESTES;'
    r'DATABASE=testeExcel;'
    r'Trusted_Connection=yes;'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Carregar o arquivo Excel, considerando que a primeira linha é o cabeçalho
excel_file = r"C:\PROGRAMACAO\PYTHON\testeExcel\testeExcel.xlsx"
df = pd.read_excel(excel_file, header=0)

# Exibir o número de colunas e as primeiras linhas para depuração
print(f"Número de colunas: {len(df.columns)}")
print(df.head())

# Definir a lista de colunas esperadas
expected_columns = [
    'SETOR', 'CONVENIO', 'BANCO', 'CPF', 'NOME', 'SEXO', 'NASC', 'IDADE', 
    'TIPO', 'LOGRADOURO', 'NUMERO', 'COMPLEMENTO', 'BAIRRO', 'CIDADE', 
    'UF', 'CEP', 'DDDCEL1', 'CEL1', 'PROCONCEL1', 'DDDCEL2', 'CEL2', 
    'PROCONCEL2', 'DDDCEL3', 'CEL3', 'PROCONCEL3', 'DDDCEL4', 'CEL4', 
    'PROCONCEL4', 'DDD1', 'FONE1', 'PROCON1', 'EMAIL1'
]

# Filtrar apenas as colunas esperadas
df = df[expected_columns]

# Converter datas para o formato adequado
df['NASC'] = pd.to_datetime(df['NASC'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')

# Substituir valores NaN por None
df = df.replace({np.nan: None})

# Contador de novos registros inseridos
new_records_count = 0

# Inserir os dados na tabela HigiNovaVida
for index, row in df.iterrows():
    try:
        # Verificar se o CPF já existe na tabela
        cursor.execute("SELECT COUNT(*) FROM HigiNovaVida WHERE CPF = ?", row.CPF)
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO Clientes (
                SETOR, CONVENIO, BANCO, CPF, NOME, SEXO, NASC, IDADE, TIPO, LOGRADOURO, 
                NUMERO, COMPLEMENTO, BAIRRO, CIDADE, UF, CEP, DDDCEL1, CEL1, PROCONCEL1, 
                DDDCEL2, CEL2, PROCONCEL2, DDDCEL3, CEL3, PROCONCEL3, DDDCEL4, CEL4, 
                PROCONCEL4, DDD1, FONE1, PROCON1, EMAIL1) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            row.SETOR, row.CONVENIO, row.BANCO, row.CPF, row.NOME, row.SEXO, row.NASC, 
            row.IDADE, row.TIPO, row.LOGRADOURO, row.NUMERO, row.COMPLEMENTO, 
            row.BAIRRO, row.CIDADE, row.UF, row.CEP, row.DDDCEL1, row.CEL1, 
            row.PROCONCEL1, row.DDDCEL2, row.CEL2, row.PROCONCEL2, 
            row.DDDCEL3, row.CEL3, row.PROCONCEL3, row.DDDCEL4, row.CEL4, 
            row.PROCONCEL4, row.DDD1, row.FONE1, row.PROCON1, row.EMAIL1)
            
            # Incrementar o contador de novos registros
            new_records_count += 1
        else:
            print(f"CPF já existe na tabela: {row.CPF}")
        
    except Exception as e:
        print(f"Erro na linha {index}: {e}")

# Confirmar a inserção dos dados
conn.commit()

# Fechar a conexão
cursor.close()
conn.close()

print(f"Dados inseridos com sucesso! Total de novos registros inseridos: {new_records_count}")
