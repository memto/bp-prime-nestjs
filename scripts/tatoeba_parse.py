import sys
import os
import csv
import time
import sqlite3

AUDIO_URL_PREFIX = r'https://audio.tatoeba.org/sentences'
FROM_LANG = 'eng'
TO_LANG = 'vie'

if len(sys.argv) != 2:
    print ("Usage: python3 theScript <DATA_DIR>")
    sys.exit(0)

data_path = os.path.abspath(sys.argv[1])

print("data_path:", data_path)

tmp_db = os.path.join(data_path, "tmp.db")
db_con = sqlite3.connect(tmp_db)
db_cur = db_con.cursor()

links_csv = os.path.join(data_path, "links.csv")
sentences_csv = os.path.join(data_path, "sentences.csv")
sentences_with_audio_csv = os.path.join(data_path, "sentences_with_audio.csv")
output_csv = os.path.join(data_path, "output.csv")

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

def index_sentences_audio(csv_file):
    db_cur.execute('''DROP TABLE IF EXISTS sentences_audio''')
    db_cur.execute('''CREATE TABLE sentences_audio (id int)''')

    with open(csv_file, 'r') as file:
        csvreader = csv.reader(file, delimiter='\t')
        for row in csvreader:
            query = f"INSERT INTO sentences_audio VALUES ({row[0]})"
            db_cur.execute(query)

    db_con.commit()

def process_data_and_gen_csv(out_csv_file):  
  query = """
  SELECT from_s.id, from_s.sentence, to_s.id, to_s.sentence FROM links l 
    INNER JOIN sentences from_s ON l.from_id = from_s.id 
    INNER JOIN sentences to_s ON l.to_id = to_s.id 
  WHERE
    l.from_id in (
      SELECT sa.id FROM sentences_audio sa 
      JOIN sentences s ON sa.id = s.id where s.lang = '{0}'
    )
    and to_s.lang = '{1}'
  """.format(FROM_LANG, TO_LANG)
  
  with open(out_csv_file, 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter='\t',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)

      for row_link in db_cur.execute(query):
        print(row_link)
        # break #== TO_TEST
        (id, text, translate_id, translate_text) = row_link
        audio_url = AUDIO_URL_PREFIX + "/{0}/{1}.mp3".format(FROM_LANG, id)
        csv_writer.writerow([id, text, audio_url, translate_id, translate_text])
        

def now_str():
  from datetime import datetime
  return datetime.now().strftime("%H:%M:%S")

if __name__ == '__main__':
  # print("indexing...", now_str())
  # index_sentences(sentences_csv)
  # index_links(links_csv)
  # index_sentences_audio(sentences_with_audio_csv)
  # print("indexing done", now_str())

  # ==
  print("process data...", now_str())
  process_data_and_gen_csv(output_csv)
  print("process data done", now_str())

  # ==
  db_con.close()

  time.sleep(5)