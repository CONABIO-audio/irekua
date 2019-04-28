var currentSelection = null;
var hoverSelection = null;
var updaters = {};

function registerUpdater(sourceWidget,updater){
	updaters[sourceWidget] = updater;
}

function setCurrentSelection(uId,sourceWidget) {
	alert(uId);
	alert(widgetSource);
	refreshViews(sourceWidget);
}

function refreshViews(sourceWidget){
	for (var key in updaters){
		if (key != sourceWidget){
			updaters[key]();
		}
	}
}

