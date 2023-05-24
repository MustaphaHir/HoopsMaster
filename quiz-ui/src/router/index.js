import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionsManager from '../views/QuestionsManager.vue'
import QuestionDisplay from '../views/QuestionDisplay.vue';
import Score from '../views/Score.vue';
import AdminLogin from '../views/AdminLogin.vue';
import AdminQuestionsList from '../views/AdminQuestionsList.vue';
import AdminQuestionDetail from '../views/AdminQuestionDetail.vue';
import AdminQuestionEdit from '../views/AdminQuestionEdit.vue';
import AdminQuestionAdd from '../views/AdminQuestionAdd.vue';


//import Score from '../views/score.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: "/new-quiz",
      name: "NewQuizPage",
      component: NewQuizPage,
    },
    {
      path: "/questions",
      name: "QuestionsManager",
      component: QuestionsManager,
    },
    {
      path: "/score",
      name: "Score",
      component: Score,
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: AdminLogin,
    },
    {
      path: '/admin/questions',
      name: 'AdminQuestionsList',
      component: AdminQuestionsList,
    },
    {
      path: '/admin/question-detail/:id',
      name: 'AdminQuestionDetail',
      component: AdminQuestionDetail,
    },
    {
      path: '/admin/question-edit/:id',
      name: 'AdminQuestionEdit',
      component: AdminQuestionEdit,
    },
    {
      path: '/admin/question-add',
      name: 'AdminQuestionAdd',
      component: AdminQuestionAdd,
    },

  ]
})

export default router
