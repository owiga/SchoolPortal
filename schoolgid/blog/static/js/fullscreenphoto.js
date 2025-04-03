const overlay = document.getElementById("overlay");

function enlargeImage(img) {
    if (img.classList.contains("icdfu")) {
        overlay.style.pointerEvents = "none";
        overlay.innerHTML = "";
        document.body.style.overflow = "auto";
        overlay.style.backgroundColor = "transparent";
        overlay.classList.remove("ofci");
    } else {
        let child = overlay.appendChild(img.cloneNode(true));
        child.classList.add("icdfu")
        overlay.style.pointerEvents = "all";
        child.style.transform = "scale(1.35)";
        document.body.style.overflow = "hidden";
        overlay.style.backgroundColor = "rgba(0, 0, 0, 0.85)";
        overlay.classList.add("ofci");
    }
    
}

document.addEventListener("click", function(event) {
    if (event.target.classList.contains("ofci")) {
        event.target.classList.remove("ofci");
        overlay.style.pointerEvents = "none";
        overlay.innerHTML = "";
        document.body.style.overflow = "auto";
        overlay.style.backgroundColor = "transparent";
    }
});