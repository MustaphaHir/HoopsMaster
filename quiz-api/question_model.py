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
    
    """
    def check_if_question_exists_in_position(self):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()

        # Check if a question already exists at the desired position
        c.execute('''SELECT * FROM question WHERE position = ?''', (self.position,))
        existing_question = c.fetchone()

        if existing_question:
            # If a question already exists at the desired position, increment the position of all questions after that position by 1
            c.execute('''SELECT id FROM question WHERE position >= ? ORDER BY position DESC''', (self.position,))
            for row in c.fetchall():
                c.execute('''UPDATE question SET position = position + 1 WHERE id = ?''', (row[0],))
    """

    def add_question_todb(self):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()

        # Check if a question already exists at the desired position
        c.execute('''SELECT * FROM question WHERE position = ?''', (self.position,))
        existing_question = c.fetchone()

        if existing_question:
            # If a question already exists at the desired position, increment the position of all questions after that position by 1
            c.execute('''SELECT id FROM question WHERE position >= ? ORDER BY position DESC''', (self.position,))
            for row in c.fetchall():
                c.execute('''UPDATE question SET position = position + 1 WHERE id = ?''', (row[0],))

        # Insert the new question at the desired position
        c.execute('''INSERT INTO question (position, title, text, image) VALUES (?, ?, ?, ?)''', (self.position, self.title, self.text, self.image))

        self.id = c.lastrowid

        for possible_answer_data in self.possible_answers:
            possible_answer = PossibleAnswer.from_json(possible_answer_data)
            possible_answer.question_id = self.id
            c.execute('''INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)''', (possible_answer.text, possible_answer.is_correct, self.id))

        db_connection.commit()
        db_connection.close()

    """
    def set_question_todb(self,id):
        db_connection = sqlite3.connect('quizbasket.db')
        db_connection.isolation_level = None
        c = db_connection.cursor()

        c.execute('''SELECT * FROM question WHERE id = ?''', (id,))
        existing_question = c.fetchone()

        if existing_question:
            # If a question already exists at the desired position, increment the position of all questions after that position by 1
            c.execute('''SELECT id FROM question WHERE position >= ? ORDER BY position DESC''', (self.position,))
            for row in c.fetchall():
                c.execute('''UPDATE question SET position = position + 1 WHERE id = ?''', (row[0],))

        # Insert the new question at the desired position
        c.execute('''UPDATE question SET position = ? WHERE id = ?''', (self.position, id))

        db_connection.commit()
        db_connection.close()
    """

    def delete_question_todb(id):
        db_connection = sqlite3.connect('quizbasket.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        c = db_connection.cursor()

        if(id=="all"):
            c.execute(f'''DELETE FROM question''')
            c.execute(f'''DELETE FROM possible_answers''')
        else:
            c.execute(f'''DELETE FROM question WHERE id  = {id}''')
            c.execute(f'''DELETE FROM possible_answers WHERE question_id  = {id}''')

        # get the number of rows affected by the query
        num_rows_deleted = c.rowcount

        db_connection.commit()

        db_connection.close()
    
        # return the number of rows deleted
        return num_rows_deleted

    def delete_all_questions_todb():
            db_connection = sqlite3.connect('quizbasket.db')

            # set the sqlite connection in "manual transaction mode"
            # (by default, all execute calls are performed in their own transactions, not what we want)
            db_connection.isolation_level = None

            c = db_connection.cursor()
            c.execute(f'''DELETE FROM question''')
            c.execute(f'''DELETE FROM possible_answers''')
            # get the number of rows affected by the query
            num_rows_deleted = c.rowcount

            db_connection.commit()

            db_connection.close()
        
            # return the number of rows deleted
            return num_rows_deleted
    
    def delete_all_participants_todb():
            db_connection = sqlite3.connect('quizbasket.db')

            # set the sqlite connection in "manual transaction mode"
            # (by default, all execute calls are performed in their own transactions, not what we want)
            db_connection.isolation_level = None

            c = db_connection.cursor()
            c.execute('''DELETE FROM participations''')
            # get the number of rows affected by the query
            num_rows_deleted = c.rowcount

            db_connection.commit()

            db_connection.close()
        
            # return the number of rows deleted
            return num_rows_deleted

    def find_id_from_position(position):
        db_connection = sqlite3.connect('quizbasket.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        c = db_connection.cursor()
#       c.execute(f'INSERT INTO question (position, title, text, image) VALUES ({self.position}, "{self.title}", "{self.text}", "{self.image}")')
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

        # Check if a question already exists at the desired position
        c.execute('''SELECT * FROM question WHERE position = ?''', (self.position,))
        existing_question = c.fetchone()

        if existing_question:
            # If a question already exists at the desired position, increment the position of all questions after that position by 1
            c.execute('''SELECT id FROM question WHERE position >= ? ORDER BY position DESC''', (self.position,))
            for row in c.fetchall():
                c.execute('''UPDATE question SET position = position + 1 WHERE id = ?''', (row[0],))

        # Update question
        c.execute('UPDATE question SET position=?, title=?, text=?, image=? WHERE id=?',
                (self.position, self.title, self.text, self.image, id))

        # Delete existing possible answers for the question
        c.execute('DELETE FROM possible_answers WHERE question_id=?', (id,))

        # Insert possible answers for the question
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