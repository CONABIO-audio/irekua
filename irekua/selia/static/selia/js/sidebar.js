function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function updateCookie() {
	var expanded = getCookie("expanded");

	if (expanded == "") {
		setCookie("expanded", true, 1);
    expanded = false;
	} else if (expanded == 'true') {
		setCookie("expanded", false, 1);
    expanded = false;
	} else {
		setCookie("expanded", true, 1);
    expanded = true;
	}

  $.post('/selia/update_session/', {expanded: expanded});

	checkCollapse()

	return false;
}

function checkCollapse() {
	var expanded = getCookie("expanded");

	if (expanded == "true") {
		$("#sidebar").removeClass("collapsed");
		$("#content").removeClass("col-md-12").addClass("col-md-9");
	} else {
		$("#sidebar").addClass("collapsed");
		$("#content").removeClass("col-md-9").addClass("col-md-12");
	}

}

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

$(document).ready(function () {
	$(".toggle-sidebar").click(updateCookie);
});
