import os
from pyspark.sql import SparkSession

def get_spark_session():
    """Creates and returns a Spark Session."""
    return SparkSession.builder \
        .appName("DesafioFinalModulo3") \
        .master("local[*]") \
        .getOrCreate()

def load_data(spark):
    """Loads CNAES and Estabelecimentos data."""
    # Define paths - assumes the script runs from '.../Engenharia_de_dados/Modulos/modulo3'
    base_path = os.getcwd()
    data_dir = os.path.join(base_path, "Módulo 3 Soluções de Big Data e Data Lake", "dados")
    cnaes_path = os.path.join(data_dir, "cnaes", "cnaes.csv")
    estabelecimentos_path = os.path.join(data_dir, "estabelecimentos", "estabelecimentos")

    # Load CNAEs
    cnaes_df = spark.read.csv(cnaes_path, header=True, sep=";", inferSchema=True)

    # Load Estabelecimentos
    estabelecimentos_columns = [
        "CNPJ_BASICO", "CNPJ_ORDEM", "CNPJ_DV", "IDENTIFICADOR_MATRIZ_FILIAL",
        "NOME_FANTASIA", "SITUACAO_CADASTRAL", "DATA_SITUACAO_CADASTRAL",
        "MOTIVO_SITUACAO_CADASTRAL", "NOME_DA_CIDADE_NO_EXTERIOR", "PAIS",
        "DATA_INICIO_ATIVIDADE", "CNAE_FISCAL_PRINCIPAL", "CNAE_FISCAL_SECUNDARIA",
        "TIPO_DE_LOGRADOURO", "LOGRADOURO", "NUMERO", "COMPLEMENTO", "BAIRRO",
        "CEP", "UF", "MUNICIPIO", "DDD_1", "TELEFONE_1", "DDD_2", "TELEFONE_2",
        "DDD_DO_FAX", "FAX", "CORREIO_ELETRONICO", "SITUACAO_ESPECIAL", "DATA_DA_SITUACAO_ESPECIAL"
    ]
    estabelecimentos_df = spark.read.load(
        os.path.join(estabelecimentos_path, "*.csv"),
        format="csv",
        sep=";",
        inferSchema=True,
        header=False
    ).toDF(*estabelecimentos_columns)

    return estabelecimentos_df, cnaes_df

if __name__ == "__main__":
    spark_session = get_spark_session()
    print("Sessão Spark iniciada.")
    
    estab_df, cnae_df = load_data(spark_session)
    
    print("Dados carregados com sucesso.")
    print("Schema de Estabelecimentos:")
    estab_df.printSchema()
    
    print("Schema de CNAEs:")
    cnae_df.printSchema()

    spark_session.stop()
    print("Sessão Spark finalizada.")
