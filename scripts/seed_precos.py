#!/usr/bin/env python3
# Insere preço fixo por instrumento
import os, sqlite3
DB_PATH = os.getenv("DB_PATH", "./db/maestro.db")
con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("SELECT COUNT(1) FROM instrumentos")
if cur.fetchone()[0] == 0:
    print("Instrumentos vazios. Rode os seeds SQL primeiro.")
else:
    cur.execute("DELETE FROM precos_servico")
    cur.execute("INSERT INTO precos_servico (servico, instrumento_id, valor, vigente_desde) SELECT 'aula', id, ?, DATE('now') FROM instrumentos", (250.0,))
    con.commit()
    print("Preços aplicados.")
con.close()
