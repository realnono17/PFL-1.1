from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///pfl.db")  # make sure this path is correct
inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tables in the database:", tables)
