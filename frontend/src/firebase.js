// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyABaseommVaJzdYEdMZfsCVIwsJjK9BbI8",
  authDomain: "login-register-firebase-2bb1a.firebaseapp.com",
  projectId: "login-register-firebase-2bb1a",
  storageBucket: "login-register-firebase-2bb1a.firebasestorage.app",
  messagingSenderId: "218806651820",
  appId: "1:218806651820:web:df650ecc1787bb642b4809",
  measurementId: "G-D2MKH699GH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export auth to use it in other components
export const auth = getAuth(app);
export default app;
