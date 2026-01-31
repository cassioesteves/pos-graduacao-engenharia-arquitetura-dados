-- DDL relacional (ANSI/PostgreSQL compatível)

create schema if not exists techstore;

-- Nota geral sobre chaves:
-- - PK: única por tabela (pode ser composta) e não aceita NULL.
-- - FK: referencia PK (ou UNIQUE/candidate key) da tabela pai para garantir integridade referencial.

-- Domínios/opcionais: validar formatos simples
-- create domain cpf as varchar(11) check (value ~ '^[0-9]{11}$');

create table if not exists techstore.clientes (
  id_cliente           bigserial primary key,
  nome                 varchar(150) not null,
  cpf                  varchar(14)  not null,  -- pode armazenar com máscara
  endereco             varchar(255) not null,
  telefone             varchar(20)  not null,
  email                varchar(150) not null,
  constraint uk_clientes_cpf unique (cpf),
  constraint uk_clientes_email unique (email)
);

create table if not exists techstore.fabricantes (
  id_fabricante        bigserial primary key,
  nome                 varchar(120) not null,
  constraint uk_fabricantes_nome unique (nome)
);

create table if not exists techstore.categorias (
  id_categoria         bigserial primary key,
  nome                 varchar(120) not null,
  constraint uk_categorias_nome unique (nome)
);

create table if not exists techstore.produtos (
  id_produto           bigserial primary key,  -- PK substituta (surrogate)
  codigo_sku           varchar(40)  not null,
  nome                 varchar(150) not null,
  descricao            text         not null,
  id_categoria         bigint       not null references techstore.categorias(id_categoria),
  id_fabricante        bigint       not null references techstore.fabricantes(id_fabricante),
  preco                numeric(12,2) not null check (preco >= 0),
  constraint uk_produtos_sku unique (codigo_sku) -- Chave natural única (código do produto)
);

create index if not exists ix_produtos_categoria on techstore.produtos(id_categoria);
create index if not exists ix_produtos_fabricante on techstore.produtos(id_fabricante);

create table if not exists techstore.estoques (
  id_estoque    bigserial primary key,
  id_produto    bigint not null references techstore.produtos(id_produto) on delete cascade,
  quantidade    integer not null default 0 check (quantidade >= 0),
  constraint uk_estoques_produto unique (id_produto) -- 1:1 com produto; garante unicidade por produto
);

create table if not exists techstore.pedidos (
  id_pedido            bigserial primary key,
  numero_pedido        varchar(30) not null,
  data_pedido          timestamp   not null,
  -- 1:N (Cliente 1 -> N Pedidos): FK no lado "muitos" (pedidos) apontando para a PK de clientes
  id_cliente           bigint      not null references techstore.clientes(id_cliente), -- FK: integridade referencial com techstore.clientes(id_cliente)
  valor_total          numeric(14,2) not null check (valor_total >= 0),
  constraint uk_pedidos_numero unique (numero_pedido)
);

create index if not exists ix_pedidos_cliente on techstore.pedidos(id_cliente);
create index if not exists ix_pedidos_data on techstore.pedidos(data_pedido);

-- Tabela associativa (M:N) entre pedidos e produtos
create table if not exists techstore.itens_pedido (
  id_item              bigserial primary key,
  -- FKs: asseguram integridade com pedidos e produtos
  id_pedido            bigint not null references techstore.pedidos(id_pedido) on delete cascade,
  id_produto           bigint not null references techstore.produtos(id_produto),
  quantidade           integer not null check (quantidade > 0),
  preco_unitario       numeric(12,2) not null check (preco_unitario >= 0),
  constraint uk_itens_pedido unique (id_pedido, id_produto) -- UK composta: evita o mesmo produto repetido no mesmo pedido
);

create index if not exists ix_itens_pedido_produto on techstore.itens_pedido(id_produto);

-- Observação:
-- valor_total do pedido deve ser a soma(quantidade*preco_unitario) dos itens.
-- Em produção, considerar view ou trigger para consistência.
