// Import the functions you need from the SDKs you need
import * as firebase from "firebase";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCAdQkha8M-OoG88j2NtZLiJT1sBWVQeWQ",
  authDomain: "firefly-6e22b.firebaseapp.com",
  projectId: "firefly-6e22b",
  storageBucket: "firefly-6e22b.appspot.com",
  messagingSenderId: "140242435447",
  appId: "1:140242435447:web:8d5ec5128f627171b6f572"
};

// Initialize Firebase
let app;
if(firebase.apps.length === 0) {
    app = firebase.initializeApp(firebaseConfig);
} else {
    app = firebase.app()
}
 const auth = firebase.auth()

 export {auth}