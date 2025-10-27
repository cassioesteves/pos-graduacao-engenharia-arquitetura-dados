// Script para criar e popular o banco de dados "amazonas_db" em uma instância MongoDB.
// Como usar: mongosh "sua_string_de_conexao" < criar-banco-dados.js

// Seleciona ou cria o banco de dados
use amazonas_db;

// Limpa dados antigos (opcional, mas recomendado para um estado limpo)
db.customers.deleteMany({});
db.products.deleteMany({});
db.orders.deleteMany({});
db.cart_items.deleteMany({});
db.product_reviews.deleteMany({});

print("Coleções antigas limpas.");

// --- Inserindo Novos Dados ---

// 1. CUSTOMERS
db.customers.insertMany([
  {
    customer_id: "CUST101",
    name: "Ana Pereira",
    email: "ana.pereira@example.com",
    phone: "+55 31 91234-5678",
    address: {
      street: "Rua da Bahia, 1000",
      city: "Belo Horizonte",
      state: "MG",
      zip_code: "30160-011"
    },
    registration_date: new Date("2024-02-10"),
    preferences: ["home", "books"],
    status: "active"
  },
  {
    customer_id: "CUST102",
    name: "Bruno Lima",
    email: "bruno.lima@example.com",
    phone: "+55 71 98765-4321",
    address: {
      street: "Av. Sete de Setembro, 200",
      city: "Salvador",
      state: "BA",
      zip_code: "40060-001"
    },
    registration_date: new Date("2024-03-05"),
    preferences: ["clothing", "electronics"],
    status: "active"
  },
  {
    customer_id: "CUST103",
    name: "Carla Dias",
    email: "carla.dias@example.com",
    phone: "+55 41 99999-8888",
    address: {
      street: "Rua XV de Novembro, 300",
      city: "Curitiba",
      state: "PR",
      zip_code: "80020-310"
    },
    registration_date: new Date("2024-04-01"),
    preferences: ["books", "electronics"],
    status: "inactive"
  }
]);

print("Coleção 'customers' populada.");

// 2. PRODUCTS
db.products.insertMany([
  {
    product_id: "PROD101",
    name: "Monitor Gamer LG UltraGear 27\"",
    description: "Monitor Full HD, 144Hz, 1ms, IPS com HDR10",
    price: 1899.90,
    category: "Electronics",
    brand: "LG",
    stock_quantity: 15,
    attributes: {
      size: "27 polegadas",
      resolution: "1920x1080",
      refresh_rate: "144Hz",
      panel_type: "IPS"
    },
    image_url: "https://example.com/images/prod101.jpg",
    created_at: new Date("2024-01-20")
  },
  {
    product_id: "PROD102",
    name: "Tênis Adidas Coreracer",
    description: "Tênis de corrida leve e respirável",
    price: 279.99,
    category: "Clothing",
    brand: "Adidas",
    stock_quantity: 80,
    attributes: {
      material: "Malha",
      sizes: ["38", "39", "40", "41", "42"],
      color: "Azul Marinho"
    },
    image_url: "https://example.com/images/prod102.jpg",
    created_at: new Date("2024-02-15")
  },
  {
    product_id: "PROD103",
    name: "Livro: O Hobbit",
    description: "Uma jornada inesperada por J.R.R. Tolkien",
    price: 49.90,
    category: "Books",
    brand: "HarperCollins",
    stock_quantity: 120,
    attributes: {
      author: "J.R.R. Tolkien",
      publisher: "HarperCollins",
      pages: 336,
      language: "Português"
    },
    image_url: "https://example.com/images/prod103.jpg",
    created_at: new Date("2024-01-15")
  },
  {
    product_id: "PROD104",
    name: "Cafeteira Elétrica Oster",
    description: "Cafeteira programável com jarra de vidro para 36 xícaras",
    price: 249.90,
    category: "Home",
    brand: "Oster",
    stock_quantity: 30,
    attributes: {
      capacity: "1.8L",
      power: "900W",
      programmable: "Sim"
    },
    image_url: "https://example.com/images/prod104.jpg",
    created_at: new Date("2024-03-01")
  },
  {
    product_id: "PROD105",
    name: "Webcam Logitech C920",
    description: "Webcam Full HD 1080p para videochamadas",
    price: 499.99,
    category: "Electronics",
    brand: "Logitech",
    stock_quantity: 40,
    attributes: {
      resolution: "1080p",
      focus_type: "Autofoco",
      microphone: "Estéreo embutido"
    },
    image_url: "https://example.com/images/prod105.jpg",
    created_at: new Date("2024-02-25")
  }
]);

