// Diagrama do Modelo Relacional para AMAZONAS_DB
// Importe este codigo em https://dbdiagram.io/d para visualizar a ilustracao vetorial do banco de dados

Table customers {
  _id objectId [pk]
  customer_id string [unique, not null]
  name string
  email string
  phone string
  street string
  city string
  state string
  zip_code string
  registration_date date
  preferences string[]
  status string
}

Table products {
  _id objectId [pk]
  product_id string [unique, not null]
  name string
  description string
  price decimal
  category string
  brand string
  stock_quantity int
  processor string
  ram string
  storage string
  screen string
  image_url string
  created_at date
}

Table orders {
  _id objectId [pk]
  order_id string [unique, not null]
  customer_id string [ref: > customers.customer_id]
  name string
  email string
  subtotal decimal
  shipping_cost decimal
  total decimal
  status string
  order_date date
  street string
  city string
  state string
  zip_code string
  payment_status string
}

Table order_items {
  _id objectId [pk]
  order_id string [ref: > orders.order_id]
  product_id string [ref: > products.product_id]
  name string
  quantity int
  unit_price decimal
  total decimal
}

Table cart_items {
  _id objectId [pk]
  cart_id string [unique, not null]
  customer_id string [ref: > customers.customer_id]
  product_id string [ref: > products.product_id]
  name string
  price decimal
  image_url string
  quantity int
  unit_price decimal
  total_price decimal
  added_at date
}

Table product_reviews {
  _id objectId [pk]
  review_id string [unique, not null]
  product_id string [ref: > products.product_id]
  customer_id string [ref: > customers.customer_id]
  customer_name string
  rating int
  comment string
  review_date date
  helpful_count int
  verified_purchase boolean
}

// Remova a seção de relacionamentos duplicada abaixo
// pois os relacionamentos já foram definidos acima com [ref: >]