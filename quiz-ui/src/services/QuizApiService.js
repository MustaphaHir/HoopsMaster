import axios from "axios";
import ParticipationStorageService from '../services/ParticipationStorageService';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null) {
    var headers = {
      "Content-Type": "application/json",
    };

    const token = ParticipationStorageService.getToken();
    if (token) {
      headers.authorization = `Bearer ${token}`;
    }

    try {
      const response = await instance({
        method,
        headers: headers,
        url: resource,
        data,
      });

      return { status: response.status, data: response.data };
    } catch (error) {
      console.error(error);
    }
  },

  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  authenticate(password) {
    return this.call("post", "login", { password });
  },
  getQuestion(position) {
    return this.call("get", `questions?position=${position}`);
  },
  getAllQuestions() {
    return this.call("get", "export");
  },
  deleteQuestionbyPosition(questionPosition) {
    return this.call("delete", `questions?position=${questionPosition}`);
  },
  addQuestion(questionData) {
    return this.call("post", "questions", questionData);
  },
  updateQuestion(position, questionData) {
    return this.call("put", `questionsposition/${position}`, questionData);
  },
  addParticipant(participantData) {
    return this.call("post", "participations", participantData);
  },
  getPercentageScore(userScore) {
    return this.call("get", `scorepercentage?score=${userScore}`);
  },
  checkUsername(username) {
    return this.call("get", `playername?username=${username}`);
  },
  getRandomQuestions() {
    return this.call("get", "tenquestions");
  }
};
