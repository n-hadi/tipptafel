function betmodal() {
      const modal = document.querySelector("#betmodal");
      const overlay = document.querySelector(".overlay");
      const openModalBtn = document.querySelectorAll(".tip-btn");
      const closeModalBtn = document.querySelector("#betmodal-close");

      const openmodal_mobilerows = document.querySelectorAll(".tipptafel tr");

      openModalBtn.forEach(function(btn){
         if(btn.getAttribute('listener') != 'true'){ //damit nur ein listener pro tip-btn
          btn.setAttribute('listener','true');
          btn.addEventListener("click", function (e) {
             if(inert == 'True'){
              popup.close()
              fill_modal(modal, e.target.dataset);
               modal.classList.remove("hide");
               overlay.classList.remove("hide");
               document.body.style.overflow = 'hidden';
             }
             else{
              window.location.href = login_url
             }
           }
           )
         }
      });

      openmodal_mobilerows.forEach(function(tr){
         if(tr.getAttribute('listener') != 'true'){
          tr.setAttribute('listener','true');
          tr.addEventListener("click", function (e) {
             if(inert == 'True'){
              popup.close()
              fill_modal(modal, tr.querySelector(".tip-btn").dataset);
               modal.classList.remove("hide");
               overlay.classList.remove("hide");
               document.body.style.overflow = 'hidden';
             }
             else{
              window.location.href = login_url
             }
           }
           )
         }
      });

      const closeModal = function () {
        modal.classList.add("hide");
        overlay.classList.add("hide");
        document.body.style.overflow = 'auto';
      };
      closeModalBtn.addEventListener("click", closeModal);
    }
  
function fill_modal(modal, dataset){
  var t1 = dataset.t1
  var t1_img_src = dataset.t1_img
  var t2 = dataset.t2
  var t2_img_src = dataset.t2_img
  var user_tipp = dataset.tipp.split(", ") // t1, t2 => ['t1', 't2']
  var user = dataset.user
  var stake = dataset.stake
  var draw_impossible = dataset.draw_impossible;

  var options = draw_impossible == 'True' ? ['t1', 't2'] : ['t1', 't2', 'x'];
  var countertip = options.filter(n => !user_tipp.includes(n))

  document.getElementById('betnow-btn').innerHTML= ""
  var betnow_einsatz = document.createElement('span');
  betnow_einsatz.textContent =  stake + ' ';
  var txt_fill = document.createElement('span')
  txt_fill.textContent = " Wette abgeben"
  betnow_einsatz.appendChild(coin_img_yt)
  betnow_einsatz.appendChild(txt_fill)
  document.getElementById('betnow-btn').appendChild(betnow_einsatz)
  document.getElementById('betnow-btn').name = dataset.gameid

  document.getElementById('modal_title_t1').innerHTML = t1;
  document.getElementById('modal_title_t2').innerHTML = t2;
  
  document.getElementById('modal_img_t1').src = t1_img_src;
  document.getElementById('modal_img_t2').src = t2_img_src;

  document.getElementById('modal_user').innerHTML = user;

  document.getElementById('modal_user_tipp_img').innerHTML = '';
  userbetimg(user_tipp,'modal_user_tipp_img');

  document.getElementById('modal_user_tipp').innerHTML = userbet(user_tipp,t1,t2)

  
  document.getElementById('modal_tipp_img').innerHTML = '';
  userbetimg(countertip, 'modal_tipp_img');

  document.getElementById('modal_tipp').innerHTML = userbet(countertip, t1, t2)
}

function userbet(tipparray, t1, t2) { // returned text auf die wettersteller wettet
     var tipstr = []
     tipparray.forEach(bet=>{
      if (bet == 't1') {
         tipstr.push(t1)
       }
       if (bet == 't2') {
         tipstr.push(t2)
       }
       if (bet == 'x') {
         tipstr.push('Unentschieden')
       }
     })
     if(tipstr.length>1){
     return tipstr[0] + '<small><br>oder<br></small>' + tipstr[1]
     }
     else{
      return tipstr[0] 
     }
  }
  
