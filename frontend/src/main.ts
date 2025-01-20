import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'; // Import Pinia

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App)
const pinia = createPinia(); // Create a Pinia instance

app.use(router)
app.use(pinia); // Register Pinia with the app

app.mount('#app')
