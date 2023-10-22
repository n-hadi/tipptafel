function get_bl_table(){
  const apiUrl = "https://www.bundesliga-widgets.de/Widgets/Table?league=bl1&season=23/24&compactview=true";
  const targetDiv = document.getElementById("fblwidget_table");

  if(targetDiv){
   fetch(apiUrl,{
    headers: {
      'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7', 
      //Damit der nur die kurzen Namen "Bayern" statt "FC Bayern München" ausspuckt
    }
   })
    .then(response => response.text())
    .then(data => {
      targetDiv.innerHTML = data;
    });
  }
}
get_bl_table()