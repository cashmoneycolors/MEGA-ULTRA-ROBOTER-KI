openssl req -x509 -newkey rsa:4096 -keyout private.key -out zertifikat.pem -days 365 -nodesstreamlit run app.pyimport streamlit as st
import io
import contextlib
import sqlite3

st.set_page_config(page_title="🔐 Lokaler Eingabe-Server", layout="centered")
st.title("🔐 Lokaler Eingabe-Server")

# SQLite-Datenbank für Logs
conn = sqlite3.connect("local_database.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        result TEXT
    )
''')
conn.commit()

code = st.text_area("💻 Gib hier deinen Python-Code ein:", height=200)

if st.button("▶️ Ausführen"):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
        result = output.getvalue()
        st.success("✅ Code erfolgreich ausgeführt.")
        st.text_area("📤 Ausgabe:", result, height=200)
        cursor.execute("INSERT INTO logs (code, result) VALUES (?, ?)", (code, result))
        conn.commit()
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
        cursor.execute("INSERT INTO logs (code, result) VALUES (?, ?)", (code, str(e)))
        conn.commit()

st.subheader("📜 Ausgeführte Befehle")
cursor.execute("SELECT code, result FROM logs ORDER BY id DESC LIMIT 5")
for row in cursor.fetchall():
    st.text_area("Code", row[0], height=100)
    st.text_area("Ergebnis", row[1], height=100)

conn.close()