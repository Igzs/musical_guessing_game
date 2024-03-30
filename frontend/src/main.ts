import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Assuming your router setup is in './router/index.ts'
import store from './store'; // If you're using Vuex, assuming setup is in './store/index.ts'
import './style.css'

const app = createApp(App);

// Use Vue Router
app.use(router);

// Use Vuex Store if applicable
app.use(store);

app.mount('#app');
