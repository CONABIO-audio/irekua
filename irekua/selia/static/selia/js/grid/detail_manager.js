var detailElement;


function createDetail() {
  if (detailElement === undefined) {
    detailElement = document.createElement("table");
    detailElement.className = "table";

    detailHead = document.createElement("thead");

    detailElement.appendChild(detailHead);

    detailBody = document.createElement('tbody');
    detailBody.className = "table-body"

    detailElement.appendChild(detailBody);


    $('#detailContainer').append(detailElement);

    var tr = detailHead.insertRow();
    var at_head = document.createElement('th');
    var val_head = document.createElement('th');
    at_head.appendChild(document.createTextNode("Atributo"));
    val_head.appendChild(document.createTextNode("Valor"));
    tr.appendChild(at_head);
    tr.appendChild(val_head);

    registerUpdater("selection", updateDetailBody);

  }
}

function updateDetailBody() {
    alert("refresh detail body")
}

function init_detail() {
  createDetail();
}

$(document).ready(function() {
  init_detail();
});