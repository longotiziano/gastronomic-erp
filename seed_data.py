def load_initial_data():
    from services.bars import create_bar
    from services.raw_materials_categories import create_raw_material_category
    from services.raw_materials import create_raw_material
    from services.users import create_user
    from database.repositories.bars import BarRepository

    bar_repo = BarRepository()
    bar = bar_repo.get_by_name_case_insensitive("Bar 1")
    if bar is None:
        bar = create_bar(name="Bar 1", address="123 Main St")

    create_user(
        name="Admin",
        email="admin@example.com",
        password="adminpassword",
        role="administrator",
        bar_id=bar.id,
        address="Admin Address",
        daily_salary=0.0
    )

    create_raw_material_category("Carnes")
    create_raw_material("Carne picada", 1)
