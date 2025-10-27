# 🏗️ Desafio Final - Arquitetura de Dados

Este repositório contém a solução para o Desafio Final do Bootcamp de Arquiteto(a) de Dados, focado no projeto de uma arquitetura de dados escalável para um e-commerce fictício chamado "Amazonas".

O foco deste projeto está na documentação da arquitetura, na modelagem de dados NoSQL e na estratégia de escalabilidade.

## 🛠️ Tecnologias Utilizadas

- 🍃 MongoDB: Banco de Dados NoSQL orientado a documentos, escolhido para a modelagem dos dados.

## 🏛️ Arquitetura

O diagrama abaixo representa a arquitetura conceitual da solução proposta:

![Diagrama da Arquitetura](Diagrama/diagrama.svg)

## 📂 Entregáveis do Projeto

Todos os artefatos do projeto estão organizados nas seguintes pastas:

### 1. 📄 Documento de Arquitetura (Entregável Principal)

O documento completo com a descrição do sistema, a arquitetura proposta, a modelagem detalhada das coleções e o plano de escalabilidade pode ser encontrado em:

- **/docs/Documento_Arquitetural.md**

### 2. 📜 Script do Banco de Dados (Opcional)

Como um entregável opcional, foi criado um script para popular uma instância do MongoDB com dados fictícios, permitindo a validação do modelo de dados.

- **Arquivo:** `/database/criar-banco-dados.js`
- **Como usar:**
  1. Tenha acesso a uma instância do MongoDB (local ou na nuvem).
  2. Execute o script usando o `mongosh`, passando a sua string de conexão.
  ```bash
  mongosh "mongodb://seu_usuario:sua_senha@seu_host:sua_porta" < database/criar-banco-dados.js
  ```
  *Se estiver rodando o MongoDB localmente sem autenticação, o comando pode ser mais simples:*
  ```bash
  mongosh < database/criar-banco-dados.js
  ```

### 3. 💎 Modelos de Dados para Hackolade

Para facilitar a visualização e a importação do modelo de dados na ferramenta Hackolade, foram criados arquivos JSON para cada uma das coleções.

- **Pasta:** `/modelagem-hackolade/`
- **Conteúdo:** Arquivos `.json` representando a estrutura de cada coleção.

### 4. 🖼️ Diagramas do Modelo de Dados

As imagens dos diagramas de dados geradas a partir do Hackolade estão localizadas em:

- **Pasta:** `/print/`
- **Conteúdo:** Arquivos `.png` com o modelo visual de cada coleção.

## 🌳 Estrutura do Projeto

```
/DesafioFinal
├── /database
│   └── criar-banco-dados.js
├── /Diagrama
│   └── diagrama.svg
├── /docs
│   └── Documento_Arquitetural.md
├── /modelagem-hackolade
│   ├── cart_items.json
│   ├── customers.json
│   ├── orders.json
│   ├── product_reviews.json
│   └── products.json
├── /print
│   ├── cart_items_model.png
│   ├── customers_model.png
│   ├── orders_model.png
│   ├── product_reviews_model.png
│   └── products_model.png
└── README.md
```

---

**Autor**

Cássio Esteves

📧 Email: cassio.esteves@hotmail.com  
💼 LinkedIn: https://www.linkedin.com/in/cassioesteves/  
🐙 GitHub: https://github.com/cassioesteves
