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

function afterUpdate() {
  getSelectionMetadata(successCallback=function(){refreshViews('update');});
}

var detailShown = true;
var mapShown = true;
var summaryShown = true;
var tableShown = true;

function toggleSummaryView() {
  $('#summaryPanel').toggleClass("collapsed");
  $('#toggleSummaryButton').toggleClass("text-muted");

  if (summaryShown) {
    document.getElementById('toggleSummaryIcon').className = "fas fa-toggle-off";
  } else {
    document.getElementById('toggleSummaryIcon').className = "fas fa-toggle-on";
  }

  summaryShown = !summaryShown;
}

function toggleDetailView() {
  $('#detailPanel').toggleClass("collapsed");
  $('#toggleDetailButton').toggleClass("text-muted");

  if (detailShown) {
    document.getElementById('toggleDetailIcon').className = "fas fa-toggle-off";
  } else {
    document.getElementById('toggleDetailIcon').className = "fas fa-toggle-on";
  }

  detailShown = !detailShown;
}

function toggleMapView() {
  $('#mapPanel').toggleClass("collapsed");
  $('#toggleMapButton').toggleClass("text-muted");

  if (mapShown) {
    document.getElementById('toggleMapIcon').className = "fas fa-toggle-off";
  } else {
    document.getElementById('toggleMapIcon').className = "fas fa-toggle-on";
  }

  mapShown = !mapShown;
}

function toggleTableView() {
  $('#tablePanel').toggleClass("collapsed");
  $('#toggleTableButton').toggleClass("text-muted");

  if (tableShown) {
    document.getElementById('toggleTableIcon').className = "fas fa-toggle-off";
  } else {
    document.getElementById('toggleTableIcon').className = "fas fa-toggle-on";
  }

  tableShown = !tableShown;
}



$(document).ready(function() {
  $('#toggleTableButton').click(function() {
    toggleTableView();
  });

  $('#toggleSummaryButton').click(function() {
    toggleSummaryView();
  });

  $('#toggleDetailButton').click(function(event) {
    toggleDetailView();
  });

  $('#toggleMapButton').click(function() {
    toggleMapView();
  });
});
