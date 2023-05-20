import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionsManager from '../views/QuestionsManager.vue'
import QuestionDisplay from '../views/QuestionDisplay.vue';
import Score from '../views/Score.vue';

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
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
