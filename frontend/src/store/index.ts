import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: false,
    user: null,
  },
  mutations: {
    authenticate(state, user) {
      state.isAuthenticated = true;
      state.user = user;
    },
  },
  actions: {
    authenticate({ commit }, user) {
      commit('authenticate', user);
    },
  },
});
