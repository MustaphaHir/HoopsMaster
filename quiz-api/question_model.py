import sqlite3
import json

class Question:
    def __init__(self, position=None, title=None, text=None, image=None):
        self.position = position
        self.title = title
        self.text = text
        self.image=image
        self.id = None


    def to_json(self):
        return json.dumps({'position': self.position, 'title': self.title, 'text': self.text, 'image': self.image})
    
    def from_json(json_str):
        data = json.loads(json_str)
        return Question(position=data['position'], title=data['title'], text=data['text'], image=data['image'])

    def add_question(self):
        db_connection = sqlite3.connect('quiz.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        
        c = db_connection.cursor()

        c.execute('''INSERT INTO question (position, title, text, image) VALUES (?, ?, ?, ?)''', (self.position, self.title, self.text, self.image))
        
        self.id = c.lastrowid
        db_connection.commit()
        db_connection.close()

    def get_question_by_id(id):
        db_connection = sqlite3.connect('quiz.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        c = db_connection.cursor()
#       c.execute(f'INSERT INTO question (position, title, text, image) VALUES ({self.position}, "{self.title}", "{self.text}", "{self.image}")')
        c.execute('''SELECT * FROM question WHERE id=?''', (id,))
        
        row = c.fetchone()
        
        db_connection.close()

        if row is None:
            return None
        else:
            return Question(row)
        

    def get_question_by_position(position):
        db_connection = sqlite3.connect('quiz.db')

        # set the sqlite connection in "manual transaction mode"
        # (by default, all execute calls are performed in their own transactions, not what we want)
        db_connection.isolation_level = None

        c = db_connection.cursor()
#       c.execute(f'INSERT INTO question (position, title, text, image) VALUES ({self.position}, "{self.title}", "{self.text}", "{self.image}")')
        c.execute('''SELECT * FROM question WHERE position=?''', (position,))
        
        row = c.fetchone()
        
        db_connection.close()

        if row is None:
            return None
        else:
            return Question(row)

