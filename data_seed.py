from services.bars import BarService
from services.products import ProductService, ProductCategoryService
from services.raw_materials import RawMaterialService, RawMaterialCategoryService
from services.recipes import RecipeService
from services.users import UserService

# ==========================================
# 1. BARES (id: 1, 2, 3)
# ==========================================
bars = [
    {"name": "Club Serrano - Palermo", "address": "Serrano 1551, CABA"},
    {"name": "Club Serrano - Recoleta", "address": "Vicente López 2100, CABA"},
    {"name": "Club Serrano - Belgrano", "address": "Cabildo 2400, CABA"},
]

# ==========================================
# 2. CATEGORÍAS DE MATERIAS PRIMAS (id: 1, 2, 3, 4, 5)
# ==========================================
rmcs = [
    {"name": "Carnes y Fiambrería"},
    {"name": "Verdulería y Frescos"},
    {"name": "Lácteos y Quesos"},
    {"name": "Panadería y Masas"},
    {"name": "Bebidas e Insumos de Barra"},
]

# ==========================================
# 3. MATERIAS PRIMAS
# ==========================================
rms = [
    # Carnes (category_id: 1)
    {"name": "Carne Picada Especial", "category_id": 1},
    {"name": "Pechuga de Pollo", "category_id": 1},
    {"name": "Panceta Ahumada", "category_id": 1},
    {"name": "Jamón Cocido", "category_id": 1},
    
    # Verduras (category_id: 2)
    {"name": "Tomate Redondo", "category_id": 2},
    {"name": "Lechuga Capuchina", "category_id": 2},
    {"name": "Cebolla Morada", "category_id": 2},
    {"name": "Limón", "category_id": 2},
    {"name": "Menta Fresca", "category_id": 2},

    # Lácteos (category_id: 3)
    {"name": "Queso Cheddar", "category_id": 3},
    {"name": "Queso Mozzarella", "category_id": 3},
    {"name": "Crema de Leche", "category_id": 3},

    # Panadería (category_id: 4)
    {"name": "Pan de Brioche", "category_id": 4},
    {"name": "Pan de Papa", "category_id": 4},
    {"name": "Prepizza Individual", "category_id": 4},

    # Bebidas Insumo (category_id: 5)
    {"name": "Gin Apostoles 750ml", "category_id": 5},
    {"name": "Fernet Branca 750ml", "category_id": 5},
    {"name": "Vodka Smirnoff 700ml", "category_id": 5},
    {"name": "Agua Tónica 1.5L", "category_id": 5},
    {"name": "Coca Cola 1.5L", "category_id": 5},
]

# ==========================================
# 4. CATEGORÍAS DE PRODUCTOS (id: 1, 2, 3, 4, 5)
# ==========================================
p_cats = [
    {"name": "Hamburguesas", "sector": "kitchen"},
    {"name": "Pizzas y Minutas", "sector": "kitchen"},
    {"name": "Coctelería de Autor", "sector": "bar"},
    {"name": "Tragos Clásicos", "sector": "bar"},
    {"name": "Cervezas y Sin Alcohol", "sector": "bar"},
]

# ==========================================
# 5. PRODUCTOS (Vincular category_id y bar_id)
# ==========================================
prods = [
    # Hamburguesas (Cocina / category_id: 1)
    {"name": "Cheeseburger Doble", "category_id": 1, "price": 8500.0, "bar_id": 1},
    {"name": "Serrana Burger (Bacon)", "category_id": 1, "price": 9800.0, "bar_id": 1},
    {"name": "Veggie Burger", "category_id": 1, "price": 7900.0, "bar_id": 2},
    
    # Pizzas (Cocina / category_id: 2)
    {"name": "Pizza Mozzarella", "category_id": 2, "price": 11000.0, "bar_id": 1},
    {"name": "Papas Serrano con Cheddar", "category_id": 2, "price": 6500.0, "bar_id": 2},

    # Coctelería (Barra / category_id: 3)
    {"name": "Gin Tonic Serrano", "category_id": 3, "price": 5500.0, "bar_id": 1},
    {"name": "Passion Vodka", "category_id": 3, "price": 5800.0, "bar_id": 3},

    # Clásicos (Barra / category_id: 4)
    {"name": "Fernet con Coca", "category_id": 4, "price": 4800.0, "bar_id": 1},
    {"name": "Negroni Clásico", "category_id": 4, "price": 5200.0, "bar_id": 2},
    {"name": "Mojito", "category_id": 4, "price": 5000.0, "bar_id": 3},

    # Cervezas/Bebidas (Barra / category_i  d: 5)
    {"name": "Pinta IPA", "category_id": 5, "price": 3800.0, "bar_id": 1},
    {"name": "Pinta Honey", "category_id": 5, "price": 3600.0, "bar_id": 2},
    {"name": "Coca Cola 354ml", "category_id": 5, "price": 2200.0, "bar_id": 1},
]

