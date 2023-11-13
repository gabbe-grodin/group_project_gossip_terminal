// !    TYPE ANIMATED LOGO
let textLength = 0;
let text = 'Terminal';

function type() {
    let textChar = text.charAt(textLength++);
    let paragraph = document.getElementById("typed");
    let charElement = document.createTextNode(textChar);
    paragraph.appendChild(charElement);
    if(textLength < text.length+1) {
        setTimeout('type()', 50);
    } else {
        text = '';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    type();
});

// !    TYPE ANIMATED SUBTITLE
let textLengthTwo = 0;
let textTwo = 'where devs get to gossip...';

function typeAgain() {
    let textCharTwo = textTwo.charAt(textLengthTwo++);
    let paragraphTwo = document.getElementById("typedAgain");
    let charElementTwo = document.createTextNode(textCharTwo);
    paragraphTwo.appendChild(charElementTwo);
    if(textLengthTwo < textTwo.length+1) {
        setTimeout('typeAgain()', 70);
    } else {
        textTwo = '';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    typeAgain();
});
