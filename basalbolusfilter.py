import pandas as pd
import numpy as np

# --- Configuração ---
INPUT_BASAL = 'datasetsconcatenados/basaldata1.csv'
INPUT_BOLUS = 'datasetsconcatenados/bolusdata1.csv'
INPUT_STATS = 'datasetsconcatenados/participant_stats.csv'

OUTPUT_BASAL = 'filteredbasal.csv'
OUTPUT_BOLUS = 'filteredbolus.csv'

# --- Leitura dos dados ---
print("Lendo os datasets...")
basal_df = pd.read_csv(INPUT_BASAL)
bolus_df = pd.read_csv(INPUT_BOLUS)
stats_df = pd.read_csv(INPUT_STATS)

# --- Normalizações iniciais ---
# Compatibilidade no nome do ID
if 'Participant ID' in stats_df.columns and 'id_pessoa' not in stats_df.columns:
    stats_df = stats_df.rename(columns={'Participant ID': 'id_pessoa'})

# Garantir que os IDs estão como string e sem espaços
for df in (stats_df, basal_df, bolus_df):
    if 'id_pessoa' in df.columns:
        df['id_pessoa'] = df['id_pessoa'].astype(str).str.strip()
    else:
        raise KeyError("Falta a coluna 'id_pessoa' num dos ficheiros (basal, bolus ou stats).")

# Normalizar IDs: remover "Basal" ou "Bolus" dos IDs para fazer match com participant_stats
basal_df['id_pessoa'] = basal_df['id_pessoa'].str.replace('Basal', '', case=False)
bolus_df['id_pessoa'] = bolus_df['id_pessoa'].str.replace('Bolus', '', case=False)

# Forçar colunas de dose a numérico
basal_df['basal_dose'] = pd.to_numeric(basal_df.get('basal_dose'), errors='coerce')
bolus_df['bolus_dose'] = pd.to_numeric(bolus_df.get('bolus_dose'), errors='coerce')

print(f"Linhas iniciais - basal: {len(basal_df)}, bolus: {len(bolus_df)}, stats: {len(stats_df)}")

# --- Filtro 1: Remover rows com doses ausentes (não numéricas) ---
print("Filtro 1: Removendo linhas com doses ausentes (NaN)...")
before = len(basal_df)
basal_df = basal_df.dropna(subset=['basal_dose']).copy()
print(f" Basal: {before} -> {len(basal_df)}")

before = len(bolus_df)
bolus_df = bolus_df.dropna(subset=['bolus_dose']).copy()
print(f" Bolus: {before} -> {len(bolus_df)}")

# --- Filtro 2: Remover doses <= 0 ---
print("Filtro 2: Removendo doses <= 0 ...")
before = len(basal_df)
basal_df = basal_df[basal_df['basal_dose'] > 0].copy()
print(f" Basal: {before} -> {len(basal_df)}")

before = len(bolus_df)
bolus_df = bolus_df[bolus_df['bolus_dose'] > 0].copy()
print(f" Bolus: {before} -> {len(bolus_df)}")

# --- Preparar colunas de estatística no stats_df ---
# Procurar colunas por padrão (tolerante a variações)
def find_col(cols, keywords):
    for k in cols:
        if all(kw.lower() in k.lower() for kw in keywords):
            return k
    return None

cols = stats_df.columns.tolist()
basal_mean_col = find_col(cols, ['Collected', 'Basal', 'Mean'])
basal_sd_col   = find_col(cols, ['Collected', 'Basal', 'SD'])
bolus_mean_col = find_col(cols, ['Collected', 'Bolus', 'Mean'])
bolus_sd_col   = find_col(cols, ['Collected', 'Bolus', 'SD'])

if not basal_mean_col or not basal_sd_col or not bolus_mean_col or not bolus_sd_col:
    print("Aviso: não foi possível detectar todas as colunas de estatísticas automaticamente.")
    print("Colunas encontradas em stats_df:", cols)
    # Continua, mas quem faltar será tratada como NaN -> participantes sem stats serão excluídos.

