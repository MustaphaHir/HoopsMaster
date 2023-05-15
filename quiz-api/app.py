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
    if 'password' not in payload:
        return jsonify({'error': 'Password is required.'}), 400
    else:
        tried_password = payload['password'].encode('UTF-8')
        hashed = hashlib.md5(tried_password).hexdigest()
        if(hashed == password_hash):
            token = build_token()
            return {'token': token}, 200  # Retourner le token dans la réponse en JSON
        else:
            return {'error': 'Unauthorized'}, 401  # Retourner une erreur 401 Unauthorized si le mot de passe est incorrect
	

	

@app.route('/questions', methods=['POST'])
def add_question():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 4

    #récupèrer un l'objet json envoyé dans le body de la requète
    data=request.get_json()

    # créer un nouvel objet Question à partir des données JSON
    question = Question.from_json(data)


    question.add_question_todb()

    return jsonify({'id': question.id}), 200
"""
@app.route('/questions/<int:id>', methods=['PUT'])
def set_question(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 4

    #récupèrer un l'objet json envoyé dans le body de la requète
    data=request.get_json()

    # créer un nouvel objet Question à partir des données JSON
    question = Question.from_json(data)


    question.set_question_todb(id)

    return jsonify({'id': question.id}), 200
"""

@app.route('/questions/<int:id>', methods=['DELETE'])
def del_question(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    if (Question.check_if_question_exists(id) ):  
        deleted = Question.delete_question_todb(id)
        if deleted:
            return jsonify({'message': f'Question with id {id} deleted successfully'}), 204
    else:
         return jsonify({'message': 'Question not found'}), 404
    
@app.route('/questions/all', methods=['DELETE'])
def del_all_question():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    deleted = Question.delete_all_questions_todb()
    if deleted!=None:
        return jsonify({'message': 'Questions are all deleted successfully'}), 204
    else:
        return jsonify({'message': 'Questions was not deleted successfully'}), 404


@app.route('/participations/all', methods=['DELETE'])
def del_all_participations():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    deleted = Question.delete_all_participants_todb()
    if deleted!=None:
        return jsonify({'message': 'Participations are all deleted successfully'}), 204
    else:
        return jsonify({'message': 'Participations was not deleted successfully'}), 404
    


@app.route('/questions/<id>', methods=['PUT'])
def update_question(id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401
    
    if (Question.check_if_question_exists(id)):  
        #récupèrer un l'objet json envoyé dans le body de la requète
        data=request.get_json()
        question = Question.from_json(data)

        # Récupérer la position de la question de la requête
        position = data.get('position')

        # Mettre à jour la question avec la position de la requête
        question.update_question_todb(id)

        return jsonify({'id': question.id}), 204
    else:
        return jsonify({'message': 'Question not found'}), 404
    

@app.route('/export', methods=['GET'])
def getall_question():
        question = Question.extract_all_questions()
        return question, 200
    
    



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



    




if __name__ == "__main__":
    app.run()