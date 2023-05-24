import sqlite3
import json


class Question:
    def __init__(self, id=None, position=None, title=None, text=None, image=None, possible_answers=[]):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possible_answers = possible_answers

    def to_json(self):
        possible_answers = [possible_answer.to_json() for possible_answer in self.possible_answers] if self.possible_answers else []
        return {
            'id': self.id,
            'position': self.position,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'possibleAnswers': possible_answers
        }

    def from_json(json_data):
        id = json_data.get('id')
        position = json_data.get('position')
        title = json_data.get('title')
        text = json_data.get('text')
        image = json_data.get('image')
        possible_answers = json_data.get('possibleAnswers')
        return Question(id, position, title, text, image, possible_answers)

    def add_question_todb(self):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()

        c.execute('''SELECT * FROM question WHERE position = ?''', (self.position,))
        existing_question = c.fetchone()

        if existing_question:
            c.execute('''SELECT id FROM question WHERE position >= ? ORDER BY position DESC''', (self.position,))
            for row in c.fetchall():
                c.execute('''UPDATE question SET position = position + 1 WHERE id = ?''', (row[0],))

        c.execute(
            '''INSERT INTO question (position, title, text, image) VALUES (?, ?, ?, ?)''',
            (self.position, self.title, self.text, self.image)
        )

        self.id = c.lastrowid

        for possible_answer_data in self.possible_answers:
            possible_answer = PossibleAnswer.from_json(possible_answer_data)
            possible_answer.question_id = self.id
            c.execute(
                '''INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)''',
                (possible_answer.text, possible_answer.is_correct, self.id)
            )

        db_connection.commit()
        db_connection.close()

    def getquizinfo():
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        c.execute('''SELECT COUNT(*) FROM question''')
        num_questions = c.fetchone()[0]

        db_connection.close()

        return num_questions
    

    def rebuild_db():
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        c.execute("""CREATE TABLE "question" (
            "id"	INTEGER,
            "position"	INTEGER NOT NULL,
            "title"	TEXT NOT NULL,
            "text"	TEXT NOT NULL,
            "image"	TEXT,
            PRIMARY KEY("id")
        );
        """)

        c.execute("""CREATE TABLE "possible_answers" (
            "id"	INTEGER,
            "text"	TEXT NOT NULL,
            "is_correct"	INTEGER NOT NULL,
            "question_id"	INTEGER NOT NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY("question_id") REFERENCES "question"("id") ON DELETE CASCADE
        );
        """)

        c.execute("""
            CREATE TABLE "participations" (
                "id"	INTEGER,
                "playerName"	TEXT,
                "SCORE"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            );

        """)


        c.execute("""
            CREATE TABLE "participant_answers" (
            "id"	INTEGER,
            "participation_id"	INTEGER,
            "answer"	NUMERIC,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("participation_id") REFERENCES "participations"("id")
        );
        """)


        db_connection.commit()
        db_connection.close()

    
        
    

    def delete_question_todb(id):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None

        c = db_connection.cursor()

        c.execute('''SELECT position FROM question WHERE id = ?''', (id,))
        current_position = c.fetchone()[0]

        if(id=="all"):
            c.execute(f'''DELETE FROM question''')
            c.execute(f'''DELETE FROM possible_answers''')
        else:
            c.execute(f'''DELETE FROM question WHERE id  = {id}''')
            c.execute(f'''DELETE FROM possible_answers WHERE question_id  = {id}''')
            c.execute('''UPDATE question SET position = position - 1 WHERE position >= ?''', (current_position,))

     
        num_rows_deleted = c.rowcount

        db_connection.commit()

        db_connection.close()
    
      
        return num_rows_deleted

    def delete_all_questions_todb():
            db_connection = sqlite3.connect('quizbasket.db')
            db_connection.isolation_level = None

            c = db_connection.cursor()
            c.execute(f'''DELETE FROM question''')
            c.execute(f'''DELETE FROM possible_answers''')
      
            num_rows_deleted = c.rowcount

            db_connection.commit()

            db_connection.close()
        
           
            return num_rows_deleted
    
    def delete_all_participants_todb():
            db_connection = sqlite3.connect('quizbasket.db')

            db_connection.isolation_level = None

            c = db_connection.cursor()
            c.execute('''DELETE FROM participations''')
            c.execute('''DELETE FROM participant_answers''')
            
            num_rows_deleted = c.rowcount

            db_connection.commit()

            db_connection.close()
        
          
            return num_rows_deleted

    def find_id_from_position(position):
        db_connection = sqlite3.connect('quizbasket.db')

        db_connection.isolation_level = None

        c = db_connection.cursor()
        c.execute('''SELECT id FROM question WHERE position=?''', (position,))
        
        row = c.fetchone()
        if row is None:
            return None

        row_id = row[0]
        db_connection.close()

        return row_id
        

    def get_question_by_id(id):
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        c.execute('''SELECT * FROM question WHERE id=?''', (id,))
        row = c.fetchone()

        db_connection.close()

        if row is None:
            return None
        else:
            question = Question(*row)
            possible_answers = PossibleAnswer.get_possible_answers_by_question_id(id)
            question.possible_answers = possible_answers
            return question
        

    def check_if_question_exists(id):
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        c.execute('''SELECT * FROM question WHERE id=?''', (id,))
        row = c.fetchone()

        db_connection.close()

        return row is not None
    

    def extract_all_questions():
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        c.execute('''SELECT * FROM question''')
        row = c.fetchall()

        db_connection.close()

        return row 




    def update_question_todb(self, id):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()

        
        c.execute('''SELECT position FROM question WHERE id = ?''', (id,))
        current_position = c.fetchone()[0]

        if self.position != current_position:
            if self.position > current_position:
                c.execute('''UPDATE question SET position = position - 1 WHERE position > ? AND position <= ?''', (current_position, self.position))
                c.execute('''UPDATE question SET position = ? WHERE id = ?''', (self.position, id))
            elif self.position < current_position:
                c.execute('''UPDATE question SET position = position + 1 WHERE position >= ? AND position < ?''', (self.position, current_position))
                c.execute('''UPDATE question SET position = ? WHERE id = ?''', (self.position, id))


                
        c.execute('UPDATE question SET title=?, text=?, image=? WHERE id=?', ( self.title, self.text, self.image, self.id))
        

        
        c.execute('DELETE FROM possible_answers WHERE question_id=?', (id,))

        
        for possible_answer_data in self.possible_answers:
            possible_answer = PossibleAnswer.from_json(possible_answer_data)
            possible_answer.question_id = id
            c.execute('INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)',
                    (possible_answer.text, possible_answer.is_correct, possible_answer.question_id))

        db_connection.commit()
        db_connection.close()




