//event listener wären besser aber kann keine benutzen da dynamisch geladen
function checkit(btn){ //btn = mockup checkbox input
   uncheckterms();
   var boxes = document.getElementsByName(btn.dataset.gameid) //hidden real checkbox inputs
   for (let i = 0; i < boxes.length; i++) {
      if (boxes[i].value == btn.dataset.team) {
         if (boxes[i].checked == true){ 
            //wenn box checked uncheck it und remove styling von mockup input
            boxes[i].checked = false;
            document.querySelector('.tbtn-checked[data-gameid="'+ btn.dataset.gameid +'"][data-team="' + btn.dataset.team + '"]').classList.remove('tbtn-checked')
         }
         else{
            // wenn box nicht gecheckt schau ob schon 2 boxen gecheckt sind
            var check = 0
            for(let j=0;j < boxes.length;j++){if(boxes[j].checked == true){check++}}
             //draw possible
            if ((check == 0 || check == 1) && boxes.length == 4){ // t1 t2 x stake = 4
               //Ansonsten check es und füg styling im mockup input hinzu
               boxes[i].click()
               btn.className += " tbtn-checked";
            }
            
              //draw impossible
            if (check == 0 && boxes.length == 3){
               //Ansonsten check es und füg styling im mockup input hinzu
               boxes[i].click()
               btn.className += " tbtn-checked";

            }
         
            }
      }
   }
}

function twodecimals(el) {
      el.value = parseFloat(parseFloat(el.value).toFixed(2));
      if (el.value < 0) {
         el.value = 0;
      }
      el.innerHTML = el.value
      el.style.border = '';
      update_sum()
   }

function uncheckterms(){
   document.getElementById('accept_terms').checked = false;
   update_sum()
}

function update_sum(){
   einsatz_inputs = document.getElementsByClassName('einsatz_input')
   var sum = 0
   for (let i = 0; i < einsatz_inputs.length; i++) {
      if (!isNaN(parseFloat(einsatz_inputs[i].value))){
         sum = parseFloat(parseFloat(sum).toFixed(2)) + parseFloat(parseFloat(einsatz_inputs[i].value).toFixed(2))
      }
   }
   summe_input = document.getElementById('einsatz_summe')
   summe_input.value = sum
   summe_input.innerHTML = sum

   if(summe_input.value > guthaben){
      summe_input.style.border = '1px solid var(--zero)';
      summe_input.style.color = 'var(--zero)';

   }
   else{
      summe_input.style.border = '';
      summe_input.style.color = '';
   }
}

function fill_einsatz_inputs(){
   var einsatz_inputs = document.querySelectorAll('.einsatz_input')
   einsatz_inputs.forEach(el =>{
   document.querySelector('.stake_input[name="'+ el.dataset.gameid +'"]').value = el.value
   })
}
var ratelimiter = false
function beforesubmit(event){
   var team_checkboxes = document.querySelectorAll('.tinput')
   if(somethingchecked(team_checkboxes)){
         if(guthabenok(team_checkboxes) && einsatz_ok(team_checkboxes) && checked_agb() && !ratelimiter){ 
            ratelimiter = true;
            fill_einsatz_inputs()
            document.getElementById('bets_form').submit()
         }
         else{
            event.preventDefault()
         }
   }
   else{
      alert('Du hast keinen Tipp abgegeben.')
      event.preventDefault()
   }
}

function somethingchecked(team_checkboxes) {
   var somethingchecked = false;
   team_checkboxes.forEach(el => {
      if (el.checked) { somethingchecked = true }
   })
   return somethingchecked
}

// check if sum > Guthaben
function guthabenok(team_checkboxes){
   var einsatz_summe = document.getElementById('einsatz_summe')
   if (guthaben < einsatz_summe.value) {
      alert('Dein Guthaben in Höhe von ' + guthaben + ' Tipptaler reicht nicht aus um den Einsatz zu decken.')
      return false
   }else{return true}
}
// check if for every t checked sum given 
// einsatz summe >=5
function einsatz_ok(team_checkboxes){
   var einsatz_ok = true;
   team_checkboxes.forEach(e => {
      if (e.checked) {
         var einsatz_input = document.querySelector(".einsatz_input[data-gameid='" + e.name + "']")
         if (einsatz_input.value < 5) {
            einsatz_input.style.border = '1px solid var(--zero)';
            einsatz_ok = false;
         }
      }
   })
   if (einsatz_ok == false){
      alert('Der Einsatz pro Tippspiel muss mindestens 5 Tipptaler betragen.')
   }
   return einsatz_ok
}

function checked_agb(){
   if (!document.getElementById('accept_terms').checked){
      alert('Bitte akzeptiere die AGB um fortzufahren.')
   }
   return document.getElementById('accept_terms').checked
}

document.body.addEventListener('htmx:confirm', function(e){
   var einsatz_inputs = document.querySelectorAll('input[type=number]')
   var team_checkboxes= document.querySelectorAll('input[type=checkbox]')
   var prevent = false

   einsatz_inputs.forEach(el => {
      if(el.value > 0){
         prevent = true
      }
   })
   team_checkboxes.forEach(el =>{
      if(el.checked){
         prevent = true
      }
   })
   if(prevent && e.target.id != 'bets_form' && window.location.pathname=="/meine_wetten/wette_erstellen/"){
      if(!confirm('Bist du sicher, dass du fortfahren möchtest?\nDeine aktuellen Eingaben werden gelöscht.')){
         e.preventDefault()
      }
   }
})
