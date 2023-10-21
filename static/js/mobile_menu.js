const slideout_btns = document.getElementsByClassName('slideout-btn')
const slideouts =     document.querySelectorAll('.slideout')
const links = document.querySelectorAll('.slideout-list>li>a')


function outofscreen(slideout){
slideout.style.transform = 'translateX(-100%)'
}

for(let i = 0; i < slideout_btns.length; i++){
 slideout_btns[i].addEventListener('click', e => {
   
    var slideout_what = e.target.parentElement.dataset.activate

    var slide_element = document.getElementById(slideout_what)
    if (slide_element.style.transform == 'translateX(0px)'){ //wenn ausgerollt roll ein
     slide_element.style.transform = 'translateX(-100%)'
    }
    else{
     //wenn eingerollt roll alle ein und roll es aus
     slideouts.forEach(outofscreen)
     slide_element.style.transform = 'translateX(0px)'
   }

  }
 )
}

for (let i=0;i<links.length;i++){
  links[i].addEventListener('click', e =>{
    slideouts.forEach(outofscreen)
  })
}
