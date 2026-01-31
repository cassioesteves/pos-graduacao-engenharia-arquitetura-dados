-- Consultas OLTP (techstore.*)

-- 1) Total de vendas por mês (OLTP)
select
  date_trunc('month', p.data_pedido) as mes,
  sum(i.quantidade * i.preco_unitario) as receita
from techstore.pedidos p
join techstore.itens_pedido i on i.id_pedido = p.id_pedido
group by 1
order by 1;

-- 2) Top 10 produtos mais vendidos por quantidade (OLTP)
select
  pr.nome,
  sum(i.quantidade) as qtd
from techstore.itens_pedido i
join techstore.produtos pr on pr.id_produto = i.id_produto
group by pr.nome
order by qtd desc
limit 10;

-- 3) Faturamento por categoria (OLTP)
select
  c.nome as categoria,
  sum(i.quantidade * i.preco_unitario) as receita
from techstore.itens_pedido i
join techstore.produtos pr on pr.id_produto = i.id_produto
join techstore.categorias c on c.id_categoria = pr.id_categoria
group by c.nome
order by receita desc;

-- Consultas DW (dw_techstore.*) — preferíveis para análise

-- 1) Total de vendas por mês (DW)
select
  t.ano,
  t.mes,
  t.nome_mes,
  sum(f.receita) as receita
from dw_techstore.fato_vendas f
join dw_techstore.dim_tempo t on t.sk_tempo = f.sk_tempo
group by t.ano, t.mes, t.nome_mes
order by t.ano, t.mes;

-- 2) Top 10 produtos mais vendidos (quantidade) (DW)
select
  p.nome_produto,
  sum(f.quantidade) as qtd
from dw_techstore.fato_vendas f
join dw_techstore.dim_produto p on p.sk_produto = f.sk_produto
group by p.nome_produto
order by qtd desc
limit 10;

-- 3) Categorias com maior impacto no faturamento (DW)
select
  p.categoria,
  sum(f.receita) as receita
from dw_techstore.fato_vendas f
join dw_techstore.dim_produto p on p.sk_produto = f.sk_produto
group by p.categoria
order by receita desc;
