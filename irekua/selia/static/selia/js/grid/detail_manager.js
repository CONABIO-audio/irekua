var detailElement;
var detailHead;
var detailBody;
var updateFormUrl;
var formChanged = false;


function createDetail() {
  if (detailElement === undefined) {
    detailElement = document.createElement("table");
    detailElement.setAttribute("id","tree-table");
    detailElement.className = "table table-hover table-bordered";

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
    registerUpdater("update", updateDetailBody);


  }
}

function configTableTreeView() {
    var
        $table = $('#tree-table'),
        rows = $table.find('tr');

    rows.each(function (index, row) {
        var
            $row = $(row),
            level = $row.data('level'),
            id = $row.data('id'),
            $columnName = $row.find('td[data-column="name"]'),
            children = $table.find('tr[data-parent="' + id + '"]');

        if (children.length) {
            var expander = $columnName.prepend('' +
                '<span class="treegrid-expander fa fa-chevron-right"></span>' +
                '');

            children.hide();

            expander.on('click', function (e) {
                var $target = $(e.target);
                if (! $(children).is(':visible') ){
                    var $element = $($row);
                    $element
                        .find('.fa-chevron-right')
                        .removeClass('fa-chevron-right')
                        .addClass('fa-chevron-down');
                    children.show();
                } else {

                    reverseHide($table,$row)
                }
            });
        }

        $columnName.prepend('' +
            '<span class="treegrid-indent" style="width:' + 15 * level + 'px"></span>' +
            '');
    });

    // Reverse hide all elements
    reverseHide = function (table, element) {
        var
            $element = $(element),
            id = $element.data('id'),
            children = table.find('tr[data-parent="' + id + '"]');

        if (children.length) {
            children.each(function (i, e) {
                reverseHide(table, e);
            });

            $element
                .find('.fa-chevron-down')
                .removeClass('fa-chevron-down')
                .addClass('fa-chevron-right');

            children.hide();
        }
    };
}

function addTreeNode(node,nodeKey,nodeName,nodeSpec,nodeId,parent,level){

    var tr = detailBody.insertRow();
    var strId = nodeId.toString();

    tr.setAttribute("data-id",strId);
    tr.setAttribute("data-parent",parent);
    tr.setAttribute("data-level",level);

    var name_col = document.createElement('td');
    var val_col = document.createElement('td');

    val_col.setAttribute("id","detail_"+nodeKey);


    name_col.appendChild(document.createTextNode(nodeName));
    name_col.setAttribute("data-column","name")

    nodeId = nodeId + 1;

    if (typeof node === 'object'){
        val_col.setAttribute("isNested",true);
        val_col.appendChild(document.createTextNode(""));
        tr.appendChild(name_col);
        tr.appendChild(val_col);

        for (var key in node){
            if (key != "url"){
                var childSpec = null;
                if (nodeSpec != null){
                    if (nodeSpec["type"] === "field"){
                        nodeId = addTreeNode(node[key],key,key,childSpec,nodeId,strId,level+1)
                    }else{
                        nodeId = addTreeNode(node[key],key,nodeSpec.children[key]["label"],nodeSpec.children[key],nodeId,strId,level+1)
                    }
                }else{
                        nodeId = addTreeNode(node[key],key,key,childSpec,nodeId,strId,level+1)
                }
            }
        }

    } else {
        val_col.setAttribute("isNested",false);
        val_col.appendChild(document.createTextNode(node));

        tr.appendChild(name_col);
        tr.appendChild(val_col);
    }

    return nodeId;

}

function loadUpdateForm(){

      formUrl = updateFormUrl+currentSelection.toString()+"/"

      $.ajax({url:formUrl,
        type:"GET",
        success: function(result){
            var html = $.parseHTML(result);
            var updateForm = document.getElementById("updateModal");

            if (updateForm){
                $("#updateModal").replaceWith(result);
            } else {
                  $("#detailContainer").append(html);
                  $('#updateForm').submit(function(event) {
                          event.preventDefault();
                          var updateParams = getUpdateParams();
                          $.ajax({url:selectionUrl,
                            type:"PUT",
                            data: updateParams,
                            success: function(result){
                                alert(result);
                                afterUpdate(result);
                            },
                            error:function(error){
                              alert(JSON.stringify(error))
                            }
                          });
                    
                  });
            }

            
            
        },
        error:function(error){
          alert("Error");
        }
      });

      configTableTreeView();
}

function updateDetailBody() {
    while (detailBody.firstChild) {
        detailBody.removeChild(detailBody.firstChild);
    }
    var nextId = 1;
    if (selectionMeta != null){
        for (var key in selectionMeta){
            if (key != "url"){
                nextId = addTreeNode(selectionMeta[key],key,selectionLabels.actions.GET[key]["label"],selectionLabels.actions.GET[key],nextId,"0",1)
            }
        }
    }
    $("#detailLabel").text("ID:"+currentSelection);
    loadUpdateForm()
}

function onUpdateFormChanged(event){
    formChanged = true;
}


function getUpdateParams(){
      alert("before")
      var formObjects = $('#updateForm').serializeArray();
      alert(formObjects);

      var updateParams = "";
      var first = true;
      for (var i = 0; i < formObjects.length; i++ in formObjects){
        var obj = formObjects[i]

        var key = obj["name"];
        if (key != "initial-metadata"){
            if (!first){
                updateParams += "&"+key+"="+obj["value"];
            } else {
                updateParams += key+"="+obj["value"];
                first = false;
            }
        }

      }
      return updateParams;
}

function init_detail() {
  createDetail();
}


$(document).ready(function() {
  init_detail();
});
