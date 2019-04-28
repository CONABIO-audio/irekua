var tableUrl;
var tableElement;
var tableData;
var tableHeadData;
var tableBody;
var tableHead;
var tableFoot;
var tablePagination;

var tableConfiguration = {};

var filterQueryStr = "";
var searchQueryStr = "";
var pageSizeStr = "";

var defaultPageSize = 10;


function loadConfiguration() {
  var text = $('#withTableLinks').text().trim();
  var withTableLinks = text.toLowerCase() == "true";
  tableConfiguration['withTableLinks'] = withTableLinks;
}


function createTable() {
  if (tableElement === undefined) {
    tableElement = document.getElementById('table');
    tableHead = document.getElementById('tableHead');
    tableBody = document.getElementById('tableBody');
    tableFoot = document.getElementById('tableFoot');
  }
}


function createPaginator() {
  if (tablePagination === undefined) {

  }

}

function updateTableHead() {
  var tr = tableHead.insertRow();
  for (var key in tableHeadData.actions.GET) {
    var label = tableHeadData.actions.GET[key]["label"];
    if (label.toLowerCase() == 'url') continue;

    var th = document.createElement('th');
    th.appendChild(document.createTextNode(label));
    tr.appendChild(th);
  }

  if (tableConfiguration['withTableLinks']) {
    var th = document.createElement('th');
    th.appendChild(document.createTextNode("acciones"));
    tr.appendChild(th);
  }


}

function updateTableBody() {
  while (tableBody.firstChild) {
    tableBody.removeChild(tableBody.firstChild);
  }

  tableData.results.forEach(function(datum) {
    var tr = tableBody.insertRow();

    var pk;
    if ('id' in datum) {
      pk = datum['id'];
    } else {
      pk = datum['name'];
    }

    tr.setAttribute('url', datum['url']);
    tr.onclick = function() {
      setCurrentSelection(pk, datum['url'])
    }

    for (var key in datum) {
      if (key.toLowerCase() == 'url') continue;

      var td = tr.insertCell();
      td.appendChild(document.createTextNode(datum[key]));
    }

    if (tableConfiguration['withTableLinks']) {
      var td = tr.insertCell();


      var link = document.createElement('a');
      link.className = "btn btn-link"
      link.appendChild(document.createTextNode("Entrar"))
      link.href = "#";
      link.onclick = function() {
        $.post('#', {action: 'enter', pk: pk}, function(data) {
          window.location = data.url;
        })
      }
      td.appendChild(link);
    }
  })
}


function setTableUrl() {
  tableUrl = $('#tableUrl').text();
}


function getTableData() {
  if (tableUrl === undefined) {
    setTableUrl();
  }

  var url = `${tableUrl}?${filterQueryStr}`;

  $.ajax({
    type: 'GET',
    url: url,
    success: function(response) {
      tableData = response;
      updateTableBody();
    }
  });
}

function getTableHeadData() {
  if (tableUrl === undefined) {
    setTableUrl();
  }

  $.ajax({
    type: 'OPTIONS',
    url: tableUrl,
    success: function(response) {
      tableHeadData = response;
      updateTableHead();
    }
  });
}


function init() {
  loadConfiguration()
  createTable();
  getTableData();
  getTableHeadData();
}

$(document).ready(function() {
  $('#filterForm').submit(function() {
    filterQueryStr = $(this).serialize()
    getTableData();
  });

  $('#searchForm').submit(function() {
    searchQueryStr = $(this).serialize()
    getTableData();
  });

  $('#pageSizeForm').submit(function() {
    pageSizeStr = $(this).serialize()
    getTableData();
  });

  $('.django-form').submit(function() {
    var data = `${$(this).serialize()}&action=${$(this).attr('id')}`;
    $.ajax({
      data: data,
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      success: function(response) {
          $(this).parent().html(response);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log({jqXHR, textStatus, errorThrown})
      }
    });
    return false;
  })

  init();
});
