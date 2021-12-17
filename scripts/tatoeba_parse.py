import sys
import os
import csv
import time
import sqlite3

if len(sys.argv) != 2:
    print ("Usage: python3 theScript <DATA_DIR>")
    sys.exit(0)

data_path = os.path.abspath(sys.argv[1])

print("data_path:", data_path)

tmp_db = os.path.join(data_path, "tmp.db")
db_con = sqlite3.connect(tmp_db)
db_cur = db_con.cursor()

links_path = os.path.join(data_path, "links.csv")
sentences_path = os.path.join(data_path, "sentences.csv")
sentences_with_audio_path = os.path.join(data_path, "sentences_with_audio.csv")

def parse_csv(csv_file):
    rows = []
    with open(csv_file, 'r') as file:
        csvreader = csv.reader(file, delimiter='\t')
        for row in csvreader:
            rows.append(row)
    
    return rows

def index_sentences(csv_file):
    db_cur.execute('''DROP TABLE IF EXISTS sentences''')
    db_cur.execute('''CREATE TABLE sentences
               (id int, lang text, sentence text)''')

    with open(csv_file, 'r') as file:
        csvreader = csv.reader(file, delimiter='\t')
        for row in csvreader:
            sentence = row[2].replace("'", "''")
            query = f"INSERT INTO sentences VALUES ({row[0]}, '{row[1]}', '{sentence}')"
            db_cur.execute(query)

    db_con.commit()


def index_links(csv_file):
    db_cur.execute('''DROP TABLE IF EXISTS links''')
    db_cur.execute('''CREATE TABLE links (from_id int, to_id int)''')

    with open(csv_file, 'r') as file:
        csvreader = csv.reader(file, delimiter='\t')
        for row in csvreader:
            query = f"INSERT INTO links VALUES ({row[0]}, '{row[1]}')"
            db_cur.execute(query)

    db_con.commit()

def now_str():
  from datetime import datetime
  return datetime.now().strftime("%H:%M:%S")

if __name__ == '__main__':
  print("indexing...", now_str())
  index_sentences(sentences_path)
  index_links(sentences_path)
  print("indexing done", now_str())

  time.sleep(30)