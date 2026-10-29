
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import (
    BigInteger, String, Text, Float, Boolean
)

# 1. PostgreSQL connection details
USER = "postgres"
PASSWORD = "root"
HOST = "localhost"
PORT = "5432"
DB_NAME = "testdb"
TABLE_NAME = "pool_popularity"

# 2. Create database engine
engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)

try:
    # 3. Read local CSV file
    csv_file = "./pool_popularity.csv"
    df = pd.read_csv(csv_file)

    print("CSV loaded successfully:", df.shape)

    # 4. Define PostgreSQL column types
    column_types = {
        "pool_row": BigInteger(),
        "inchikey14": String(14),
        "pubchem_cid": BigInteger(),
        "smiles": Text(),
        "formula": String(100),
        "monoisotopic_mass": Float(),
        "log1p_substances": Float(),
        "log1p_pubmed": Float(),
        "log1p_patents": Float(),
        "pop": Float(),
        "substances_approx": BigInteger(),
        "pubmed_approx": BigInteger(),
        "patents_approx": BigInteger(),
        "np_coconut": Boolean(),
        "np_lotus": Boolean(),
        "np_npatlas": Boolean()
    }

    # 5. Create table and insert CSV records
    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False,
        dtype=column_types,
        chunksize=1000,
        method="multi"
    )

    print(f"Table '{TABLE_NAME}' created successfully.")
    print(f"Inserted {len(df)} records.")

    # 6. Verify inserted data
    with engine.connect() as conn:
        from sqlalchemy import text

        result = conn.execute(
            text(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        )
        print("Total database records:", result.scalar())

except Exception as error:
    print("Error:", error)

finally:
    engine.dispose()
    print("Database connection closed.")
