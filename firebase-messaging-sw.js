importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

// دي البيانات الملكية الخاصة بمشروعك يا بطل
firebase.initializeApp({
  apiKey: "AIzaSyCs_vLcVUudSP3_4QaSQHQB44WGjQK31Ac", 
  authDomain: "alpha-shadow-7.firebaseapp.com",
  projectId: "alpha-shadow-7",
  messagingSenderId: "367347348332",
  appId: "1:367347348332:web:61908298713a073f4e198b"
});

const messaging = firebase.messaging();

// وظيفة الإشعار لما يوصل والشاشة مقفولة
messaging.setBackgroundMessageHandler(function(payload) {
  const title = payload.notification.title || "تنبيه من Alpha Shadow";
  const options = {
    body: payload.notification.body || "طلبك جاهز يا فنان! 🔥",
    icon: "https://i.ibb.co/3yk8S7K/logo.png"
  };
  return self.registration.showNotification(title, options);
});
