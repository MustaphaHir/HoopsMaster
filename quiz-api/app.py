from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from jwt_utils import build_token,decode_token,JwtError
from question_model import Question



app = Flask(__name__)
CORS(app)


password_hash = 'd8170650479293c12e0201e5fdf45f40'  # Mot de passe 'password' en MD5

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


@app.route('/login', methods=['POST'])
def Authenticate():
    
	payload = request.get_json()
	tried_password = payload['password'].encode('UTF-8')
	hashed = hashlib.md5(tried_password).hexdigest()
	if(hashed == password_hash):
		token = build_token()
		return {'token': token}, 200  # Retourner le token dans la réponse en JSON
	else:
		return {'error': 'Unauthorized'}, 401  # Retourner une erreur 401 Unauthorized si le mot de passe est incorrect
	

	

@app.route('/questions', methods=['POST'])
def post_question():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    #récupèrer un l'objet json envoyé dans le body de la requète
    data=request.get_json()

    # créer un nouvel objet Question à partir des données JSON
    question = Question.from_json(data)


    question.add_question()

    return jsonify({'id': question.id}), 200


@app.route('/questions/<int:id>', methods=['GET'])
def get_questions_by_id(id):
    question = Question.get_question_by_id(id)
    if question:
        return question.to_json(), 200
    else:
        return jsonify({'message': 'Question not found'}), 404
    


@app.route('/questions', methods=['GET'])
def get_questions_by_position():
    position = request.args.get('position')
    return get_questions_by_id(Question.find_id_from_position(position))

@app.route('/questions/<int:id>', methods=['PUT'])
def update_question_by_id(id):
    question = Question.get_question_by_id(id)
    if question:
        return question.to_json(), 200
    else:
        return jsonify({'message': 'Question not found'}), 404

if __name__ == "__main__":
    app.run()