const hashedCode = "06a2bb3737abd3f64bd52d657374b6b56eb14212"; // Код доступа

async function hashInput(input) {
    return CryptoJS.SHA1(input).toString();
}

async function checkCode() {
    let userCode = document.getElementById("accessCode").value;
    let hashedUserCode = await hashInput(userCode);
    let errorMessage = document.getElementById("errorMessage");

    if (hashedUserCode === hashedCode) {
        localStorage.setItem("access_granted", "true");
        document.getElementById("overlay").classList.add("hidden");
    } else {
        errorMessage.style.display = "block";
    }
}

window.onload = function () {
    if (localStorage.getItem("access_granted") === "true") {
        document.getElementById("overlay").classList.add("hidden");
    }
};