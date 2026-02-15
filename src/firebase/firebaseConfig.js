import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyCaL4UGhBl3jBqtMrpV8j12raVkA_I5JSU",
  authDomain: "emotionengine-5723e.firebaseapp.com",
  databaseURL: "https://emotionengine-5723e-default-rtdb.firebaseio.com",
  projectId: "emotionengine-5723e",
  storageBucket: "emotionengine-5723e.firebasestorage.app",
  messagingSenderId: "401837446466",
  appId: "1:401837446466:web:53f7cf3b121c13cdafe4db",
  measurementId: "G-W0V9T8FN44"
};

const app = initializeApp(firebaseConfig);

export default app;
