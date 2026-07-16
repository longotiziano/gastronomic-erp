def load_initial_data():
    from services.bars import create_bar
    from services.users import create_user
    bar = create_bar(name="Bar 1", address="123 Main St")
    user = create_user(
        name="Admin",
        email="admin@example.com",
        password="adminpassword",
        role="administrator",
        bar_id=bar.id,
        address="Admin Address",
        daily_salary=0.0
    )