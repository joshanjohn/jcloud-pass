'use strict';

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDQ-EUuJUGE7NhLN3YOPBb2vj5OYwHYf_I",
    authDomain: "jcloud-paas.firebaseapp.com",
    projectId: "jcloud-paas",
    storageBucket: "jcloud-paas.firebasestorage.app",
    messagingSenderId: "758103231649",
    appId: "1:758103231649:web:6ab6d4dbbaa972bb4774e0",
    measurementId: "G-9DSBL5ZJRT",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

window.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#auth-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const emailInput = document.querySelector("#email");
        const passwordInput = document.querySelector("#password");

        if (!emailInput || !passwordInput) {
            console.error("Login form inputs were not found.");
            return;
        }

        try {
            const userCredential = await signInWithEmailAndPassword(
                auth,
                emailInput.value,
                passwordInput.value,
            );
            console.log("Firebase login successful:", userCredential.user.email);
        } catch (error) {
            console.error("Firebase login failed:", error);
        }
    });
});
