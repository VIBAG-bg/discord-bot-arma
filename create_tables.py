from database.db import Base, engine
from database.models import User

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")