function userbetimg(tipparray, destination) {
    tipparray.forEach(bet =>{
      var elem = document.createElement("img");
      elem.classList += 'ml1'
      if (bet == 't1') {
        elem.src = img_tipp1
        document.getElementById(destination).appendChild(elem);
      }
      if (bet == 't2') {
        elem.src = img_tipp2
        document.getElementById(destination).appendChild(elem);
      }
      if (bet == 'x') {
        elem.src = img_tippx
        document.getElementById(destination).appendChild(elem);
      }
    })
  }

function filtermodal(){
  const modal = document.querySelector("#filtermodal");
  const overlay = document.querySelector(".overlay");
  const openModalBtn = document.querySelectorAll(".filter-btn");
  const closeModalBtn = document.querySelector("#filtermodal-close");
  const filterform = document.querySelector('#filter-form')


  openModalBtn.forEach(function (btn) {
    if (btn.getAttribute('listener') != 'true') { //damit nur ein listener pro tip-btn
      btn.setAttribute('listener', 'true');
      btn.addEventListener("click", function (e) {
        popup.close()
        modal.classList.remove("hide");
        overlay.classList.remove("hide");
        document.body.style.overflow = 'hidden';
      }
      )
    }
  });

  const closeModal = function () {
    modal.classList.add("hide");
    overlay.classList.add("hide");
    document.body.style.overflow = 'auto';
  };
  closeModalBtn.addEventListener("click", closeModal);
  filterform.addEventListener("submit", closeModal);
}

function detailmodal(){
  const modal = document.querySelector("#detailmodal");
  const overlay = document.querySelector(".overlay");
  const openModalBtn = document.querySelectorAll(".t-detail");
  const closeModalBtn = document.querySelector("#detailmodal-close");


  openModalBtn.forEach(function (btn) {
    if (btn.getAttribute('listener') != 'true') { //damit nur ein listener pro t-detail btn
      btn.addEventListener("click", function (e) {
          e.stopPropagation() // damit nicht parent_row weiterleitet
          popup.close()
          fill_detail_modal(modal, e.target.dataset);
          modal.classList.remove("hide");
          overlay.classList.remove("hide");
          document.body.style.overflow = 'hidden';
        })
      btn.setAttribute('listener', 'true');
    }
     
    var parent_row = btn.closest("tr");
    if (parent_row.getAttribute("listener")!= "true"){
      parent_row.addEventListener("click",function(evt){
        var new_url = current_url()+ "/$" + btn.dataset["gameid"] + "/";
        htmx.ajax('GET', new_url, "#page-content")
         window.history.pushState(null, "", new_url);

      })
    parent_row.setAttribute('listener', 'true');
    }
      
    });

  const closeModal = function () {
    modal.classList.add("hide");
    overlay.classList.add("hide");
    document.body.style.overflow = 'auto';
  };
  closeModalBtn.addEventListener("click", closeModal);
}

