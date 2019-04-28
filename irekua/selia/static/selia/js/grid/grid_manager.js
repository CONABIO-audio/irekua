var currentSelection = null;
var hoverSelection = null;
var selectionUrl = null;

var updaters = {};

function registerUpdater(actionName, updater) {
  if (!(actionName in updaters)) {
    updaters[actionName] = [];
  }

  updaters[actionName].push(updater);
}

function refreshViews(actionName) {
  updaters[actionName].forEach(function(elt) {elt();});
}

function setCurrentSelection(uId, url) {
  currentSelection = uId;
  selectionUrl = url;
  refreshViews('selection');
}
