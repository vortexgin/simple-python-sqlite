from helper.SqliteHelper import create_connection

app_name = "Simple Python Sqlite"
app_debug = True
app_host = "0.0.0.0"
app_port = 8080
secret_key = "6LcgGLcUAAAAAD0vDkLecCswf_h-fV1NL3F82ybm"
db_path = ':memory:'
conn = create_connection(db_path=db_path)
