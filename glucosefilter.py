################################## GLUCOSE FILTERS ##################################
"""
import os
import pandas as pd

pasta_csv = "Glucose Data"
pasta_saida = "datasetsconcatenados"

# Garante que a pasta de saída existe
os.makedirs(pasta_saida, exist_ok=True)

# Nome do ficheiro de saída
ficheiro_saida = "glucosedata.csv"

# --- EXECUÇÃO ---
# Lista todos os ficheiros CSV na pasta

ficheiros = [f for f in os.listdir(pasta_csv) if f.endswith(".csv")]

# Lê e concatena todos os ficheiros
dataframes = []
for f in ficheiros:
    caminho_ficheiro = os.path.join(pasta_csv, f)
    print(f"Lendo: {f}")
    df = pd.read_csv(caminho_ficheiro)
    dataframes.append(df)

# Concatena todos os DataFrames
df_final = pd.concat(dataframes, ignore_index=True)



# Guarda o resultado final
df_final.to_csv(os.path.join(pasta_saida, ficheiro_saida), index=False)

print(f"\n✅ Ficheiros concatenados com sucesso!")
print(f"Ficheiro final guardado em: {os.path.join(pasta_saida, ficheiro_saida)}")


# 1. Ler o dataset concatenado
df = pd.read_csv(os.path.join(pasta_saida, ficheiro_saida))

# 2. Filtrar hipoglicemia (< 3.9 mmol/L)
hypo = df[df["value"] < 3.9]

# 3. Filtrar hiperglicemia (> 6.9 mmol/L)
hyper = df[df["value"] > 6.9]

# 4. Guardar os resultados em CSVs separados
hypo.to_csv(os.path.join(pasta_saida, "hypoglycemic.csv"), index=False)
hyper.to_csv(os.path.join(pasta_saida, "hyperglycemic.csv"), index=False)


print(f"Hipoglicemia: {len(hypo)} linhas guardadas em hypoglycemic.csv")
print(f"Hiperglicemia: {len(hyper)} linhas guardadas em hyperglycemic.csv")
"""

################################## CONCATENATION ##################################
"""
import os
import pandas as pd

pasta_csv = "Sleep Data/UoMSleep"
pasta_saida = "datasetsconcatenados"

# Garante que a pasta de saída existe
os.makedirs(pasta_saida, exist_ok=True)

# Nome do ficheiro de saída
ficheiro_saida = "sleepdata.csv"

# --- EXECUÇÃO ---
# Lista todos os ficheiros CSV na pasta

ficheiros = [f for f in os.listdir(pasta_csv) if f.endswith(".csv")]

# Lê e concatena todos os ficheiros
dataframes = []
for f in ficheiros:
    caminho_ficheiro = os.path.join(pasta_csv, f)
    print(f"Lendo: {f}")
    df = pd.read_csv(caminho_ficheiro)
    dataframes.append(df)

# Concatena todos os DataFrames
df_final = pd.concat(dataframes, ignore_index=True)



# Guarda o resultado final
df_final.to_csv(os.path.join(pasta_saida, ficheiro_saida), index=False)

print(f"\n✅ Ficheiros concatenados com sucesso!")
print(f"Ficheiro final guardado em: {os.path.join(pasta_saida, ficheiro_saida)}")
"""

################################## BASAL e BOLUS FILTERS ##################################

import os
import pandas as pd

pasta_csv = "Insulin Data/Bolus Data"
pasta_saida = "datasetsconcatenados"

# Garante que a pasta de saída existe
os.makedirs(pasta_saida, exist_ok=True)

# Nome do ficheiro de saída
ficheiro_saida = "bolusdata1.csv"

# --- EXECUÇÃO ---
# Lista todos os ficheiros CSV na pasta
ficheiros = [f for f in os.listdir(pasta_csv) if f.endswith(".csv")]

# Lê e concatena todos os ficheiros
dataframes = []
for f in ficheiros:
    caminho_ficheiro = os.path.join(pasta_csv, f)
    print(f"Lendo: {f}")
    
    # Extrai o nome do ficheiro sem extensão (id da pessoa)
    id_pessoa = os.path.splitext(f)[0]
    
    # Lê o CSV
    df = pd.read_csv(caminho_ficheiro)
    
    # Adiciona uma coluna com o id da pessoa
    df["id_pessoa"] = id_pessoa
    
    dataframes.append(df)

# Concatena todos os DataFrames
df_final = pd.concat(dataframes, ignore_index=True)

# Guarda o resultado final
df_final.to_csv(os.path.join(pasta_saida, ficheiro_saida), index=False)

print(f"\n✅ Ficheiros concatenados com sucesso!")
print(f"Ficheiro final guardado em: {os.path.join(pasta_saida, ficheiro_saida)}")
