var hoverSelection;
var currentSelection;
var selectionUrl;
var selectionMeta;
var selectionLabels;
var updateResponse;
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
            type:"OPTIONS",
            success: function(result){
              selectionLabels=result;
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
              });
            },
            error:function(error){
              alert("Error")
            }
  });

}

function setCurrentSelection(uId, url) {
  currentSelection = uId;
  selectionUrl = url;
  getSelectionMetadata(successCallback=function(){refreshViews('selection');});
}

function afterUpdate(updateRes) {
	newMeta = Object.assign(selectionMeta, updateRes);
	selectionMeta = newMeta;
	refreshViews('update');
}
