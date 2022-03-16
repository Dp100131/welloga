
const realButton = document.getElementById('real-file');
const falseButton = document.getElementById('custom-button');
const falseText = document.getElementById('custom-text');

falseButton.addEventListener("click", function(){

    realButton.click();

});

realButton.addEventListener("change", function(){

    if(realButton.value){

        falseText.innerHTML = realButton.value;

    }else{

        falseText.innerHTML = "No file chosen, yet.";

    }

});