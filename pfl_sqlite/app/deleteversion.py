from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./pfl.db")
with engine.connect() as conn:
    conn.execute(text("DELETE FROM alembic_version"))
    conn.commit()
