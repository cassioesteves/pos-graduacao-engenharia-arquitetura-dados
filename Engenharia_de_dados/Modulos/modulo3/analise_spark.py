import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType, IntegerType, DoubleType, StringType, StructType, StructField

# --- Funções Definidas pelo Usuário (UDFs) ---

@udf(returnType=BooleanType())
def is_avenida(logradouro):
    """Verifica se um logradouro começa com AVENIDA, ignorando maiúsculas/minúsculas."""
    if not logradouro:
        return False
    return logradouro.strip().upper().startswith("AVENIDA")

@udf(returnType=BooleanType())
def is_cnae_cultivo(descricao):
    """Verifica se a descrição de um CNAE contém a palavra 'cultivo'."""
    if not descricao:
        return False
    return "cultivo" in descricao.lower()


# --- Análise Principal ---

def main():
    """Função principal para executar a análise com Spark."""
    spark = SparkSession.builder \
        .appName("DesafioFinalModulo3") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.driver.extraJavaOptions", 
                "-Djava.security.manager=allow "
                "--add-opens=java.base/java.lang=ALL-UNNAMED "
                "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
                "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED "
                "--add-opens=java.base/java.io=ALL-UNNAMED "
                "--add-opens=java.base/java.net=ALL-UNNAMED "
                "--add-opens=java.base/java.nio=ALL-UNNAMED "
                "--add-opens=java.base/java.util=ALL-UNNAMED "
                "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
                "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED "
                "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
                "--add-opens=java.base/sun.nio.cs=ALL-UNNAMED "
                "--add-opens=java.base/sun.security.action=ALL-UNNAMED "
                "--add-opens=java.base/sun.util.calendar=ALL-UNNAMED "
                "--add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED") \
        .getOrCreate()
    
    print("--- Configurando Ambiente e Carregando Dados ---")
    
    # Define os caminhos para os arquivos de dados
    # O caminho base é o diretório onde o script está localizado
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, "Módulo 3 Soluções de Big Data e Data Lake", "dados")
    cnaes_path = os.path.join(data_dir, "cnaes", "cnaes.csv")
    estabelecimentos_dir = os.path.join(data_dir, "estabelecimentos", "estabelecimentos")
    parquet_output_path = os.path.join(base_path, "estabelecimentos.parquet")

    # --- Carregamento dos Dados ---
    
    # Schema para o arquivo de CNAEs para leitura otimizada
    cnaes_schema = StructType([
        StructField("CNAE", StringType(), True),
        StructField("DESCRICAO_CNAE", StringType(), True)
    ])
    cnaes_df = spark.read.csv(cnaes_path, header=True, sep=";", schema=cnaes_schema)

    # Nomes das colunas para o DataFrame de estabelecimentos
    estabelecimentos_columns = [
        "CNPJ_BASICO", "CNPJ_ORDEM", "CNPJ_DV", "IDENTIFICADOR_MATRIZ_FILIAL",
        "NOME_FANTASIA", "SITUACAO_CADASTRAL", "DATA_SITUACAO_CADASTRAL",
        "MOTIVO_SITUACAO_CADASTRAL", "NOME_DA_CIDADE_NO_EXTERIOR", "PAIS",
        "DATA_INICIO_ATIVIDADE", "CNAE_FISCAL_PRINCIPAL", "CNAE_FISCAL_SECUNDARIA",
        "TIPO_DE_LOGRADOURO", "LOGRADOURO", "NUMERO", "COMPLEMENTO", "BAIRRO",
        "CEP", "UF", "MUNICIPIO", "DDD_1", "TELEFONE_1", "DDD_2", "TELEFONE_2",
        "DDD_DO_FAX", "FAX", "CORREIO_ELETRONICO", "SITUACAO_ESPECIAL", "DATA_DA_SITUACAO_ESPECIAL"
    ]
    
    # Schema para o DataFrame de estabelecimentos para garantir tipos corretos e performance
    estabelecimentos_schema = StructType([
        StructField("CNPJ_BASICO", StringType(), True),
        StructField("CNPJ_ORDEM", StringType(), True),
        StructField("CNPJ_DV", StringType(), True),
        StructField("IDENTIFICADOR_MATRIZ_FILIAL", IntegerType(), True),
        StructField("NOME_FANTASIA", StringType(), True),
        StructField("SITUACAO_CADASTRAL", IntegerType(), True),
        StructField("DATA_SITUACAO_CADASTRAL", StringType(), True),
        StructField("MOTIVO_SITUACAO_CADASTRAL", IntegerType(), True),
        StructField("NOME_DA_CIDADE_NO_EXTERIOR", StringType(), True),
        StructField("PAIS", StringType(), True),
        StructField("DATA_INICIO_ATIVIDADE", StringType(), True),
        StructField("CNAE_FISCAL_PRINCIPAL", StringType(), True),
        StructField("CNAE_FISCAL_SECUNDARIA", StringType(), True),
        StructField("TIPO_DE_LOGRADOURO", StringType(), True),
        StructField("LOGRADOURO", StringType(), True),
        StructField("NUMERO", StringType(), True),
        StructField("COMPLEMENTO", StringType(), True),
        StructField("BAIRRO", StringType(), True),
        StructField("CEP", StringType(), True),
        StructField("UF", StringType(), True),
        StructField("MUNICIPIO", StringType(), True),
        StructField("DDD_1", StringType(), True),
        StructField("TELEFONE_1", StringType(), True),
        StructField("DDD_2", StringType(), True),
        StructField("TELEFONE_2", StringType(), True),
        StructField("DDD_DO_FAX", StringType(), True),
        StructField("FAX", StringType(), True),
        StructField("CORREIO_ELETRONICO", StringType(), True),
        StructField("SITUACAO_ESPECIAL", StringType(), True),
        StructField("DATA_DA_SITUACAO_ESPECIAL", StringType(), True)
    ])

    # Leitura dos múltiplos arquivos CSV de estabelecimentos
    estabelecimentos_df = spark.read.load(
        os.path.join(estabelecimentos_dir, "*.csv"),
        format="csv", sep=";", schema=estabelecimentos_schema, header=False
    )
    
    # Armazena os DataFrames em cache para acesso mais rápido nas operações seguintes
    estabelecimentos_df.cache()
    cnaes_df.cache()
    
    print("Dados carregados.\n")

    # --- Pergunta 1: Quantos estabelecimentos existem? ---
    print("--- Pergunta 1 ---")
    total_estabelecimentos = estabelecimentos_df.count()
    print(f"Total de estabelecimentos: {total_estabelecimentos}\n")

    # --- Pergunta 2: Colunas e tipos numéricos ---
    print("--- Pergunta 2 ---")
    num_cols_total = len(estabelecimentos_df.columns)
    # A pergunta exige o uso de inferSchema, então relemos os dados apenas para esta questão.
    # Em um projeto real, usaríamos o schema já definido.
    estabelecimentos_inferred_df = spark.read.load(
        os.path.join(estabelecimentos_dir, "*.csv"),
        format="csv", sep=";", inferSchema=True, header=False).toDF(*estabelecimentos_columns)
    numeric_cols_count = sum(1 for f in estabelecimentos_inferred_df.schema.fields if isinstance(f.dataType, (IntegerType, DoubleType)))
    print(f"Total de colunas: {num_cols_total}, Colunas numéricas (com inferSchema): {numeric_cols_count}\n")
    
    # --- Pergunta 3: Comparação de tamanho (CSV vs Parquet) ---
    print("--- Pergunta 3 ---")
    if os.path.exists(parquet_output_path):
        shutil.rmtree(parquet_output_path)
    estabelecimentos_df.write.parquet(parquet_output_path)
    
    size_csv_bytes = sum(os.path.getsize(os.path.join(estabelecimentos_dir, f)) for f in os.listdir(estabelecimentos_dir) if f.endswith('.csv'))
    size_parquet_bytes = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, filenames in os.walk(parquet_output_path) for f in filenames)
    
    if size_parquet_bytes > 0:
        reduction_factor = size_csv_bytes / size_parquet_bytes
        print(f"Tamanho CSV: {size_csv_bytes / (1024*1024):.2f} MB")
        print(f"Tamanho Parquet: {size_parquet_bytes / (1024*1024):.2f} MB")
        print(f"Fator de redução: ~{reduction_factor:.1f}x\n")
    else:
        print("Não foi possível calcular a economia de espaço.\n")

    # --- Análises com Spark SQL ---
    estabelecimentos_df.createOrReplaceTempView("estabelecimentos")
    cnaes_df.createOrReplaceTempView("cnaes")
    spark.udf.register("is_avenida_udf", is_avenida)
    spark.udf.register("is_cnae_cultivo_udf", is_cnae_cultivo)

    # --- Pergunta 4: Estabelecimentos sem logradouro ---
    print("--- Pergunta 4 ---")
    logradouro_null_count = spark.sql("SELECT COUNT(*) FROM estabelecimentos WHERE LOGRADOURO IS NULL").first()[0]
    print(f"Estabelecimentos com logradouro nulo: {logradouro_null_count}\n")
    
    # --- Pergunta 5: Logradouros que contêm 'AVENIDA' ---
    print("--- Pergunta 5 ---")
    avenida_count = spark.sql("SELECT COUNT(*) FROM estabelecimentos WHERE is_avenida_udf(LOGRADOURO) = True").first()[0]
    print(f"Estabelecimentos cujo logradouro contém 'AVENIDA': {avenida_count}\n")

    # --- Pergunta 6: CEPs distintos ---
    print("--- Pergunta 6 ---")
    cep_distintos_count = spark.sql("SELECT COUNT(DISTINCT CEP) FROM estabelecimentos").first()[0]
    print(f"Número de CEPs distintos: {cep_distintos_count}\n")
    
    # --- Pergunta 7: CNAEs na tabela CNAES ---
    print("--- Pergunta 7 ---")
    cnaes_count = spark.sql("SELECT COUNT(*) FROM cnaes").first()[0]
    print(f"Total de CNAEs: {cnaes_count}\n")

    # --- Pergunta 8: Estabelecimentos com CNAE de 'cultivo' ---
    print("--- Pergunta 8 ---")
    estabelecimentos_with_cnae = estabelecimentos_df.join(
        cnaes_df,
        estabelecimentos_df.CNAE_FISCAL_PRINCIPAL == cnaes_df.CNAE,
        "inner"
    )
    estabelecimentos_with_cnae.createOrReplaceTempView("estabelecimentos_with_cnae")
    cultivo_count = spark.sql("SELECT COUNT(*) FROM estabelecimentos_with_cnae WHERE is_cnae_cultivo_udf(DESCRICAO_CNAE) = True").first()[0]
    print(f"Estabelecimentos com CNAE de cultivo: {cultivo_count}\n")
    
    # --- Pergunta 11: Estabelecimentos que são filiais ---
    print("--- Pergunta 11 ---")
    # IDENTIFICADOR_MATRIZ_FILIAL: 1-MATRIZ, 2-FILIAL
    filiais_count = spark.sql("SELECT COUNT(*) FROM estabelecimentos WHERE IDENTIFICADOR_MATRIZ_FILIAL = 2").first()[0]
    print(f"Total de filiais: {filiais_count}\n")

    spark.stop()
    print("--- Análise Concluída ---")

if __name__ == "__main__":
    main()