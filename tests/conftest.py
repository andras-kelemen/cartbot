import os

# Ensures cartbot.bot uses an in-memory DB when imported during tests
os.environ.setdefault("DB_PATH", ":memory:")
