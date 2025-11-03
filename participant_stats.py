import pandas as pd

# Dados da Table 21
table21_data = {
    'Participant ID': [
        'UoM2301', 'UoM2302', 'UoM2303', 'UoM2304', 'UoM2305', 'UoM2306',
        'UoM2307', 'UoM2308', 'UoM2309', 'UoM2310', 'UoM2313', 'UoM2314',
        'UoM2320', 'UoM2401', 'UoM2403', 'UoM2404', 'UoM2405'
    ],
    'Basal Insulin Type': [
        'R', 'L', 'N/A', 'R', 'L', 'L', 'R', 'R', 'R', 'R', 'L', 'L', 'N/A', 'L', 'L', 'N/A', 'L'
    ],
    'Reported Daily Basal [U]': [
        '24', '10', '12', '34.1', '20', '8', '5–7', 'N/A', 'N/A', '22', '64', '12', 'Variable', '5–30', '15', '15', '32'
    ],
    'Reported Daily Bolus [U]': [
        'N/A', '16', '12', '25–30', '23', '20–25', '7–16', 'N/A', 'N/A', '24', '60', '25', 'Variable', '30', '19', '20', '20'
    ],
    'Collected Basal Mean [U]': [
        21.60, 8.06, None, 30.09, 23.00, 9.30, 6.77, 9.58, 19.17, 21.38, 65.80, 12.14, None, 30.00, 12.00, None, 26.30
    ],
    'Collected Basal SD [U]': [
        4.78, 1.36, None, 3.37, 0.00, 2.95, 1.04, 1.24, 1.05, 0.69, 2.20, 3.09, None, 0.00, 4.70, None, 8.28
    ],
    'Collected Bolus Mean [U]': [
        11.59, 10.30, None, 25.30, 16.56, 21.56, 12.53, 15.95, 10.73, 19.99, 42.14, 24.81, 13.66, 40.77, 12.34, 16.93, 16.18
    ],
    'Collected Bolus SD [U]': [
        2.79, 3.95, None, 6.73, 6.69, 3.86, 3.25, 2.64, 4.55, 3.42, 16.03, 6.03, 1.69, 18.00, 6.55, 7.08, 5.99
    ],
    'Days Between Report and Collection': [
        192, 179, 165, 124, 97, 96, 148, 33, 203, 283, 115, 91, 101, 111, 120, 111, 131
    ],
    'Carbs/Insulin Ratio': [
        '9–12', '8–10', 'N/A', '5–7', '10', 'N/A', '12–15', 'N/A', 'N/A', '2.5', '5', '10', '6–10', 'N/A', '15', '10', '1.5'
    ]
}

# Criar DataFrame
df = pd.DataFrame(table21_data)

# Salvar como CSV com separador ","
df.to_csv('participant_stats.csv', index=False)

print("✅ Ficheiro 'participant_stats.csv' criado com sucesso!")