class PossibleAnswer:
    def __init__(self, id, text, is_correct, question_id):
        self.id = id
        self.text = text
        self.is_correct = is_correct
        self.question_id = question_id
        

    def to_json(self):
        if(self.is_correct==0):
               booleenreponse= False
        else:
                booleenreponse= True

        return {
            'id': self.id,
            'text': self.text,
            'isCorrect': booleenreponse,
            'question_id': self.question_id
        }

    def from_json(json_data):
        id = json_data.get('id')
        question_id = json_data.get('question_id')
        text = json_data.get('text')
        is_correct = json_data.get('isCorrect')

        return PossibleAnswer(id, text,is_correct , question_id)
    
    def get_possible_answers_by_question_id(question_id):
            db_connection = sqlite3.connect('quizbasket.db')
            db_connection.isolation_level = None

            c = db_connection.cursor()
            c.execute('SELECT * FROM possible_answers WHERE question_id=?', (question_id,))

            rows = c.fetchall()

            db_connection.close()

            if not rows:
                return None

            possible_answers = []
            for row in rows:
                possible_answer = PossibleAnswer(*row)
                possible_answers.append(possible_answer)

            return possible_answers
    


class PossibleAnswer:
    def __init__(self, id, text, is_correct, question_id):
        self.id = id
        self.text = text
        self.is_correct = is_correct
        self.question_id = question_id
        

    def to_json(self):
        if(self.is_correct==0):
               booleenreponse= False
        else:
                booleenreponse= True

        return {
            'id': self.id,
            'text': self.text,
            'isCorrect': booleenreponse,
            'question_id': self.question_id
        }

    def from_json(json_data):
        id = json_data.get('id')
        question_id = json_data.get('question_id')
        text = json_data.get('text')
        is_correct = json_data.get('isCorrect')

        return PossibleAnswer(id, text,is_correct , question_id)
    
    def get_possible_answers_by_question_id(question_id):
            db_connection = sqlite3.connect('quizbasket.db')
            db_connection.isolation_level = None

            c = db_connection.cursor()
            c.execute('SELECT * FROM possible_answers WHERE question_id=?', (question_id,))

            rows = c.fetchall()

            db_connection.close()

            if not rows:
                return None

            possible_answers = []
            for row in rows:
                possible_answer = PossibleAnswer(*row)
                possible_answers.append(possible_answer)

            return possible_answers
    


