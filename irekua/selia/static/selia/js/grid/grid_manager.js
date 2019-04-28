var currentSelection = null;
var hoverSelection = null;
var selectionUrl = null;
var selectionMeta = null;
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

function getSelectionMetadata(successCallback=null) {
  $.ajax({url:selectionUrl,
  		  type:"GET",
  		  success: function(result){
  		  	selectionMeta=result;
  		  	if (successCallback != null){
  		  		successCallback();
  		  	}
  		  },
  		  error:function(error){
  			alert("Error")
  		  }
  		})
}

function setCurrentSelection(uId, url) {
  currentSelection = uId;
  selectionUrl = url;
  getSelectionMetadata(successCallback=function(){refreshViews('selection');});
}
