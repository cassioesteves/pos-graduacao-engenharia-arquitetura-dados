import os
import glob
import pandas as pd
import shutil

def main():
    print("--- Iniciando Análise com Pandas ---")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, "Módulo 3 Soluções de Big Data e Data Lake", "dados")
    cnaes_path = os.path.join(data_dir, "cnaes", "cnaes.csv")
    estabelecimentos_dir = os.path.join(data_dir, "estabelecimentos", "estabelecimentos")
    parquet_output_path = os.path.join(base_path, "estabelecimentos_pandas.parquet")

    # --- Carregamento CNAEs ---
    print("Carregando CNAEs...")
    cnaes_df = pd.read_csv(cnaes_path, sep=";", encoding='latin1', dtype=str) # Force string to match Spark behavior for codes
    print(f"CNAEs carregados: {len(cnaes_df)}")

    # --- Carregamento Estabelecimentos ---
    print("Carregando Estabelecimentos...")
    estab_files = glob.glob(os.path.join(estabelecimentos_dir, "*.csv"))
    
    estabelecimentos_columns = [
        "CNPJ_BASICO", "CNPJ_ORDEM", "CNPJ_DV", "IDENTIFICADOR_MATRIZ_FILIAL",
        "NOME_FANTASIA", "SITUACAO_CADASTRAL", "DATA_SITUACAO_CADASTRAL",
        "MOTIVO_SITUACAO_CADASTRAL", "NOME_DA_CIDADE_NO_EXTERIOR", "PAIS",
        "DATA_INICIO_ATIVIDADE", "CNAE_FISCAL_PRINCIPAL", "CNAE_FISCAL_SECUNDARIA",
        "TIPO_DE_LOGRADOURO", "LOGRADOURO", "NUMERO", "COMPLEMENTO", "BAIRRO",
        "CEP", "UF", "MUNICIPIO", "DDD_1", "TELEFONE_1", "DDD_2", "TELEFONE_2",
        "DDD_DO_FAX", "FAX", "CORREIO_ELETRONICO", "SITUACAO_ESPECIAL", "DATA_DA_SITUACAO_ESPECIAL"
    ]

    # Reading all files into one DataFrame (assuming it fits in memory)
    dfs = []
    for f in estab_files:
        # Using low_memory=False to avoid mixed type warnings, or specifying dtypes would be better
        # We read as string first to avoid leading zero issues, then convert as needed
        df = pd.read_csv(f, sep=";", header=None, names=estabelecimentos_columns, encoding='latin1', dtype=str, on_bad_lines='skip')
        dfs.append(df)
    
    estab_df = pd.concat(dfs, ignore_index=True)
    print(f"Estabelecimentos carregados: {len(estab_df)}")
    print("-" * 30)

    # --- Pergunta 1: Quantos estabelecimentos existem? ---
    print(f"Pergunta 1 (Total Estabelecimentos): {len(estab_df)}")

    # --- Pergunta 2: Colunas e tipos numéricos (Simulação) ---
    # Spark inferSchema logic is complex to mimic perfectly, but let's check what looks numeric.
    # We will reload a sample with pandas default inference to see what it thinks.
    sample_df = pd.read_csv(estab_files[0], sep=";", header=None, names=estabelecimentos_columns, encoding='latin1', nrows=1000)
    numeric_cols = 0
    for col in sample_df.columns:
        if pd.api.types.is_numeric_dtype(sample_df[col]):
            numeric_cols += 1
    print(f"Pergunta 2 (Colunas: {len(sample_df.columns)}, Numéricas (Pandas est.): {numeric_cols})")
    print("Nota: O Spark pode inferir diferente. Verifique as opções: 30 e 13, 30 e 12, 30 e 0, 30 e 30.")

    # --- Pergunta 3: Comparação de tamanho (CSV vs Parquet) ---
    print("Pergunta 3 (Compressão Parquet)...")
    try:
        if os.path.exists(parquet_output_path):
            if os.path.isdir(parquet_output_path):
                shutil.rmtree(parquet_output_path)
            else:
                os.remove(parquet_output_path)
        
        # Writing to parquet (using pyarrow or fastparquet)
        estab_df.to_parquet(parquet_output_path, compression='snappy')
        
        size_csv = sum(os.path.getsize(f) for f in estab_files)
        size_parquet = os.path.getsize(parquet_output_path)
        
        print(f"Tamanho CSV: {size_csv / (1024*1024):.2f} MB")
        print(f"Tamanho Parquet: {size_parquet / (1024*1024):.2f} MB")
        print(f"Fator: {size_csv/size_parquet:.2f}x")
    except Exception as e:
        print(f"Erro ao gerar parquet: {e}")

    # --- Pergunta 4: Logradouro NULL ---
    # In Pandas, empty strings or NaN are nulls.
    null_logradouro = estab_df['LOGRADOURO'].isna().sum()
    print(f"Pergunta 4 (Logradouro NULL): {null_logradouro}")

    # --- Pergunta 5: Logradouro contém 'AVENIDA' ---
    # "is_avenida" logic: strip().upper().startswith("AVENIDA")
    def is_avenida(x):
        if pd.isna(x): return False
        return str(x).strip().upper().startswith("AVENIDA")
    
    avenida_count = estab_df['LOGRADOURO'].apply(is_avenida).sum()
    print(f"Pergunta 5 (Logradouro 'AVENIDA'): {avenida_count}")

    # --- Pergunta 6: CEPs distintos ---
    distinct_ceps = estab_df['CEP'].nunique()
    print(f"Pergunta 6 (CEPs distintos): {distinct_ceps}")

    # --- Pergunta 7: Total CNAEs ---
    print(f"Pergunta 7 (Total CNAEs): {len(cnaes_df)}")

    # --- Pergunta 8: CNAE Cultivo ---
    # Join estab_df with cnaes_df on CNAE_FISCAL_PRINCIPAL == CNAE
    # cnaes_df columns: CNAE, DESCRICAO_CNAE
    # estab_df columns: ..., CNAE_FISCAL_PRINCIPAL, ...
    
    # Ensure keys match type
    cnaes_df['CNAE'] = cnaes_df['CNAE'].astype(str)
    estab_df['CNAE_FISCAL_PRINCIPAL'] = estab_df['CNAE_FISCAL_PRINCIPAL'].astype(str)
    
    merged_df = estab_df.merge(cnaes_df, left_on='CNAE_FISCAL_PRINCIPAL', right_on='CNAE', how='inner')
    
    def is_cultivo(x):
        if pd.isna(x): return False
        return "cultivo" in str(x).lower()
        
    cultivo_count = merged_df['DESCRICAO_CNAE'].apply(is_cultivo).sum()
    print(f"Pergunta 8 (CNAE 'cultivo'): {cultivo_count}")

    # --- Pergunta 11: Filiais ---
    # IDENTIFICADOR_MATRIZ_FILIAL == 2
    # Note: We read as string, so check for "2"
    filiais_count = (estab_df['IDENTIFICADOR_MATRIZ_FILIAL'] == "2").sum()
    print(f"Pergunta 11 (Filiais): {filiais_count}")

if __name__ == "__main__":
    main()
