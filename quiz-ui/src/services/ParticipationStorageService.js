export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem("participationScore");
  },
  saveTotalNumberOfQuestions(totalNumberOfQuestions) {
    window.localStorage.setItem("totalNumberOfQuestions", totalNumberOfQuestions);
  },
  getTotalNumberOfQuestions() {
    return window.localStorage.getItem("totalNumberOfQuestions");
  },
  saveTokenToStorage(token) {
    return window.localStorage.setItem('token', token);
  },
  getToken() {
    return window.localStorage.getItem('token');
  },
  removeTokenFromStorage() {
    return window.localStorage.removeItem('token');
  }
};