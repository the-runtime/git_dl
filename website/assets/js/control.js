button = document.getElementById('button');
button.addEventListener("click", clicked);
function clicked(){
    link = document.getElementById('link').value;
    console.log(link);
    window.location.replace("url/?link="+link);
};
