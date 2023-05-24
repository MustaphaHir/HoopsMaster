from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from jwt_utils import build_token, decode_token, JwtError
from question_model import Question, Participations

app = Flask(__name__)
CORS(app)

password_hash = 'd8170650479293c12e0201e5fdf45f40'  # Mot de passe 'password' en MD5

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    quiz_size = Question.getquizinfo()
    quiz_score = Participations.getscoresinfo()
    return {"size": quiz_size, "scores": quiz_score}, 200

@app.route('/rebuild-db', methods=['POST'])
def Rebuild_db():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401
    
    try:
        Question.rebuild_db()  # Appeler la fonction rebuild_db() pour créer les tables
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def Authenticate():
    payload = request.get_json()
    if 'password' not in payload:
        return jsonify({'error': 'Password is required.'}), 400
    else:
        tried_password = payload['password'].encode('UTF-8')
        hashed = hashlib.md5(tried_password).hexdigest()
        if hashed == password_hash:
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
        return jsonify({'error': str(e)}), 401

    data = request.get_json()

    # Créer un nouvel objet Question à partir des données JSON
    question = Question.from_json(data)

    question.add_question_todb()

    return jsonify({'id': question.id}), 200

@app.route('/participations', methods=['POST'])
def add_participant():
    data = request.get_json()

    # Créer un objet Participations avec les données fournies
    participant = Participations.from_json(data)

    if Question.getquizinfo() > len(data['answers']):
        return jsonify({'error': "Il manque des réponses à des questions"}), 400
    elif Question.getquizinfo() < len(data['answers']):
        return jsonify({'error': "Il y a trop de questions par rapport aux réponses"}), 400
    else:
        participant.add_participant_to_db()
        return participant.to_json(), 200


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

    if Question.check_if_question_exists(id):
        Question.delete_question_todb(id)
        return jsonify({'message': f'Question with id {id} deleted successfully'}), 204
    else:
        return jsonify({'message': 'Question not found'}), 404


@app.route('/questions', methods=['DELETE'])
def del_questionbyPosition():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    position = request.args.get('position')

    return del_question(Question.find_id_from_position(position))


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
    if deleted is not None:
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
    if deleted is not None:
        return jsonify({'message': 'Participations are all deleted successfully'}), 204
    else:
        return jsonify({'message': 'Participations was not deleted successfully'}), 404


@app.route('/questions/<id>', methods=['PUT'])
def update_question(id):
    if Question.check_if_question_exists(id):
        data = request.get_json()
        question = Question.from_json(data)

        question.update_question_todb(id)

        return jsonify({'id': question.id}), 204
    else:
        return jsonify({'message': 'Question not found'}), 404


@app.route('/questionsposition/<position>', methods=['PUT'])
def update_question_by_position(position):
    return update_question(Question.find_id_from_position(position))



@app.route('/export', methods=['GET'])
def getall_question():
    questions = Question.extract_all_questions()
    return jsonify(questions), 200


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


@app.route('/scorepercentage', methods=['GET'])
def calculate_score_percentage():
    score_user = int(request.args.get('score'))

    other_scores = Participations.getallscores()

    sorted_scores = sorted(other_scores, reverse=True)

    user_position = sorted_scores.index(score_user) + 1

    score_percentage = (user_position / len(sorted_scores)) * 100

    return jsonify(score_percentage), 200


@app.route('/playername', methods=['GET'])
def getPlayerName():
    playerName = request.args.get('username')

    allPlayerNames = Participations.getallplayername()

    if playerName in allPlayerNames:
        return jsonify({"data": True}), 200
    else:
        return jsonify({"data": False}), 200


if __name__ == "__main__":
    app.run()