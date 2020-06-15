import sqlite3
import pandas as pd

conn = sqlite3.connect("local.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Create ELEMENTS table and initialize it
c.execute('''CREATE TABLE IF NOT EXISTS ELEMENTS ([id] INTEGER NOT NULL, [name] TEXT, PRIMARY KEY (id))''')
chemical_elements = pd.read_csv("Files/ChemicalElement.csv", dtype={'id': int, 'name': str})
chemical_elements.to_sql('ELEMENTS', conn, if_exists='append', index=False)

# Create COMMODITY table and initialize it
c.execute('''CREATE TABLE IF NOT EXISTS COMMODITY ([id] INTEGER PRIMARY KEY NOT NULL,
             [name] TEXT, [inventory] NUMERIC, [price] NUMERIC)''')
chemical_elements = pd.read_csv("Files/Commodity.csv", dtype={'id': int, 'name': str, 'inventory': float, 'price': float})
chemical_elements.to_sql('COMMODITY', conn, if_exists='append', index=False)

# Create COMPOSITION table and initialize it
c.execute('''CREATE TABLE IF NOT EXISTS COMPOSITION ([element_id] INTEGER NOT NULL,
             [commodity_id] INTEGER NOT NULL, [percentage] NUMERIC, PRIMARY KEY (element_id, commodity_id))''')
chemical_elements = pd.read_csv("Files/Composition.csv", dtype={'element_id': int, 'commodity_id': int, 'percentage': float})
chemical_elements.to_sql('COMPOSITION', conn, if_exists='append', index=False)

conn.commit()
conn.close()