# ==========================================
# 5.1 RECETAS (product_id -> lista de {raw_material_id, amount})
# ==========================================
recipes = [
    # Cheeseburger Doble (product_id: 1)
    {"product_id": 1, "raw_material_id": 1, "amount": 0.180},   # Carne Picada Especial (kg)
    {"product_id": 1, "raw_material_id": 10, "amount": 0.050},  # Queso Cheddar (kg)
    {"product_id": 1, "raw_material_id": 13, "amount": 1},      # Pan de Brioche (unidad)

    # Serrana Burger - Bacon (product_id: 2)
    {"product_id": 2, "raw_material_id": 1, "amount": 0.180},   # Carne Picada Especial
    {"product_id": 2, "raw_material_id": 3, "amount": 0.040},   # Panceta Ahumada
    {"product_id": 2, "raw_material_id": 10, "amount": 0.050},  # Queso Cheddar
    {"product_id": 2, "raw_material_id": 13, "amount": 1},      # Pan de Brioche

    # Veggie Burger (product_id: 3)
    {"product_id": 3, "raw_material_id": 6, "amount": 0.030},   # Lechuga Capuchina
    {"product_id": 3, "raw_material_id": 5, "amount": 0.050},   # Tomate Redondo
    {"product_id": 3, "raw_material_id": 13, "amount": 1},      # Pan de Brioche

    # Pizza Mozzarella (product_id: 4)
    {"product_id": 4, "raw_material_id": 15, "amount": 1},      # Prepizza Individual
    {"product_id": 4, "raw_material_id": 11, "amount": 0.150},  # Queso Mozzarella
    {"product_id": 4, "raw_material_id": 5, "amount": 0.080},   # Tomate Redondo

    # Papas Serrano con Cheddar (product_id: 5)
    {"product_id": 5, "raw_material_id": 10, "amount": 0.100},  # Queso Cheddar
    {"product_id": 5, "raw_material_id": 3, "amount": 0.030},   # Panceta Ahumada

    # Gin Tonic Serrano (product_id: 6)
    {"product_id": 6, "raw_material_id": 16, "amount": 0.050},  # Gin Apostoles 750ml (L)
    {"product_id": 6, "raw_material_id": 19, "amount": 0.200},  # Agua Tónica 1.5L (L)
    {"product_id": 6, "raw_material_id": 9, "amount": 2},       # Menta Fresca (hojas/unidad)

    # Passion Vodka (product_id: 7)
    {"product_id": 7, "raw_material_id": 18, "amount": 0.050},  # Vodka Smirnoff 700ml
    {"product_id": 7, "raw_material_id": 8, "amount": 0.5},     # Limón

    # Fernet con Coca (product_id: 8)
    {"product_id": 8, "raw_material_id": 17, "amount": 0.070},  # Fernet Branca 750ml
    {"product_id": 8, "raw_material_id": 20, "amount": 0.250},  # Coca Cola 1.5L

    # Negroni Clásico (product_id: 9)
    {"product_id": 9, "raw_material_id": 16, "amount": 0.030},  # Gin Apostoles 750ml
    {"product_id": 9, "raw_material_id": 8, "amount": 0.5},     # Limón

    # Mojito (product_id: 10)
    {"product_id": 10, "raw_material_id": 18, "amount": 0.050}, # Vodka Smirnoff 700ml (o ron, ajustar si tenés esa MP)
    {"product_id": 10, "raw_material_id": 9, "amount": 5},      # Menta Fresca
    {"product_id": 10, "raw_material_id": 8, "amount": 0.5},    # Limón

    # Pinta IPA, Pinta Honey, Coca Cola 354ml -> sin receta (venta directa, sin transformación)
]

# ==========================================
# 6. USUARIOS (Roles: waiter, administrator, cashier, manager)
# ==========================================
users = [
    {
        "name": "Peter",
        "address": "Av. Corrientes 1234, CABA",
        "email": "admin@a.com",
        "password": "password",
        "daily_salary": 25000.0,
        "leave_at": None,
        "rol": "administrator"
    },
    {
        "name": "Gonzalo Admin",
        "address": "Av. Corrientes 1234, CABA",
        "email": "admin@clubserrano.com",
        "password": "Password123!",
        "daily_salary": 25000.0,
        "leave_at": None,
        "rol": "administrator",
        "confirm_password": "Password123!"
    },
    {
        "name": "Sofia Gerente",
        "address": "Av. Santa Fe 3000, CABA",
        "email": "sofia.manager@clubserrano.com",
        "password": "Password123!",
        "daily_salary": 20000.0,
        "leave_at": None,
        "rol": "manager",
        "confirm_password": "Password123!"
    },
    {
        "name": "Carlos Cajero",
        "address": "Thames 1800, CABA",
        "email": "carlos.cashier@clubserrano.com",
        "password": "Password123!",
        "daily_salary": 15000.0,
        "leave_at": None,
        "rol": "cashier",
        "confirm_password": "Password123!"
    },
    {
        "name": "Mateo Mozo",
        "address": "Honduras 4500, CABA",
        "email": "mateo.waiter@clubserrano.com",
        "password": "Password123!",
        "daily_salary": 12000.0,
        "leave_at": None,
        "rol": "waiter",
        "confirm_password": "Password123!"
    },
    {
        "name": "Lucia Moza (Ex Empleada)",
        "address": "Scalabrini Ortiz 900, CABA",
        "email": "lucia.ex@clubserrano.com",
        "password": "Password123!",
        "daily_salary": 12000.0,
        "leave_at": "2024-01-15",
        "rol": "waiter",
        "confirm_password": "Password123!"
    }
]

# ==========================================
# EJECUCIÓN
# ==========================================
print("Poblando la base de datos...")

def load_initial_data():
    for bar in bars:
        BarService().create(**bar)

    for rmc in rmcs:
        RawMaterialCategoryService().create(**rmc)

    for rm in rms:
        RawMaterialService().create(**rm)

    for p_cat in p_cats:
        ProductCategoryService().create(**p_cat)

    for prod in prods:
        ProductService().create(**prod)

    for recipe in recipes: 
        RecipeService().create(**recipe)

    for user in users:
        UserService().create(**user)

print("¡Registros creados perfectamente! 🚀")               