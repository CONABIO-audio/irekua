var tableUrl;
var tableElement;
var tableData;
var tableHeadData;
var tableBody;
var tableHead;
var tableFoot;
var tablePagination;
var tablePageSizeMenu;

var tableConfiguration = {};

var filterQueryStr = "";
var searchQueryStr = "";
var pageSizeOptions = [5, 10, 20, 50, 100];
var pageSize = 5;
var page = 1;


function loadConfiguration() {
  var text = $('#withTableLinks').text().trim();
  var withTableLinks = text.toLowerCase() == "true";
  tableConfiguration['withTableLinks'] = withTableLinks;
}


function linkElements() {
  if (tableElement === undefined) {
    tableElement = document.getElementById('table');
  }

  if (tableHead === undefined) {
    tableHead = document.getElementById('tableHead');
  }

  if (tableBody === undefined) {
    tableBody = document.getElementById('tableBody');
  }

  if (tableFoot === undefined) {
    tableFoot = document.getElementById('tableFoot');
  }

  if (tablePagination === undefined) {
    tablePagination = document.getElementById('pagination');
  }

  if (tablePageSizeMenu === undefined) {
    tablePageSizeMenu = document.getElementById('pageSizeSelector');
  }
}

function pageSizeMenuOnClickFactory(pageSizeOption) {
  return function() {
    pageSize = pageSizeOption;
    getTableData();
    updatePageSizeSelectionMenu();
  }
}


function updatePageSizeSelectionMenu() {
  clearElement(tablePageSizeMenu);

  for (var i = 0; i < pageSizeOptions.length; i++) {
    var pageSizeOption = pageSizeOptions[i];
    var a = document.createElement('a');
    a.className = (pageSizeOption == pageSize) ? "dropdown-item active" : "dropdown-item";
    a.href = "#";
    a.onclick = pageSizeMenuOnClickFactory(pageSizeOption);
    a.appendChild(document.createTextNode(pageSizeOption));

    tablePageSizeMenu.appendChild(a);
  }
}


function clearElement(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}


function paginationOnClickFactory(index) {
  return function() {
    page = index;
    getTableData();
  }
}

function updatePagination() {
  clearElement(tablePagination);

  var li = document.createElement('li');
  li.className = "page-item";
  var a = document.createElement('a');
  a.className = "page-link";
  a.setAttribute("aria-label", "Previous");
  var span = document.createElement('span');
  span.setAttribute("aria-hidden", "true");

  span.appendChild(document.createTextNode('\u00AB'));
  a.appendChild(span);
  li.appendChild(a);
  tablePagination.appendChild(li);

  var count = tableData.count;
  var pages = Math.ceil(parseInt(count) / parseInt(pageSize));
  var reference = document.getElementById('next');
  for (var i = 1; i <= pages; i++) {
    var li = document.createElement('li');
    li.className = (page === i) ? "page-item active" : "page-item";

    var a = document.createElement('a');
    a.className = "page-link";
    a.href = "#";
    a.onclick = paginationOnClickFactory(i)
    a.appendChild(document.createTextNode(i));

    li.appendChild(a);
    tablePagination.appendChild(li);
  }

  li = document.createElement('li');
  li.className = "page-item";
  a = document.createElement('a');
  a.className = "page-link";
  a.setAttribute("aria-label", "Next");
  span = document.createElement('span');
  span.setAttribute("aria-hidden", "true");

  span.appendChild(document.createTextNode('\u00BB'));
  a.appendChild(span);
  li.appendChild(a);
  tablePagination.appendChild(li);
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
  clearElement(tableBody)

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
  tableUrl = $('#tableUrl').text().trim();
}

function getTableUrl() {
  var searchStr = (searchQueryStr === "") ? "" : "&" + searchQueryStr;
  var queryStr = (filterQueryStr === "") ? "" : "&" + filterQueryStr;
  return `${tableUrl}?page=${page}&page_size=${pageSize}${searchStr}${queryStr}`;
}


function getTableData() {
  if (tableUrl === undefined) {
    setTableUrl();
  }

  var url = getTableUrl();
  console.log(url);

  $.ajax({
    type: 'GET',
    url: url,
    success: function(response) {
      tableData = response;
      updateTableBody();
      updatePagination();
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

function tableInit() {
  loadConfiguration()
  linkElements();
  updatePageSizeSelectionMenu();
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
    pageSize = $(this).serialize()
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

  tableInit();
});
