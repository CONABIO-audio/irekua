var itemFileList = [];
var errorList = [];
var successList = [];
var req_count = 0;
var bad_date_map = false;
var date_parser_map = null;

$(function() {
  $('.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
});

$(document).on('click', '.ui-datepicker*', function(e) {
  e.stopPropagation();
});

$(document).on('click', '.dropdown-menu select*', function(e) {
  e.stopPropagation();
});



function submitSingle(fileIndex, file, url, total_files) {
  var formData = new FormData($('#addItemForm')[0]);
  var request = new XMLHttpRequest();

  formData.set('item_file', file);
  request.open('POST', url, false);
  request.send(formData);

  try {
    response_obj = JSON.parse(request.responseText);
    if (request.status == 200) {
      successList.push([file.name, request.status, response_obj]);
    } else {
      errorList.push([file.name, request.status, response_obj]);
    }
  } catch (error) {
    console.error(error);
  }
  req_count = req_count + 1;
  percent = Math.round((req_count * 100) / total_files);
  $('#progress_upload_bar')
    .css('width', percent + '%')
    .attr('aria-valuenow', percent);
  $('#progress_upload_bar span').html(percent + '%');

  if (fileIndex == total_files - 1) {
    showResults(url, errorList, successList);
  }
}

var showResults = function(url, errors, successes) {
  var duplicate_pks = [];
  var success_pks = [];

  for (var i = 0; i < errors.length; i++) {
    var error = errors[i];
    var error_data = error[2];
    if (error_data['error_type'] == 'duplicate') {
      duplicate_pks.push(error_data['duplicate_pk']);
    }
  }
  for (var i = 0; i < successes.length; i++) {
    var success = successes[i];
    var success_data = success[2];
    success_pks.push(success_data['success_pk']);
  }

  window.location.href =
    url +
    '&duplicate_pks=' +
    JSON.stringify(duplicate_pks) +
    '&success_pks=' +
    JSON.stringify(success_pks);
};

function toTitleCase(str) {
  str = str || '';
  str = str.replace('_', ' ');
  return str.replace(/\w\S*/g, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

function toTitleCase2(str) {
  str = str || '';
  str = str.replace('_', ' ');
  return str.replace(/\w\S*/, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

function asigna_autocomplete_tax($elems) {
  $elems.each(function() {
    if ($(this).autocomplete('instance')) $(this).autocomplete('destroy');
    $(this).autocomplete({
      source: function(request, response) {
        var termino = request.term + '*';
        $.ajax({
          url:
            '?slr_service=taxonomy&wt=json&q.op=AND&' +
            'q=((nombre:' +
            termino +
            ') OR (sinonimos:' +
            termino +
            ')' +
            ' OR (nombres_comunes:' +
            termino +
            '))',
          contentType: 'application/json',
          dataType: 'json',
          crossDomain: true,
          success: function(res) {
            response(
              $.map(res.response.docs, function(item) {
                var desc = [];
                var i = 0;
                while (item.sinonimos && i < item.sinonimos.length)
                  desc.push(toTitleCase2(item.sinonimos[i++]));
                i = 0;
                while (item.nombres_comunes && i < item.nombres_comunes.length)
                  desc.push(toTitleCase2(item.nombres_comunes[i++]));
                var texto = item.nombre;
                if (item.categoria_taxonomica == 'genero') texto += ' (Género)';
                else if (item.categoria_taxonomica != 'especie')
                  texto += ' (' + toTitleCase(item.categoria_taxonomica) + ')';
                var obj_ret = {label: texto, value: item.nombre, tax_obj: item};
                if (desc) obj_ret['desc'] = desc;
                return obj_ret;
              }),
            );
          },
        });
      },
    });
  });
}

function distinctStr(str) {
  return String.prototype.concat(...new Set(str))
}

$(document).ready(function() {
  var sort_submit = document.getElementsByClassName('sort_submit');
  var itemFilePicker = document.getElementById('itemFilePicker');
  var addItemForm = document.getElementById('addItemForm');
  var datepicker = document.getElementById('ui-datepicker-div');
  var datePattern = document.getElementById('itemDatePattern');

  if (datepicker) {
    function hide_if_pressed_and_shown(ddown, event) {
      if (datepicker.style.display != 'none') {
        event.preventDefault();
        datepicker.style.display = 'none';

        if ($(ddown).hasClass('show')) {
          $(ddown).removeClass('show');
          $(ddown.querySelector('.dropdown-menu')).removeClass('show');
        }
      }
    }

    function hide_if_not_datepicker(ddown, event) {
      if (datepicker.style.display == 'block') {
        event.preventDefault();
      }
    }

    var drop_downs = document.getElementsByClassName('dropdown');

    for (var i = 0; i < drop_downs.length; i++) {
      if (drop_downs[i].querySelector('.datepicker')) {
        $(drop_downs[i]).on('hide.bs.dropdown', function(e) {
          hide_if_not_datepicker(this, e);
        });
        $(drop_downs[i].querySelector('.dropdown-toggle')).on('click', function(
          e,
        ) {
          hide_if_pressed_and_shown(drop_downs[i], e);
        });
      } else {
        $(drop_downs[i].querySelector('.dropdown-toggle')).on('click', function(
          e,
        ) {
          if (datepicker.style.display != 'none') {
            datepicker.style.display = 'none';
          }
        });
      }
    }
  }

  if (itemFilePicker && addItemForm) {
    errorList = [];
    successList = [];
    itemFileList = [];
    req_count = 0;

    if (datePattern){
      datePattern.addEventListener('input',function(e){
        var example_date = {"year":"1985","month":"09","day":"19"}
        var pvalue = datePattern.value;
        var pieces = [];
        if (pvalue.includes('<') && pvalue.includes('>')){
          
          for(var i=0; i<pvalue.length;i++) {
            if (pvalue[i] == "<"){
              
              for (var j=i+1; j<pvalue.length; j++){
                if (pvalue[j] == ">"){
                  pieces.push([i+1,j]);
                  i = j;
                  break;
                } else if (pvalue[j] == "<") {
                  i = pvalue.length;
                  break;
                }
              }
            }
          }
          if (pieces.length > 0){
            date_parser_map = {};
            bad_date_map = false;
            for (var p=0;p<pieces.length;p++){
              var substr = pvalue.substring(pieces[p][0],pieces[p][1]);
              var substr_length = substr.length;
              var cat = distinctStr(substr);
              if (substr_length > 0 && cat.length == 1){
                switch(cat){
                  case 'y':{
                    if (substr_length == 4 || substr_length == 2){
                      date_parser_map['year'] = {'limits':pieces[p],'length':substr_length,"order":p}
                    } else {
                      bad_date_map = true;
                    }
                    break;
                  }
                  case 'm':{
                    if (substr_length == 2){
                      date_parser_map['month'] = {'limits':pieces[p],'length':substr_length,"order":p}
                    } else {
                      bad_date_map = true;
                    }                    
                    break;
                  }
                  case 'd':{
                    if (substr_length == 2){
                      date_parser_map['day'] = {'limits':pieces[p],'length':substr_length,"order":p}
                    } else {
                      bad_date_map = true;
                    }
                    break;
                  }
                  default:{
                    bad_date_map = true;
                    break;
                  }
                }
              } else {
                bad_date_map = true;
              }
            }
            if (!bad_date_map){
              if ('year' in date_parser_map && 'month' in date_parser_map && 'day' in date_parser_map){
                //alert(JSON.stringify(date_parser_map));
              }
            }
          }
        }
      });
    }

    itemFilePicker.addEventListener('change', function(e) {
      itemFileList = [];
      for (var i = 0; i < itemFilePicker.files.length; i++) {
        itemFileList.push(itemFilePicker.files[i]);

      }
    });

    addItemForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var url = this.action + '&async=true';
      var total_files = itemFileList.length;

      if (total_files > 0) {
        document.getElementById('selected_objects').style.display = 'none';
        document.getElementById('filePickerContainer').style.display = 'none';
        addItemForm.style.display = 'none';
        document.getElementById('progress_upload').style.display = 'block';

        for (var i = 0; i < total_files; i++) {
          submitSingle(i, itemFileList[i], url, total_files);
        }
      } else {
        alert('Please select at least one file');
      }
    });
  }

  if (sort_submit.length > 0) {
    sort_submit[0].onchange = function() {
      document.getElementById('filter_form').submit();
    };
  }
});