function fill_detail_modal(modal, dataset){
  var t1 = dataset.t1
  var t1_img_src = dataset.t1_img
  var t2 = dataset.t2
  var t2_img_src = dataset.t2_img
  var user_tipp = dataset.tipp.split(", ") // t1, t2 => ['t1', 't2']
  var user = dataset.user;
  var stake = dataset.stake;
  var outcome = dataset.match_outcome;
  var draw_impossible = dataset.draw_impossible;
  
  var options =  draw_impossible == 'True' ? ['t1', 't2'] : ['t1', 't2', 'x'];
  var countertip = options.filter(n => !user_tipp.includes(n));

  document.getElementById('dmodal_user').innerHTML = (user=="")?"-":user;

  document.getElementById('dmodal_user_tipp_img').innerHTML = ''; //vorheriges bild weg machen
  userbetimg(countertip, 'dmodal_user_tipp_img');

  document.getElementById('dmodal_user_tipp').innerHTML = userbet(countertip, t1, t2)


  document.getElementById('dmodal_tipp_img').innerHTML = '';
  userbetimg(user_tipp, 'dmodal_tipp_img');

  document.getElementById('dmodal_tipp').innerHTML = userbet(user_tipp, t1, t2)
  
  document.getElementById('dmodal_einsatz').innerHTML =""
  var einsatzspan = document.createElement('span');
  einsatzspan.textContent =  stake + ' ';
  einsatzspan.appendChild(coin_img)
  document.getElementById('dmodal_einsatz').appendChild(einsatzspan);
  document.getElementById('dmodal_status').innerHTML = get_status(outcome, user, user_tipp);

  document.querySelector('.copy-link-input').value = current_url() + '/$' + dataset.gameid
}

function get_status(outcome, user, user_tipp){
  var status = null

  if (user == ''){
    if (outcome == 'an'){
      status = "User wird gesucht..."
    }
    if (['t1','t2','x'].includes(outcome)) {
      status = "Keinen User gefunden"
    }
  }
  else{
    if(outcome=="an"){
      status = "Anstehend"
    }
    else{
      (user_tipp.includes(outcome)) ? status = "Gewonnen" : status = "Verloren"
    }
  }
  (outcome == 'u') ? status = "Ungültig" : status;
  return status
}

function fill_table_status(){
  var status_tds = document.querySelectorAll('.bet_status');
  status_tds.forEach(td =>{
    var gameid = td.dataset.gameid
    var data_element = document.querySelector('a.t-detail[data-gameid="'+ gameid+'"]')
    var outcome = data_element.dataset.match_outcome
    var user = data_element.dataset.user
    var user_tipp = data_element.dataset.tipp.split(", ")
    var status = get_status(outcome, user, user_tipp);
    (status =="Keinen User gefunden")?status="Keinen User<br>gefunden":status;
    (status == "User wird gesucht...")?status = "User wird<br>gesucht...":status;
    td.innerHTML = status;
  })
}


htmx.onLoad(function (elt) {
      inject_spinner()
      // look up all elements with the tomselect class on it within the element
      var allSelects = htmx.findAll(elt, ".tomselect")
      for (select of allSelects) {
        new TomSelect(select, {
          persist: false,
          createOnBlur: true,
          create: true
        });
      }
      if(document.getElementsByClassName('tip-btn')){
        betmodal();
        filtermodal();
      }
      if(document.getElementsByClassName('t-detail')){
        detailmodal();
        fill_table_status();
        copy_link();
      }
      if(document.getElementById('fblwidget_table')){
        get_bl_table()
      }
      
    })

function inject_spinner() {
  try { // index unlogged gibts kein h4 oben. braucht nicht alles absaufen deshalb
    if(!document.getElementById("content_spinner")){
    var content_spinner = document.createElement("img");
    content_spinner.setAttribute("src", spinner_url);
    content_spinner.setAttribute("width", "25px");
    content_spinner.setAttribute("class", "my-indicator right");
    content_spinner.setAttribute("id", "content_spinner");

    var pageContentDiv = document.getElementById("page-content");
    var firstDiv = pageContentDiv.querySelector("div:first-of-type");
    var targetH4 = firstDiv.querySelector("h4");
    targetH4.appendChild(content_spinner);
  }
  } catch (error) {
    true
  }

}

document.body.addEventListener('htmx:afterRequest', (evt) =>{
  popup.close() //falls link geklickt mach popup weg
  inject_spinner()
      if(evt.target.id == 'betnow-btn'){
        show_popup(evt)
      }
})

