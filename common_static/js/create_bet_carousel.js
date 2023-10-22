var carousel = document.querySelector(".carousel-container");
var track = document.querySelector(".track");
var tournament_btns = document.querySelectorAll(".card")
var width = carousel.offsetWidth;
var index = 0;
window.addEventListener("resize", function () {
  width = carousel.offsetWidth;
});

function next(){
 if (index < max_index()) {
  index = index + 1;
  track.style.transform = "translateX(" + index * -width + "px)";
  }
}
function prev(){
 if(index >0){
   index = index - 1;
  track.style.transform = "translateX(" + index * -width + "px)";
  }
}

function max_index(){
 let sum_width = 0
 tournament_btns.forEach(btn =>{
  sum_width += btn.offsetWidth
 })
var divisionResult =  sum_width / carousel.offsetWidth ;
var nextSmallestInt = Math.floor(divisionResult); // because index starts at 0
return nextSmallestInt
}
