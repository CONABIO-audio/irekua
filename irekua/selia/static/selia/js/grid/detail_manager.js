var detailElement;
var detailHead;
var detailBody;


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
                '<span class="treegrid-expander glyphicon glyphicon-chevron-right"></span>' +
                '');

            children.hide();

            expander.on('click', function (e) {
                var $target = $(e.target);
                if (! $(children).is(':visible') ){
                    var $element = $($row);
                    $element
                        .find('.glyphicon-chevron-right')
                        .removeClass('glyphicon-chevron-right')
                        .addClass('glyphicon-chevron-down');
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
                .find('.glyphicon-chevron-down')
                .removeClass('glyphicon-chevron-down')
                .addClass('glyphicon-chevron-right');

            children.hide();
        }
    };
}

function addTreeNode(node,name,nodeId,parent,level){
    var tr = detailBody.insertRow();
    var strId = nodeId.toString();

    tr.setAttribute("data-id",strId);
    tr.setAttribute("data-parent",parent);
    tr.setAttribute("data-level",level);

    var name_col = document.createElement('td');
    var val_col = document.createElement('td');

    name_col.appendChild(document.createTextNode(name));
    name_col.setAttribute("data-column","name")

    nodeId = nodeId + 1;

    if (typeof node === 'object'){
        val_col.appendChild(document.createTextNode(""));
        tr.appendChild(name_col);
        tr.appendChild(val_col);
        
        for (var key in node){
            nodeId = addTreeNode(node[key],key,nodeId,strId,level+1)
        }

    } else {
        val_col.appendChild(document.createTextNode(node));

        tr.appendChild(name_col);
        tr.appendChild(val_col);
    }

    return nodeId;

}

function updateDetailBody() {
    while (detailBody.firstChild) {
        detailBody.removeChild(detailBody.firstChild);
    }
    var nextId = 1;
    if (selectionMeta != null){
        for (var key in selectionMeta){
            nextId = addTreeNode(selectionMeta[key],key,nextId,"0",1)
        }
    }
    configTableTreeView();


}

function init_detail() {
  createDetail();
}

$(document).ready(function() {
  init_detail();
});