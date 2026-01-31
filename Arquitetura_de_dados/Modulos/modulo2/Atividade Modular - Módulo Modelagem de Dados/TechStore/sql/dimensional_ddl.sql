-- DDL dimensional (Data Warehouse)
-- Modelo adotado: Estrela (dimensões desnormalizadas).
-- Em Floco de Neve, categoria/fabricante seriam tabelas de dimensão próprias
-- e Dim_Produto teria FKs para essas tabelas (dimensões normalizadas).
-- Estrela: menos tabelas e menos junções; Floco de Neve: mais tabelas e mais junções.
-- Pergunta 12: No Floco de Neve, dimensões podem estar normalizadas para reduzir redundâncias (mais tabelas/joins).

create schema if not exists dw_techstore;

create table if not exists dw_techstore.dim_tempo (
  sk_tempo     serial primary key,
  data         date not null unique,
  dia          int  not null,
  mes          int  not null,
  ano          int  not null,
  trimestre    int  not null,
  semestre     int  not null,
  nome_mes     varchar(20) not null,
  nome_dia     varchar(20) not null
);
-- Hierarquia temporal: Ano > Semestre > Trimestre > Mês > Dia (suporta drill-down/roll-up)

create unique index if not exists ux_dim_tempo_data on dw_techstore.dim_tempo(data);

create table if not exists dw_techstore.dim_produto (
  sk_produto         serial primary key,
  id_produto_natural bigint,
  codigo_sku         varchar(40),
  nome_produto       varchar(150),
  categoria          varchar(120),
  fabricante         varchar(120)
);

create table if not exists dw_techstore.dim_cliente (
  sk_cliente         serial primary key,
  id_cliente_natural bigint,
  nome               varchar(150),
  cpf                varchar(14),
  email              varchar(150),
  cidade             varchar(120),
  uf                 varchar(2)
);

create table if not exists dw_techstore.fato_vendas (
  sk_fato        bigserial primary key,
  sk_tempo       int not null references dw_techstore.dim_tempo(sk_tempo),
  sk_produto     int not null references dw_techstore.dim_produto(sk_produto),
  sk_cliente     int not null references dw_techstore.dim_cliente(sk_cliente),
  numero_pedido  varchar(30),
  quantidade     integer not null check (quantidade > 0),
  preco_unitario numeric(12,2) not null check (preco_unitario >= 0),
  receita        numeric(14,2) not null check (receita >= 0)
);

-- Medida principal: quantidade vendida no nível do item do pedido
comment on column dw_techstore.fato_vendas.quantidade is 'Medida (fato): quantidade vendida no item do pedido';
comment on table dw_techstore.fato_vendas is 'Tabela Fato do processo de vendas: contém medidas (quantidade, preço unitário, receita) e FKs para dimensões';

create index if not exists ix_fato_vendas_tempo on dw_techstore.fato_vendas(sk_tempo);
create index if not exists ix_fato_vendas_produto on dw_techstore.fato_vendas(sk_produto);
create index if not exists ix_fato_vendas_cliente on dw_techstore.fato_vendas(sk_cliente);

-- Notas de carga (ETL) resumidas:
-- - Mapear pedidos/itens do OLTP para FATO_VENDAS (grão = item do pedido).
-- - Preencher DIM_TEMPO por calendário.
-- - DIM_PRODUTO e DIM_CLIENTE a partir dos cadastros (incluindo SK e chaves naturais).
-- - receita = quantidade * preco_unitario no momento da venda.