class Participations:
    def __init__(self, id, playerName=None, answers=[], score=0):
        self.id = id
        self.playerName = playerName
        self.answers = answers
        self.score = score


    def to_json(self):
        answers = [answer for answer in self.answers] if self.answers else []
        return {
            'playerName': self.playerName,
            'answers': answers,
            'score': self.score
        }
    

    def from_json(json_data):
        id = json_data.get('id')
        playerName = json_data.get('playerName')
        answers = json_data.get('answers')
        score = json_data.get('score')
        return Participations(id, playerName, answers, score)
    

    def get_number_of_participants(self):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()
        c.execute('''SELECT COUNT(*) FROM participations''')
        num_participations = c.fetchone()[0]
        db_connection.close()
        return num_participations
    
    
    def get_score_of_participants(self):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()

        c.execute('''SELECT answer FROM participant_answers WHERE participation_id = ?''', (self.id,))
        participant_answers = c.fetchall()
        position = 0
        self.score = 0
        for answer in participant_answers:
            position += 1
            c.execute("""SELECT row_num
                FROM (
                SELECT ROW_NUMBER() OVER (ORDER BY id) AS row_num, is_correct
                FROM possible_answers
                WHERE question_id = ?
                ) AS numbered_rows
                WHERE is_correct = 1""", (Question.find_id_from_position(position),))
            
            true_answer = c.fetchone()[0]
            if true_answer==answer[0]:
                 self.score+=1

        db_connection.close()

        return self.score

    

    def add_participant_to_db(self):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()
        c.execute('''INSERT INTO participations (playerName) VALUES (?)''',
                  (self.playerName, ))
        self.id = c.lastrowid
        for answer_data in self.answers:
            c.execute('''INSERT INTO participant_answers (participation_id, answer) VALUES (?, ?)''',
                      (self.id, answer_data))


        c.execute('''UPDATE participations SET score = ? WHERE id = ?''', (self.get_score_of_participants(), self.id))

        
            
        db_connection.commit()
        db_connection.close()


    def getscoresinfo():
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        data = []
        c.execute('''SELECT playerName, score FROM participations ORDER BY score DESC LIMIT 7''')
        results = c.fetchall()

        for score_participants in results:
            player_name = score_participants[0]
            score = score_participants[1]
            data.append({'playerName': player_name, 'score': score})

            
        db_connection.close()

        return data
    
    def getallscores():
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        data = []
        c.execute('''SELECT score FROM participations''')
        results = c.fetchall()

        for score_participants in results:
            score = score_participants[0]
            data.append(score)

            
        db_connection.close()

        return data
    
    def getallplayername():
        db_connection = sqlite3.connect('quizbasket.db')
        c = db_connection.cursor()

        data = []
        c.execute('''SELECT playerNAME FROM participations''')
        results = c.fetchall()

        for playerName in results:
            playerName = playerName[0]
            data.append(playerName)

            
        db_connection.close()

        return data
    


class ParticipantAnswers:
    def __init__(self, id=None, participation_id=None, answer=None):
        self.id = id
        self.participation_id = participation_id
        self.answer = answer

    def to_json(self):
        return {
            'participation_id': self.participation_id,
            'answer': self.answer,
        }
    
    def from_json(json_data):
        participation_id = json_data.get('participation_id')
        answer = json_data.get('answer')
        return ParticipantAnswers(participation_id, answer)


