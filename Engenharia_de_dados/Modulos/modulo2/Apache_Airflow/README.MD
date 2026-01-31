# Pipeline ETL com Apache Airflow

Este projeto implementa um pipeline de ETL (Extração, Transformação e Carga) completo utilizando **Apache Airflow**, orquestrando a ingestão de dados de um **Bucket S3 (AWS)** para um banco de dados **PostgreSQL**.

## 🎯 Objetivos
*   **Orquestração de Dados**: Automatizar o fluxo de dados entre nuvem e ambiente local/containerizado.
*   **Ingestão de Arquivos**: Leitura de dados armazenados no AWS S3.
*   **Armazenamento Estruturado**: Carga dos dados processados em tabelas relacionais no PostgreSQL.
*   **Ambiente Reprodutível**: Uso de Docker para isolamento e facilidade de execução.

## 🛠️ Stack Tecnológica
*   **Orquestração**: Apache Airflow 2.x
*   **Containerização**: Docker & Docker Compose
*   **Banco de Dados**: PostgreSQL
*   **Fonte de Dados**: AWS S3
*   **Linguagem**: Python

## 📂 Estrutura do Projeto
*   `0-Arquivos dags/`: Contém as definições dos pipelines (DAGs) do Airflow.
*   `Airflow*/`: Configurações locais e ambientes do Airflow.
*   `mysql-connector*/`: Drivers de conexão (se aplicável).

## 🚀 Como Executar
1.  **Pré-requisitos**: Docker e Docker Compose instalados.
2.  **Configuração**:
    *   Defina as credenciais da AWS e conexão com Postgres no Airflow (Admin -> Connections).
3.  **Subir o Ambiente**:
    ```bash
    docker-compose up -d
    ```
4.  **Acessar o Airflow**:
    *   Navegue para `http://localhost:8080`.
    *   Ative a DAG correspondente para iniciar o processo ETL.

---
*Projeto desenvolvido como parte do Bootcamp de Engenharia de Dados (XP Educação).*