import re
import json
import os

class TinyRDBMS:
    def __init__(self, db_name="my_database.json"):
        self.db_name = db_name
        self.tables = {}
        self.load()

    def load(self):
        if os.path.exists(self.db_name):
            with open(self.db_name, 'r') as f:
                self.tables = json.load(f)

    def save(self):
        with open(self.db_name, 'w') as f:
            json.dump(self.tables, f, indent=4)

    def execute(self, query):
        query = query.strip()
        
        # 1. CREATE TABLE
        create_match = re.match(r"CREATE TABLE (\w+) \((.*)\)", query, re.IGNORECASE)
        if create_match:
            table_name, cols_raw = create_match.groups()
            cols = [c.strip().split() for c in cols_raw.split(",")]
            self.tables[table_name] = {
                "schema": {c[0]: c[1] for c in cols},
                "rows": [],
                "pk": cols[0][0]  # First column is PK by default for simplicity
            }
            self.save()
            return f"Table {table_name} created."

        # 2. INSERT INTO
        insert_match = re.match(r"INSERT INTO (\w+) VALUES \((.*)\)", query, re.IGNORECASE)
        if insert_match:
            table_name, vals_raw = insert_match.groups()
            if table_name not in self.tables: return "Error: Table not found."
            
            vals = [v.strip().strip("'") for v in vals_raw.split(",")]
            schema_keys = list(self.tables[table_name]["schema"].keys())
            new_row = dict(zip(schema_keys, vals))
            
            # Primary Key Check
            pk = self.tables[table_name]["pk"]
            if any(r[pk] == new_row[pk] for r in self.tables[table_name]["rows"]):
                return "Error: Primary Key violation."
            
            self.tables[table_name]["rows"].append(new_row)
            self.save()
            return "Row inserted."

        # 3. SELECT with JOIN
        select_join_match = re.match(r"SELECT (.*) FROM (\w+) JOIN (\w+) ON (.*)", query, re.IGNORECASE)
        if select_join_match:
            cols_req, t1, t2, on_clause = select_join_match.groups()
            left_col, right_col = [x.strip().split(".")[1] for x in on_clause.split("=")]
            
            results = []
            for r1 in self.tables[t1]["rows"]:
                for r2 in self.tables[t2]["rows"]:
                    if r1[left_col] == r2[right_col]:
                        results.append({**r1, **r2})
            return results

        # 4. BASIC SELECT
        select_match = re.match(r"SELECT (.*) FROM (\w+)", query, re.IGNORECASE)
        if select_match:
            cols, table_name = select_match.groups()
            if table_name not in self.tables: return "Error: Table not found."
            return self.tables[table_name]["rows"]

        # 5. DELETE
        delete_match = re.match(r"DELETE FROM (\w+) WHERE (\w+)\s*=\s*'(.*)'", query, re.IGNORECASE)
        if delete_match:
            table_name, col, val = delete_match.groups()
            original_count = len(self.tables[table_name]["rows"])
            self.tables[table_name]["rows"] = [r for r in self.tables[table_name]["rows"] if r[col] != val]
            self.save()
            return f"Deleted {original_count - len(self.tables[table_name]['rows'])} rows."

        return "Error: Invalid SQL Syntax."

# --- REPL MODE ---
if __name__ == "__main__":
    db = TinyRDBMS()
    print("TinyRDBMS Shell. Type 'exit' to quit.")
    while True:
        sql = input("db > ")
        if sql.lower() == 'exit': break
        print(db.execute(sql))
