import { createStore } from 'vuex';
import axios
 from 'axios';
export default createStore({
  state: {
    isAuthenticated: false,
    user: null,
  },
  mutations: {
    setAuthState(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    authenticate(state, user) {
      state.isAuthenticated = true;
      state.user = user;
    },
  },
  actions: {
    authenticate({ commit }, user) {  
      commit('authenticate', user);
    },
    async checkAuthState({ commit, state }) {
      try {
        const response = await axios.get('http://localhost:8000/auth/verify', {withCredentials : true});
        const isAuthenticated = response.data.authenticated;
        commit('setAuthState', isAuthenticated);
      } catch (error) {
        console.error("Authentication check failed:", error);
        commit('setAuthState', false);
      }
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    },
});
