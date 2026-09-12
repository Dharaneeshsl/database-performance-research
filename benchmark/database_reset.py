"""
Database Reset and Isolation Manager
Ensures baseline database state is restored before mutating runs.
"""

from loaders.postgres_loader import load_postgres_data
from loaders.mongo_loader import load_mongo_data

def reset_database_state(db_engine: str, data_dir: str):
    """Restores fresh dataset state for a given database engine."""
    print(f"Resetting baseline dataset state for {db_engine} from '{data_dir}'...")
    if db_engine == "postgresql":
        load_postgres_data(data_dir)
    elif db_engine == "mongodb":
        load_mongo_data(data_dir)
    else:
        raise ValueError(f"Unknown database engine: {db_engine}")
