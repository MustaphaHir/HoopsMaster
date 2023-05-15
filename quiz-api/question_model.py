import sqlite3
import json

class Question:
    def __init__(self, id=None, position=None, title=None, text=None, image=None, possible_answers=[]):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image=image
        self.possible_answers = possible_answers

    def to_json(self):
        possible_answers = [possible_answers.to_json() for possible_answers in self.possible_answers] if self.possible_answers else []
        return {
            'id': self.id,
            'position': self.position,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'possibleAnswers': possible_answers
        }
    
    @staticmethod
    def from_json(json_data):
        id = json_data.get('id')
        position = json_data.get('position')
        title = json_data.get('title')
        text = json_data.get('text')
        image = json_data.get('image')
        possible_answers = json_data.get('possibleAnswers')
    

        return Question(id, position, title, text, image, possible_answers)

    def add_question(self):
        db_connection = sqlite3.connect('quizbasket.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        c = db_connection.cursor()

        c.execute('''INSERT INTO question (position, title, text, image) VALUES (?, ?, ?, ?)''', (self.position, self.title, self.text, self.image))

        self.id = c.lastrowid

        for possible_answer_data in self.possible_answers:
            possible_answer = PossibleAnswer.from_json(possible_answer_data)
            possible_answer.question_id = self.id
            c.execute('''INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)''', (possible_answer.text, possible_answer.is_correct, self.id))


        db_connection.commit()

        db_connection.close()


        

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
        

    def find_id_from_position(position):
        db_connection = sqlite3.connect('quizbasket.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        c = db_connection.cursor()
#       c.execute(f'INSERT INTO question (position, title, text, image) VALUES ({self.position}, "{self.title}", "{self.text}", "{self.image}")')
        c.execute('''SELECT id FROM question WHERE position=?''', (position,))
        
        row = c.fetchone()[0]
        db_connection.close()

        return row

    def get_question_by_position(position):
        return Question.get_question_by_id(Question.find_id_from_position(position))



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

    @staticmethod
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