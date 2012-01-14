import MySQLdb

class LangcardDB:
    def __init__(self):
        self.conn = MySQLdb.connect (host = "localhost",
                                     user = "root",
                                     passwd = "root",
                                     db = "langcards")

        
    def __del__(self):
        self.conn.close ()


    def langcardGetPhraseList():
        pass


    def langcardSetPhrase(self, data):
        cursor = self.conn.cursor()
            
        cursor.execute ("insert into phrases set phrase=\""+data["phrase"]+"\";")
        phrase_id = self.conn.insert_id()

        for word in data["words"]:
            cursor.execute ("insert into words (original, translation, comments) values (\"%s\",\"%s\",\"%s\")" % (data["words"][word]["foreign"], data["words"][word]["nativeword"], data["words"][word]["comments"]))

            cursor.execute("insert into phrases_words (id_phrase, id_word, position) values (%d, %d, %d)" % (phrase_id, self.conn.insert_id(), data["words"][word]["position"]));

        cursor.close ()

