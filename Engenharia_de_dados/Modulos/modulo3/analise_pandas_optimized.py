import os
import glob
import pandas as pd

def main():
    print("--- Iniciando Análise Otimizada (Q8 e Q11) ---")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, "Módulo 3 Soluções de Big Data e Data Lake", "dados")
    cnaes_path = os.path.join(data_dir, "cnaes", "cnaes.csv")
    estabelecimentos_dir = os.path.join(data_dir, "estabelecimentos", "estabelecimentos")

    # --- 1. Identificar CNAEs de Cultivo ---
    print("Carregando CNAEs...")
    cnaes_df = pd.read_csv(cnaes_path, sep=";", encoding='latin1', dtype=str)
    
    def is_cultivo(x):
        if pd.isna(x): return False
        return "cultivo" in str(x).lower()
    
    cultivo_cnaes = set(cnaes_df[cnaes_df['DESCRICAO_CNAE'].apply(is_cultivo)]['CNAE'])
    print(f"CNAEs de Cultivo identificados: {len(cultivo_cnaes)}")

    # --- 2. Processar Estabelecimentos em Chunks ---
    print("Processando Estabelecimentos...")
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

    total_filiais = 0
    total_cultivo = 0
    total_processed = 0

    for f in estab_files:
        print(f"Lendo {os.path.basename(f)}...")
        # Read only necessary columns
        chunks = pd.read_csv(
            f, sep=";", header=None, names=estabelecimentos_columns, 
            encoding='latin1', dtype=str, on_bad_lines='skip',
            usecols=["IDENTIFICADOR_MATRIZ_FILIAL", "CNAE_FISCAL_PRINCIPAL"],
            chunksize=100000
        )
        
        for chunk in chunks:
            # Q11: Filiais (IDENTIFICADOR_MATRIZ_FILIAL == "2")
            total_filiais += (chunk["IDENTIFICADOR_MATRIZ_FILIAL"] == "2").sum()
            
            # Q8: Cultivo (CNAE_FISCAL_PRINCIPAL in cultivo_cnaes)
            total_cultivo += chunk["CNAE_FISCAL_PRINCIPAL"].isin(cultivo_cnaes).sum()
            
            total_processed += len(chunk)
            
    print("-" * 30)
    print(f"Total processado: {total_processed}")
    print(f"Pergunta 8 (CNAE 'cultivo'): {total_cultivo}")
    print(f"Pergunta 11 (Filiais): {total_filiais}")

if __name__ == "__main__":
    main()