function copy_link(){
  var copy_btn = document.querySelector('.copy-link-button')
  if (copy_btn.getAttribute('listener') != 'true'){
   copy_btn.addEventListener('click',(e)=>{
    var sharelink = document.querySelector('.copy-link-input')
    var text = sharelink.value
    sharelink.select()
    navigator.clipboard.writeText(text)
    sharelink.blur();
    sharelink.value = "Kopiert!";
    setTimeout(() => (sharelink.value = text), 2000);
  })
  copy_btn.setAttribute('listener','true');
  }
}

function show_popup(evt){
  var res = JSON.parse(evt.detail.xhr.response) //{"message": string, "balance": string }
  var status_code = evt.detail.xhr.status
  var balance = document.getElementById("sidebar-guthaben")
  const dialog = document.querySelector("#bet_placed_popup")
  const popup_txt = document.querySelector("#bet_placed_popup_txt")
  const modal = document.querySelector("#betmodal");
  const overlay = document.querySelector(".overlay");
  modal.classList.add("hide");
  overlay.classList.add("hide");
  document.body.style.overflow = 'auto';
  popup_txt.innerHTML = res["message"]
  if (status_code == 200) {
    var gameId = evt.target.name
    var button = document.querySelector('button[data-gameid="' + gameId + '"]');
    var row = button.parentNode.parentNode;
    balance.innerHTML = res["balance"]
    dialog.show()
    party.confetti(dialog, {
      count: party.variation.range(20, 40),
    });
    row.remove()
    setTimeout(() => (dialog.close(),popup_txt.innerHTML=""), 4000)
    
  }
  else {
    dialog.show()
    if (status_code == 403) {
      var aufladen = document.getElementById('bet_placed_popup_aufladen')
      var aufladen_parent = aufladen.parentNode;
      aufladen.classList.remove('hide')
      aufladen_parent.classList.remove('hide')
      setTimeout(() => (
        dialog.close(),
        aufladen.classList.add('hide'),
        aufladen_parent.classList.add('hide'),
        popup_txt.innerHTML=""
        ), 6000)
    }
    else {
      setTimeout(() => (dialog.close(),popup_txt.innerHTML=""), 4000)
    }
  }
}

function current_url(){
var currentURL = window.location.href
var urlParts = currentURL.split("/");
var domain = urlParts[2];
var urlWithProtocol = urlParts.slice(0, 3).join("/");
return urlWithProtocol //https://www.domain.com

}

window.addEventListener("popstate", function() {
  location.reload();
});

/* my bets */
function toggle_oldbets(hidebutton) {
  var allbetsvisible = true ? hidebutton.classList.contains("allbetsvisible") : false;
  var currentTime = new Date();
  var detailbtns = document.querySelectorAll('a.t-detail');
  for(let i =0; i < detailbtns.length; i++){
    var detail_btn = detailbtns[i]
    var dataDate = new Date(detail_btn.getAttribute('data-date'));
    var closestTR = detail_btn.closest('tr')
    var closestTR_display = window.getComputedStyle(closestTR).getPropertyValue("display")
      if (dataDate > currentTime) {
        closestTR.style.display = 'table-row';      
      } 
      else if(closestTR_display == "none" && !allbetsvisible){
        closestTR.style.display = 'table-row';      
      }
      else {
        closestTR.style.display = 'none';
      }
  }
  hidebutton.innerHTML = '';
  var spanElement = document.createElement("span");
  spanElement.classList.add("mr2")
  if (allbetsvisible){
    spanElement.innerHTML = "Alte Wetten einblenden"
    hidebutton.classList.remove("allbetsvisible", "visible_eye")
    hidebutton.classList.add("invisible_eye")
    hidebutton.style.content = "url('../icons/visible.png')"
  }
  else{
    spanElement.innerHTML = "Alte Wetten ausblenden"
    hidebutton.classList.remove("invisible_eye")
    hidebutton.classList.add("allbetsvisible","visible_eye")
    hidebutton.style.content = "url('../icons/invisible.png')"
  }
  hidebutton.appendChild(spanElement);
}
/* end mybets */