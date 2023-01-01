document.addEventListener("rotate", ev => {
    if (ev.direction) {
        document.querySelector("body").style.backgroundColor = "#FFFFFF";
    }
});