print("Coleção 'products' populada.");

// 3. ORDERS
db.orders.insertMany([
  {
    order_id: "ORD101",
    customer_id: "CUST101",
    customer_info: {
      name: "Ana Pereira",
      email: "ana.pereira@example.com"
    },
    items: [
      {
        product_id: "PROD101",
        name: "Monitor Gamer LG UltraGear 27\"",
        quantity: 1,
        unit_price: 1899.90,
        total: 1899.90
      }
    ],
    subtotal: 1899.90,
    shipping_cost: 75.50,
    total: 1975.40,
    status: "shipped",
    order_date: new Date("2024-04-10"),
    shipping_address: {
      street: "Rua da Bahia, 1000",
      city: "Belo Horizonte",
      state: "MG",
      zip_code: "30160-011"
    },
    payment_status: "paid"
  },
  {
    order_id: "ORD102",
    customer_id: "CUST102",
    customer_info: {
      name: "Bruno Lima",
      email: "bruno.lima@example.com"
    },
    items: [
      {
        product_id: "PROD102",
        name: "Tênis Adidas Coreracer",
        quantity: 1,
        unit_price: 279.99,
        total: 279.99
      },
      {
        product_id: "PROD104",
        name: "Cafeteira Elétrica Oster",
        quantity: 1,
        unit_price: 249.90,
        total: 249.90
      }
    ],
    subtotal: 529.89,
    shipping_cost: 45.00,
    total: 574.89,
    status: "delivered",
    order_date: new Date("2024-04-12"),
    shipping_address: {
      street: "Av. Sete de Setembro, 200",
      city: "Salvador",
      state: "BA",
      zip_code: "40060-001"
    },
    payment_status: "paid"
  }
]);

print("Coleção 'orders' populada.");

// 4. CART_ITEMS
db.cart_items.insertMany([
  {
    cart_id: "CART101",
    customer_id: "CUST103",
    product_id: "PROD103",
    product_info: {
      name: "Livro: O Hobbit",
      price: 49.90,
      image_url: "https://example.com/images/prod103.jpg"
    },
    quantity: 1,
    unit_price: 49.90,
    total_price: 49.90,
    added_at: new Date("2024-04-20")
  },
  {
    cart_id: "CART102",
    customer_id: "CUST101",
    product_id: "PROD105",
    product_info: {
      name: "Webcam Logitech C920",
      price: 499.99,
      image_url: "https://example.com/images/prod105.jpg"
    },
    quantity: 1,
    unit_price: 499.99,
    total_price: 499.99,
    added_at: new Date("2024-04-22")
  }
]);

print("Coleção 'cart_items' populada.");

// 5. PRODUCT_REVIEWS
db.product_reviews.insertMany([
  {
    review_id: "REV101",
    product_id: "PROD101",
    customer_id: "CUST101",
    customer_name: "Ana Pereira",
    rating: 5,
    comment: "Imagem incrível, os 144Hz fazem muita diferença nos jogos!",
    review_date: new Date("2024-04-18"),
    helpful_count: 25,
    verified_purchase: true
  },
  {
    review_id: "REV102",
    product_id: "PROD102",
    customer_id: "CUST102",
    customer_name: "Bruno Lima",
    rating: 4,
    comment: "Muito confortável para corridas leves, mas a cor é um pouco mais escura do que na foto.",
    review_date: new Date("2024-04-20"),
    helpful_count: 15,
    verified_purchase: true
  }
]);

print("Coleção 'product_reviews' populada.");

print("\nBanco de dados 'amazonas_db' populado com sucesso!");

print("Total de documentos por coleção:");
print("Customers: " + db.customers.countDocuments());
print("Products: " + db.products.countDocuments());
print("Orders: " + db.orders.countDocuments());
print("Cart Items: " + db.cart_items.countDocuments());
print("Reviews: " + db.product_reviews.countDocuments());
