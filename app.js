fetch("http://172.20.10.7:5000/api/send", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        text: spokenText,
        room: "101",
        lang: currentLang
    })
})
.then(res => console.log("Envoyé à la réception"))
.catch(err => console.error("Erreur envoi :", err));
