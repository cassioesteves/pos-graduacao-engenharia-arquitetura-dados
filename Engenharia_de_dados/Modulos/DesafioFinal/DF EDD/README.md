# 🚀 Desafio Final - Engenharia de Dados (Bootcamp)

Este repositório contém a resolução do Desafio Final do Bootcamp de Engenharia de Dados.

O tema do **Desafio Final** é a construção de Pipelines ETL com integração do **Apache Kafka** com um banco de dados **PostgreSQL** usando **Kafka Connect**, e entrega em Data Lake. Todos os serviços que compõem o Kafka e o database PostgreSQL (que servirá de fonte) serão implantados com **Docker Compose**.

Portanto, desenvolvemos uma solução prática de Engenharia de Dados que implementa a criação de pipelines ETL utilizando o modelo **Bronze, Silver e Gold**, processados com **Apache Spark SQL API** e integrados a um Data Lake no Amazon S3 via Kafka Connect.

## 🏗️ Arquitetura do Projeto

O pipeline de dados foi desenhado para simular um ambiente produtivo robusto, garantindo escalabilidade e confiabilidade.

```mermaid
graph LR
    API[API Tesouro Direto] -->|Python| PG[(PostgreSQL)]
    PG -->|CDC (JDBC Source)| Kafka[Apache Kafka]
    Kafka -->|S3 Sink Connector| S3_Bronze[(S3 - Bronze Layer)]
    S3_Bronze -->|Apache Spark| Spark[Processamento ETL]
    Spark -->|Limpeza| S3_Silver[(S3 - Silver Layer)]
    Spark -->|Agregação| S3_Gold[(S3 - Gold Layer)]
    S3_Gold -->|Spark SQL| Analytics[Análise de Dados]
```

## 🛠️ Tecnologias Utilizadas

*   **Linguagem**: Python 3.14
*   **Processamento Distribuído**: Apache Spark (PySpark)
*   **Streaming & Mensageria**: Apache Kafka & Kafka Connect
*   **Banco de Dados**: PostgreSQL
*   **Armazenamento (Data Lake)**: Amazon S3 (Simulado/Real)
*   **Orquestração/Ambiente**: Docker & Docker Compose
*   **Libs Auxiliares**: `boto3`, `pandas`, `sqlalchemy`, `dotenv`

## 📂 Estrutura do Projeto

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `docker-compose.yaml` | Definição dos serviços (Kafka, Postgres, Zookeeper, Workers). |
| `importar.ipynb` | **Ingestão**: Busca dados da API e salva no PostgreSQL (Gatilho do Pipeline). |
| `etl-spark.ipynb` | **Processamento**: Leitura do S3 (Bronze), tratamento (Silver) e agregação (Gold). |
| `spark_sql_pipeline.ipynb` | **Análise**: Consultas SQL para validar os dados processados e raw. |
| `connectors/` | Configurações dos conectores do Kafka (Source JDBC e Sink S3). |
| `.env_kafka_connect` | Variáveis de ambiente e credenciais sensíveis. |

## ⚙️ Como Executar

### 1. Preparar o Ambiente
Certifique-se de ter o **Docker** e **Python** instalados.
```bash
# Subir os containers (Kafka, Postgres, Connect)
docker-compose up -d

# Registrar os conectores do Kafka
./register_connectors.ps1
```

### 2. Ingestão de Dados
Execute o notebook `importar.ipynb`.
*   Ele fará o download dos dados do Tesouro Direto.
*   Inserirá os registros no PostgreSQL.
*   O Kafka Connect capturará as mudanças e enviará para o tópico e posteriormente para o S3 (Camada Bronze).

### 3. Processamento ETL
Execute o notebook `etl-spark.ipynb`.
*   Leitura dos dados brutos (JSON/Parquet) da camada **Bronze**.
*   Deduplicação e tipagem dão origem à camada **Silver**.
*   Agregações de negócio geram a camada **Gold**.

> **Nota**: Caso utilize Windows, configurações adicionais de `winutils` e `HADOOP_HOME` são aplicadas automaticamente no notebook.

### 4. Análise
Execute o notebook `spark_sql_pipeline.ipynb` para visualizar os insights gerados e validar a integridade dos dados entre as camadas.

## 📊 Resultados Alcançados

*   Pipeline de dados 100% automatizado via código.
*   Implementação de camadas de dados (Medallion Architecture).
*   Integração segura com AWS S3.
*   Monitoramento de fluxo via Kafka.

---
**Autor**: Cassio Esteves
*Engenheiro de Dados em Formação*
