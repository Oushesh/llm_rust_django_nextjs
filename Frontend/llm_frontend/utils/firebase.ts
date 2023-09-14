// Import the functions you need from the SDKs you need
import { initializeApp, getApp, getApps } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'
import { getAuth } from 'firebase/auth'

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
// Your web app's Firebase configuration

//TODO: move those keys keys env variables. in vercel its not required.
const firebaseConfig = {
    apiKey: "AIzaSyD7uRhxqFEx0tA0smTLY_YezfWzV5IYncQ",
    authDomain: "netflix-clone-ce54b.firebaseapp.com",
    projectId: "netflix-clone-ce54b",
    storageBucket: "netflix-clone-ce54b.appspot.com",
    messagingSenderId: "160622151554",
    appId: "1:160622151554:web:ff26fc56e1d4a63c90719b"
};

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp()
const db = getFirestore()
const auth = getAuth()

export default app
export { auth, db }

