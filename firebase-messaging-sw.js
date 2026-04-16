importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

// البيانات دي هي اللي هتربط "الحارس" بمشروعك الحالي
firebase.initializeApp({
  apiKey: "AIzaSyCs_vLcVUudSP3_4QaSQHQB44WGjQK31Ac", 
  authDomain: "alphashadow-23689.firebaseapp.com", // اتأكدت لك إن ده الـ ID الصح
  projectId: "alphashadow-23689",
  messagingSenderId: "367347348332", // رقم المرسل
  appId: "1:367347348332:web:61908298713a073f4e198b"
});

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
  const title = payload.notification.title || "Alpha Shadow 👑";
  const options = {
    body: payload.notification.body || "طلب جديد في الانتظار! 🔥",
    icon: "https://i.ibb.co/3yk8S7K/logo.png",
    vibrate: [200, 100, 200], // هزة تنبيه للكاشير
    badge: "https://i.ibb.co/3yk8S7K/logo.png"
  };
  return self.registration.showNotification(title, options);
});
