'use strict';

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import {
    getAuth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";

// --- Firebase Initialization ---
let auth;

/**
 *  fetch Firebase config and initializes the SDK.
 */
async function initFirebase() {
    try {
        const configResponse = await fetch('/auth/config');
        if (!configResponse.ok) throw new Error("Failed to fetch Firebase config");
        const firebaseConfig = await configResponse.json();

        const app = initializeApp(firebaseConfig);
        auth = getAuth(app);

        console.log("Firebase initialized");
        setupListeners();
    } catch (error) {
        console.error("Firebase init failed:", error);
    }
}

/**
 * Attaches event listeners for login, signup, and logout.
 */
function setupListeners() {
    // login  user
    const loginBtn = document.getElementById("login");
    if (loginBtn) {
        loginBtn.addEventListener('click', function () {
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            console.log("Attempting login...");
            signInWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    console.log("Logged in successfully");
                    userCredential.user.getIdToken().then((token) => {
                        document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                        window.location = "/workspace";
                    });
                })
                .catch((error) => {
                    console.error("Login Error:", error.code, error.message);
                    alert("Login failed: " + error.message);
                });
        });
    }

    // sign up new user 
    const signupBtn = document.getElementById("sign-up");
    if (signupBtn) {
        signupBtn.addEventListener('click', function () {
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            console.log("Attempting signup...");
            createUserWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    console.log("Account created");
                    userCredential.user.getIdToken().then((token) => {
                        document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                        window.location = "/workspace";
                    });
                })
                .catch((error) => {
                    console.error("Signup Error:", error.code, error.message);
                    alert("Signup failed: " + error.message);
                });
        });
    }

    // sign out user
    const signoutBtn = document.getElementById("sign-out");
    if (signoutBtn) {
        signoutBtn.addEventListener('click', function () {
            signOut(auth)
                .then(() => {
                    console.log("Signed out");
                    // Expire the token cookie
                    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1900 00:00:00 UTC; SameSite=Strict";
                    window.location = "/";
                })
                .catch((error) => {
                    console.error("Sign-out Error:", error);
                });
        });
    }

    
}

// Start Initialization
window.addEventListener("load", initFirebase);