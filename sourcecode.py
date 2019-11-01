import sqlite3

def main():
    conn = sqlite3.connect(r"c:\Users\pingkam\Documents\University\Fourth_Year_University\CMPUT 291\sqlite\movie.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    conn.close()

main()


