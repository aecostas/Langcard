#import MySQLdb
import sqlite3

class LangcardDB:
    def __init__(self):
        self.conn = sqlite3.connect('db/langcard.db')

        
    def __del__(self):
        self.conn.close ()


    def langcardGetRandomWord(self):
        cursor = self.conn.cursor()

        cursor.execute ("select phrases.id, words.comments, words.original, words.translation, phrases.phrase, phrases_words.position from phrases inner join phrases_words on phrases.id=phrases_words.id_phrase inner join words on phrases_words.id_word=words.id order by random() limit 1;")
        row = cursor.fetchone()
        return row



    def langcardGetPhraseList(self):
        phrases = {}
        cursor = self.conn.cursor()

        cursor.execute ("select phrases.id, words.comments, words.original, words.translation, phrases.phrase, phrases_words.position from phrases inner join phrases_words on phrases.id=phrases_words.id_phrase inner join words on phrases_words.id_word=words.id order by phrases.id;")

        row = cursor.fetchone()
        while row is not None:

            if row:
                print row
                phrases[len(phrases)] = row;
            row = cursor.fetchone()

        cursor.close ()

        return phrases


    def langcardSetPhrase(self, data):
        cursor = self.conn.cursor()
            
        cursor.execute ("insert into phrases (phrase ) values (\""+data["phrase"]+"\");")
        self.conn.commit()
        phrase_id = cursor.lastrowid;

        for word in data["words"]:
            cursor.execute ("insert into words (original, translation, comments) values (\"%s\",\"%s\",\"%s\")" % (data["words"][word]["foreign"], data["words"][word]["nativeword"], data["words"][word]["comments"]))
            self.conn.commit()

            cursor.execute("insert into phrases_words (id_phrase, id_word, position) values (%d, %d, %d)" % (phrase_id, cursor.lastrowid, data["words"][word]["position"]));
            self.conn.commit()
        cursor.close ()

