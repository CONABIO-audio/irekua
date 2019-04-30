var formerSelection = null;

function selectOnMap(){
  if (formerSelection != null && formerSelection != currentSelection){
    mapMarkers[formerSelection].setIcon(mapGreenIcon);
  }
  mapMarkers[currentSelection].setIcon(mapRedIcon);
  formerSelection = currentSelection;
}

$(document).ready(function() {
  registerUpdater("selection", selectOnMap);
});