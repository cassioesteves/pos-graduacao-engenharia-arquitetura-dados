# Processamento de Big Data com Apache Spark (Dados Públicos de CNPJ)

Este projeto demonstra a aplicação de **Engenharia de Dados** e **Processamento Distribuído** utilizando **Apache Spark (PySpark)** para analisar grandes volumes de dados públicos da Receita Federal (CNPJ e Estabelecimentos).

## 🎯 Objetivos do Projeto
*   **Ingestão de Dados Massivos**: Leitura de múltiplos arquivos CSV contendo milhões de registros de empresas brasileiras.
*   **Otimização de Armazenamento**: Conversão de dados brutos (CSV) para formato coluna comprimido (**Parquet**) para ganho de performance e redução de custos de armazenamento.
*   **Análise Exploratória via Spark SQL**: Execução de consultas complexas utilizando SQL distribuído e DataFrames.
*   **Qualidade de Dados (Data Quality)**: Implementação de UDFs (User Defined Functions) para validação e limpeza de dados (ex: padronização de logradouros).

## 🛠️ Tecnologias Utilizadas
*   **Apache Spark**: Motor de processamento unificado para Big Data.
*   **PySpark**: Interface Python para Spark.
*   **Spark SQL**: Módulo para processamento de dados estruturados.
*   **Parquet**: Formato de armazenamento colunar eficiente.
*   **Python**: Linguagem de script e análise.

## 📊 Principais Análises Realizadas
O script `analise_spark.py` respondeu a questões estratégicas sobre a base de dados:
1.  **Volumetria**: Contagem total de estabelecimentos ativos (> 20 milhões).
2.  **Schema Inference**: Validação automática de tipos de dados.
3.  **Benchmark de Compressão**: Comparação entre CSV e Parquet (demonstrando redução de ~2.5x no tamanho).
4.  **Qualidade de Endereços**: Identificação de inconsistências em logradouros (ex: redundância de termos como "AVENIDA").
5.  **Cruzamento de Dados (Joins)**: Associação entre Estabelecimentos e CNAEs (Atividades Econômicas) para segmentação de mercado (ex: setor de Cultivo).

## 🚀 Como Executar

### Pré-requisitos
*   Python 3.8+
*   Apache Spark instalado localmente ou cluster (Databricks/EMR)
*   Bibliotecas: `pyspark`, `numpy`

### Passos
1.  **Setup do Ambiente**:
    ```bash
    pip install pyspark
    ```
2.  **Execução da Análise**:
    ```bash
    python analise_spark.py
    ```

## 📈 Resultados Chave
*   Identificação de **1.093.082** filiais em operação.
*   Mapeamento de **889.886** CEPs distintos.
*   Análise de performance confirmando a eficiência do **Parquet** sobre grandes volumes de texto plano.

---
*Projeto desenvolvido como parte do Bootcamp de Engenharia de Dados (XP Educação).*
