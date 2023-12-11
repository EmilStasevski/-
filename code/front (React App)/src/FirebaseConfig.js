// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

const FirebaseConfig = {
  apiKey: "AIzaSyCuL4x5twvbykspItqh6R2oRqR37GJi0VI",
  authDomain: "parsingcec.firebaseapp.com",
  databaseURL:
    "https://parsingcec-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "parsingcec",
  storageBucket: "parsingcec.appspot.com",
  messagingSenderId: "504335341061",
  appId: "1:504335341061:web:31d516764e25bd6a7a6e6c",
  measurementId: "G-L20BSLZWX6",
};

const app = initializeApp(FirebaseConfig);
export const db = getDatabase(app);