# Converter para colunas canónicas e numéricas
stats_df = stats_df.copy()
if basal_mean_col: stats_df['basal_mean'] = pd.to_numeric(stats_df[basal_mean_col], errors='coerce')
else: stats_df['basal_mean'] = np.nan

if basal_sd_col: stats_df['basal_sd'] = pd.to_numeric(stats_df[basal_sd_col], errors='coerce')
else: stats_df['basal_sd'] = np.nan

if bolus_mean_col: stats_df['bolus_mean'] = pd.to_numeric(stats_df[bolus_mean_col], errors='coerce')
else: stats_df['bolus_mean'] = np.nan

if bolus_sd_col: stats_df['bolus_sd'] = pd.to_numeric(stats_df[bolus_sd_col], errors='coerce')
else: stats_df['bolus_sd'] = np.nan

# --- Construir limites por participante ---
participant_limits = {}
for _, row in stats_df.iterrows():
    pid = str(row['id_pessoa']).strip()
    basal_mean = row.get('basal_mean', np.nan)
    basal_sd   = row.get('basal_sd', np.nan)
    bolus_mean = row.get('bolus_mean', np.nan)
    bolus_sd   = row.get('bolus_sd', np.nan)

    # Usar np.isfinite para garantir valores numéricos
    if np.isfinite(basal_mean) and np.isfinite(basal_sd):
        basal_min = basal_mean - 2 * basal_sd
        basal_max = basal_mean + 2 * basal_sd
    else:
        basal_min = basal_max = None

    if np.isfinite(bolus_mean) and np.isfinite(bolus_sd):
        bolus_min = bolus_mean - 2 * bolus_sd
        bolus_max = bolus_mean + 2 * bolus_sd
    else:
        bolus_min = bolus_max = None

    participant_limits[pid] = {
        'basal_min': basal_min, 'basal_max': basal_max,
        'bolus_min': bolus_min, 'bolus_max': bolus_max
    }

# --- Filtro 3: Validar doses basais por participante ---
print("Filtro 3: Validando doses basais por participante...")
def filter_basal_by_participant(row):
    pid = str(row['id_pessoa']).strip()
    dose = row['basal_dose']
    limits = participant_limits.get(pid, {})
    min_val = limits.get('basal_min')
    max_val = limits.get('basal_max')
    # Se não houver estatísticas válidas, EXCLUI (mantive a tua lógica original)
    if min_val is None or max_val is None:
        return False
    return (min_val <= dose <= max_val)

before = len(basal_df)
basal_filtered = basal_df[basal_df.apply(filter_basal_by_participant, axis=1)].copy()
print(f" Basal: {before} -> {len(basal_filtered)} (excluí {before - len(basal_filtered)} por limites ausentes/fora)")

# --- Filtro 4: Validar doses bolus por participante ---
print("Filtro 4: Validando doses bolus por participante...")
def filter_bolus_by_participant(row):
    pid = str(row['id_pessoa']).strip()
    dose = row['bolus_dose']
    limits = participant_limits.get(pid, {})
    min_val = limits.get('bolus_min')
    max_val = limits.get('bolus_max')
    if min_val is None or max_val is None:
        return False
    return (min_val <= dose <= max_val)

before = len(bolus_df)
bolus_filtered = bolus_df[bolus_df.apply(filter_bolus_by_participant, axis=1)].copy()
print(f" Bolus: {before} -> {len(bolus_filtered)} (excluí {before - len(bolus_filtered)} por limites ausentes/fora)")

# --- Salvando os resultados ---
print(f"Salvando {len(basal_filtered)} linhas de basal filtradas em {OUTPUT_BASAL}...")
basal_filtered.to_csv(OUTPUT_BASAL, index=False)

print(f"Salvando {len(bolus_filtered)} linhas de bolus filtradas em {OUTPUT_BOLUS}...")
bolus_filtered.to_csv(OUTPUT_BOLUS, index=False)

print("✅ Processo concluído com sucesso!")
