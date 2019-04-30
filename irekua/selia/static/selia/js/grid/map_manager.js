var formerSelection = null;

function selectOnMap(){
  if (mapMarkers[currentSelection]){
      if (formerSelection != null && formerSelection != currentSelection){
        mapMarkers[formerSelection].setIcon(mapGreenIcon);
      }
      mapMarkers[currentSelection].setIcon(mapRedIcon);
      formerSelection = currentSelection;
  }

}

function init_map(){
    registerUpdater("selection", selectOnMap);
}

$(document).ready(function() {
  init_map();
});