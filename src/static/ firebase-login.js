'use strict'

// Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
  import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from 'https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js';
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyDQ-EUuJUGE7NhLN3YOPBb2vj5OYwHYf_I",
    authDomain: "jcloud-paas.firebaseapp.com",
    projectId: "jcloud-paas",
    storageBucket: "jcloud-paas.firebasestorage.app",
    messagingSenderId: "758103231649",
    appId: "1:758103231649:web:6ab6d4dbbaa972bb4774e0",
    measurementId: "G-9DSBL5ZJRT"
  };

  // Initialize Firebase


window.addEventListener("load", function(){ 
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(); 

  

})