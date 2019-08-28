var itemFileList = [];
var errorList = [];
var successList = [];
var req_count = 0;
var error_page_number = 0;
var total_error_pages = 0;
var error_page_step = 5;

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
function parseDate(fileName,parser_map){
  var date_context = fileName.match(parser_map["regexp"]);
  if (date_context){
    var date = ""

    date = date + date_context.toString().substring(parser_map["year"]["limits"][0],parser_map["year"]["limits"][1]);
    date = date + "-" + date_context.toString().substring(parser_map["month"]["limits"][0],parser_map["month"]["limits"][1]);
    date = date + "-" + date_context.toString().substring(parser_map["day"]["limits"][0],parser_map["day"]["limits"][1]);
    date = date+" "+date_context.toString().substring(parser_map["hour"]["limits"][0],parser_map["hour"]["limits"][1]);
    date = date + ":" + date_context.toString().substring(parser_map["minute"]["limits"][0],parser_map["minute"]["limits"][1])
    date = date + ":" + date_context.toString().substring(parser_map["second"]["limits"][0],parser_map["second"]["limits"][1])

    return date;
  }

  return "";

}
function validate_date(dateString,format="YYYY-MM-DD"){
  if (dateString != ""){
    if (moment(dateString, format,true).isValid()){
      return dateString;
    }
  }

  return false;
}
function validateFile(fileIndex, file, url, total_files, date_parser_map,date) {
  file["file_index"] = fileIndex;
  file["veto"] = false;

  if (date_parser_map){
    date = validate_date(parseDate(file.name,date_parser_map),format="YYYY-MM-DD hh:mm:ss");
  } else {
    date = validate_date(date);
  }

  if (date){
    file["captured_on"] = date;
  } else {
    file["captured_on"] = null;
  }

  switch (file.type){
    case 'image/jpeg':
    case 'image/jpg':{
      file["item_type"] = "Foto de Camara Trampa (jpg)";
      break;
    }
    case 'image/png':{
      file["item_type"] = "Foto de Camara Trampa (png)";
      break;
    }
    default:{
      file["item_type"] = null;
      break;
    }
  }

}
function validate_parser_map(pvalue){
      var example_date = {"year":"1985","month":"09","day":"19"}
      var pattern_mask = "";
      var pieces = [];
      var date_parser_map = {};
      var bad_date_map = false;
      var date_regexp = null;

      if (pvalue.includes('<') && pvalue.includes('>')){
        
        for(var i=0; i<pvalue.length;i++) {
          if (pvalue[i] == "<"){
            pattern_mask = pattern_mask + pvalue[i];
            for (var j=i+1; j<pvalue.length; j++){
              pattern_mask = pattern_mask + pvalue[j];
              if (pvalue[j] == ">"){
                pieces.push([i+1,j]);
                i = j;
                break;
              } else if (pvalue[j] == "<") {
                i = pvalue.length;
                break;
              }
            }
          } else {
            pattern_mask = pattern_mask + "_";
          }
        }
        
        if (pieces.length > 0){
          date_regexp = pvalue.substring(pieces[0][0]-1,pieces[pieces.length-1][1]+1);
          var cut_pattern = pattern_mask.substring(pieces[0][0]-1,pieces[pieces.length-1][1]+1).replace(/</g,"").replace(/>/g,"");

          for (var p=0;p<pieces.length;p++){
            var substr = pvalue.substring(pieces[p][0],pieces[p][1]);
            var substr_length = substr.length;
            var cat = distinctStr(substr);
            var parser_key = null;
            var start = 0;
            if (substr_length > 0 && cat.length == 1){
              switch(cat){
                case 'Y':{
                  if (substr_length == 4 || substr_length == 2){
                    parser_key = 'year';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'M':{
                  if (substr_length == 2){
                    parser_key = 'month';
                  } else {
                    bad_date_map = true;
                  }                    
                  break;
                }
                case 'D':{
                  if (substr_length == 2){
                    parser_key = 'day';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'h':{
                  if (substr_length == 2){
                    parser_key = 'hour';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 'm':{
                  if (substr_length == 2){
                    parser_key = 'minute';
                  } else {
                    bad_date_map = true;
                  }
                  break;
                }
                case 's':{
                  if (substr_length == 2){
                    parser_key = 'second';
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

              if (!bad_date_map){
                date_regexp = date_regexp.replace("<"+substr+">","\\d{"+substr_length+"}");
                start = cut_pattern.indexOf(substr);
                date_parser_map[parser_key] = {'limits':[start,start+substr_length],'length':substr_length,"order":p};
              }
              
            } else {
              bad_date_map = true;
            }

          }
          if (!bad_date_map){
            if ('year' in date_parser_map && 'month' in date_parser_map && 'day' in date_parser_map && 'second' in date_parser_map){
              date_parser_map["regexp"] = date_regexp;
              return date_parser_map;
            }
          }
        }
      }

      return false;
}

function get_file_page(items, page, per_page, filter) {
 
  var page = page || 1,
  per_page = per_page || 10,
  offset = (page - 1) * per_page,
  filteredItems = items.filter(filter),
  paginatedItems = filteredItems.slice(offset).slice(0, per_page),
  total_pages = Math.ceil(filteredItems.length / per_page);


  if (filteredItems.length <= per_page && filteredItems.length > 0){
    total_pages = 1;
  }
  return {
          page: page,
          per_page: per_page,
          pre_page: page - 1 ? page - 1 : null,
          next_page: (total_pages > page) ? page + 1 : null,
          total: filteredItems.length,
          total_pages: total_pages,
          data: paginatedItems
          };
}

function check_errors(f){
  if ((!f.item_type || !f.captured_on) && !f.veto){
    return true;
  } else {
    return false;
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
      select: function(event,ui){
        document.getElementById('term_type').value = ui.item.tax_obj.categoria_taxonomica;
      },
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
  //var itemFilePicker = document.getElementById('itemFilePicker');
  //var addItemForm = document.getElementById('addItemForm');
  var datepicker = document.getElementById('ui-datepicker-div');
  // var datePattern = document.getElementById('itemDatePattern');
  // var dateInput = document.getElementById('itemDate');
  // var dateErrorsContainer = document.getElementById('date_errors_container');
  // var dateErrors = document.getElementById('date_errors')
  var upload_item_form = document.getElementById('upload_item_form');
  var uploader_section = document.getElementById('uploader_section');

  if (upload_item_form && uploader_section){
    var uploader = new FileUploader(uploader_section,upload_item_form,"Upload items");
  }

  function renderErrorList(page,parent){
    while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
    }
    for (var i=0;i<page.data.length;i++){
        var errorRow = document.createElement('div');
        errorRow.className = 'row d-flex justify-content-between list_item';
        errorRow.align = "center";
        errorRow.style["margin"] = "10px";

        var descrCol = document.createElement('div');
        descrCol.className = 'col-3';
        var errorTypeCol = document.createElement('div');
        errorTypeCol.className = 'col-3';
        var fixerCol =  document.createElement('div');
        fixerCol.className = 'col-4';

        errorRow.appendChild(descrCol);
        errorRow.appendChild(errorTypeCol);
        errorRow.appendChild(fixerCol);

        var fileTitle = document.createElement('h5');
        fileTitle.textContent = 'File:';
        var fileName = document.createElement('div');
        fileName.className = "text-muted ml-4 ellipsise";
        fileName.textContent = page.data[i].name;

        var errorTitle = document.createElement('h5');
        errorTitle.textContent = 'Error type:';
        var errorName = document.createElement('div');
        errorName.className = "text-muted ml-4";

        errorTypeCol.appendChild(errorTitle);
        errorTypeCol.appendChild(errorName);
        descrCol.appendChild(fileTitle);
        descrCol.appendChild(fileName);

        var omitBtn = document.createElement('button');
        omitBtn.className = "btn btn-primary omit_btn"
        omitBtn.textContent = "Omit"
        omitBtn["file_index"] = page.data[i]["file_index"];

        omitBtn.onclick = function(e){
          itemFileList[this.file_index]["veto"] = true;
          var new_zero = get_file_page(itemFileList,0,error_page_step,filter=check_errors);
          error_page_number = Math.min(new_zero["total_pages"],error_page_number);
          var error_page = get_file_page(itemFileList,error_page_number,error_page_step,filter=check_errors);

          if (error_page.data.length > 0){
              total_error_pages = error_page["total_pages"];
              renderErrorList(error_page,dateErrors);
              $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
              dateErrorsContainer.style.display = "block";
          }
        }

        if (!page.data[i].item_type){
          errorName.textContent = "Wrong file type.";
          fixerCol.appendChild(omitBtn);

        } else if (!page.data[i].captured_on){
          errorName.textContent = "Date could not be parsed.";

          var new_input = document.createElement('input');
          new_input.type = "text";
          new_input.id = "date_input_file_"+page.data[i]["file_index"];
          $(new_input).datepicker({dateFormat: 'YYYY-MM-DD'});
          new_input.placeholder = "YYYY-MM-DD";

          var fixBtn = document.createElement('button');
          fixBtn.className = "btn btn-primary"
          fixBtn.textContent = "Fix"
          fixBtn["file_index"] = page.data[i]["file_index"];

          fixBtn.onclick = function(e){
            var raw_date = document.getElementById("date_input_file_"+this.file_index).value;
            var new_date = validate_date(raw_date);
            if (new_date){
              itemFileList[this.file_index]["captured_on"] = new_date;

              var new_zero = get_file_page(itemFileList,0,error_page_step,filter=check_errors);
              error_page_number = Math.min(new_zero["total_pages"],error_page_number);
              var error_page = get_file_page(itemFileList,error_page_number,error_page_step,filter=check_errors);

              if (error_page.data.length > 0){
                  total_error_pages = error_page["total_pages"];
                  renderErrorList(error_page,dateErrors);
                  $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
                  dateErrorsContainer.style.display = "block";
              }
            } else {
              alert("Please provide a valid date")
            }
          }

          fixerCol.appendChild(new_input);
          fixerCol.appendChild(fixBtn);
          fixerCol.appendChild(omitBtn);
        }
        parent.appendChild(errorRow);
      }
  }
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

  // if (itemFilePicker && addItemForm) {
  //   errorList = [];
  //   successList = [];
  //   itemFileList = [];
  //   req_count = 0;
  //   error_page_number = 0;
  //   total_error_pages = 0;
  //   error_page_step = 5;

  //   if (datePattern){
  //     document.getElementById('collapseDatePatternBtn').onclick = function(e){
  //       if ($("#collapseDatePattern").hasClass("show")){
  //           e.stopPropagation();
  //       } else {
  //           dateInput.value = "";
  //           $(dateInput).addClass('incorrect_pattern');
  //       }
  //     }
  //     document.getElementById('collapseDateBtn').onclick = function(e){
  //       if ($("#collapseDate").hasClass("show")){
  //           e.stopPropagation();
  //       } else {
  //           datePattern.value = "";
  //       }
  //     }
  //     document.getElementById('next_error_page').onclick = function(e){
  //       error_page_number = Math.min(total_error_pages,error_page_number+1);
  //       var error_page = get_file_page(itemFileList,error_page_number,error_page_step,filter=check_errors);
  //         if (error_page.data.length > 0){
  //           total_error_pages = error_page["total_pages"];
  //           renderErrorList(error_page,dateErrors);
  //           $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
  //           dateErrorsContainer.style.display = "block";
  //       }
  //     }
  //     document.getElementById('prev_error_page').onclick = function(e){
  //       error_page_number = Math.max(0,error_page_number-1);
  //       var error_page = get_file_page(itemFileList,error_page_number,error_page_step,filter=check_errors);
  //         if (error_page.data.length > 0){
  //           total_error_pages = error_page["total_pages"];
  //           renderErrorList(error_page,dateErrors);
  //           $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
  //           dateErrorsContainer.style.display = "block";
  //       }
  //     }
  //     document.getElementById('init_upload').onclick = function(e){
  //       var url = addItemForm.action + '&init_upload_session';
  //       var total_files = itemFileList.length;
  //       var parser_map = validate_parser_map(datePattern.value);
  //       var date_input = validate_date(dateInput.value);
  //       var go_on = true;
  //       var date_mode = "parse";

  //       if (total_files <= 0){
  //         alert('Please select at least one file');
  //         go_on = false;
  //       }

  //       if ($("#collapseDatePattern").hasClass("show")){
  //           if (!parser_map){
  //             alert('Incorrect date pattern');
  //             go_on = false;
  //           }
  //       } else {
  //           date_mode = "input";
  //           if (!date_input){
  //             alert('Incorrect date');
  //             go_on = false;
  //           }
  //       }


  //       if (go_on) {
  //         document.getElementById('selected_objects').style.display = 'none';
  //         document.getElementById('filePickerContainer').style.display = 'none';
  //         addItemForm.style.display = 'none';
  //         //document.getElementById('progress_upload').style.display = 'block';
  //         for (var i = 0; i < total_files; i++) {
  //           if (date_mode=="input"){
  //             validateFile(i, itemFileList[i], url, total_files,date=date_input);
  //           } else {
  //             validateFile(i, itemFileList[i], url, total_files,date_parser_map=parser_map);
  //           }
  //         }

  //         var error_page = get_file_page(itemFileList,0,5,filter=check_errors);
  //         if (error_page.data.length > 0){
  //           total_error_pages = error_page["total_pages"];
  //           renderErrorList(error_page,dateErrors);
  //           $('#error_paginator_label').html("Page "+error_page["page"]+"/"+error_page["total_pages"]);
  //           dateErrorsContainer.style.display = "block";
  //         }
  //       }
  //     };
  //     $(datePattern).bind('invalid', function() {
  //       return false;
  //     });
  //     datePattern.addEventListener('input',function(e){
  //       var parser_map = validate_parser_map(datePattern.value);
  //       if (parser_map){
  //         $(this).removeClass('incorrect_pattern')
  //       } else {
  //         $(this).addClass('incorrect_pattern')
  //       }
  //     });

  //     $(dateInput).datepicker("option", "onSelect", function(){
  //       var date_input = validate_date(dateInput.value);
  //       if (date_input){
  //         $(dateInput).removeClass('incorrect_pattern');
  //       } else {
  //         $(dateInput).addClass('incorrect_pattern');
  //       }
  //     });

  //     dateInput.addEventListener('input',function(e){
  //       var date_input = validate_date(dateInput.value);
  //       if (date_input){
  //         $(this).removeClass('incorrect_pattern');
  //       } else {
  //         $(this).addClass('incorrect_pattern');
  //       }
  //     });
  //   }

  //   itemFilePicker.addEventListener('change', function(e) {
  //     itemFileList = [];
  //     for (var i = 0; i < itemFilePicker.files.length; i++) {
  //       itemFileList.push(itemFilePicker.files[i]);

  //     }
  //   });

  //   addItemForm.addEventListener('submit', function(e) {
  //     e.preventDefault();
  //     var url = this.action + '&async=true';
  //     var total_files = itemFileList.length;

  //     if (total_files > 0) {
  //       document.getElementById('selected_objects').style.display = 'none';
  //       document.getElementById('filePickerContainer').style.display = 'none';
  //       addItemForm.style.display = 'none';
  //       document.getElementById('progress_upload').style.display = 'block';

  //       for (var i = 0; i < total_files; i++) {
  //         submitSingle(i, itemFileList[i], url, total_files);
  //       }
  //     } else {
  //       alert('Please select at least one file');
  //     }
  //   });
  // }


  if (sort_submit.length > 0) {
    sort_submit[0].onchange = function() {
      document.getElementById('filter_form').submit();
    };
  }
});
