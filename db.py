import MySQLdb

class LangcardDB:
    def __init__(self):
        self.conn = MySQLdb.connect (host = "localhost",
                                     user = "root",
                                     passwd = "root",
                                     db = "langcards")

        
    def __del__(self):
        self.conn.close ()


    def langcardGetPhraseList(self):
        phrases = {}
        cursor = self.conn.cursor()

        cursor.execute ("select phrases.id, words.comments, words.original, words.translation, phrases.phrase, phrases_words.position from phrases inner join phrases_words on phrases.id=phrases_words.id_phrase inner join words on phrases_words.id_word=words.id order by phrases.id;")

        row = cursor.fetchone()
        while row is not None:
            print "Row..."

            if row:
                print "row != null"
                phrases[len(phrases)] = row;
            row = cursor.fetchone()


        cursor.close ()
        return phrases


    def langcardSetPhrase(self, data):
        cursor = self.conn.cursor()
            
        cursor.execute ("insert into phrases set phrase=\""+data["phrase"]+"\";")
        phrase_id = self.conn.insert_id()

        for word in data["words"]:
            cursor.execute ("insert into words (original, translation, comments) values (\"%s\",\"%s\",\"%s\")" % (data["words"][word]["foreign"], data["words"][word]["nativeword"], data["words"][word]["comments"]))

            cursor.execute("insert into phrases_words (id_phrase, id_word, position) values (%d, %d, %d)" % (phrase_id, self.conn.insert_id(), data["words"][word]["position"]));

        cursor.close ()

