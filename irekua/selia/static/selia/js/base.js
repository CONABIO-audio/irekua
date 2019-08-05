var itemFileList = [];
var errorList = [];
var successList = [];
var req_count = 0;


$( function() {
            $( ".datepicker" ).datepicker();
        } );


$(document).on('click', '.ui-datepicker*', function (e) {
        e.stopPropagation();
});


function submitSingle(fileIndex,file,url,total_files){
 	var formData = new FormData($('#addItemForm')[0]);
 	var request = new XMLHttpRequest();

 	formData.set('item_file',file);
 	request.open("POST",url,false);
 	request.send(formData);

	try {
		response_obj = JSON.parse(request.responseText);
	 	if (request.status == 200){
	 		successList.push([file.name,request.status,response_obj]);
	 	} else {
	 		errorList.push([file.name,request.status,response_obj]);
	 	}
	}
	catch(error) {
	  console.error(error);
	}
	req_count = req_count + 1;
 	percent = Math.round(req_count*100/total_files);
 	$('#progress_upload_bar').css('width', percent+'%').attr('aria-valuenow', percent);
 	$('#progress_upload_bar span').html( percent+'%');

 	if (fileIndex == total_files - 1){
 		showResults(url,errorList,successList);
 	}
 };

 var showResults = function(url,errors,successes){
	var duplicate_pks = [];
	var success_pks = [];

	for (var i=0;i<errors.length;i++){
		var error = errors[i];
		var error_data = error[2];
		if (error_data["error_type"] == "duplicate"){
			duplicate_pks.push(error_data["duplicate_pk"]);
		}
	}
	for (var i=0;i<successes.length;i++){
		var success = successes[i];
		var success_data = success[2];
		success_pks.push(success_data["success_pk"])
	}

	window.location.href = url+"&duplicate_pks="+JSON.stringify(duplicate_pks)+"&success_pks="+JSON.stringify(success_pks);
}

function toTitleCase(str) {
    str = str || '';
    str = str.replace('_',' ');
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + 
        txt.substr(1).toLowerCase();});
}

function toTitleCase2(str) {
    str = str || '';
    str = str.replace('_',' ');
    return str.replace(/\w\S*/, function(txt){return txt.charAt(0).toUpperCase() + 
        txt.substr(1).toLowerCase();});
}

function asigna_autocomplete_tax($elems) {
    $elems.each(function() {
        if($(this).autocomplete("instance"))
            $(this).autocomplete("destroy");
        $(this).autocomplete({
            source : function (request, response){
                var termino = request.term+'*';
                $.ajax({
                    url: '?slr_service=taxonomy&wt=json&q.op=AND&'+
                        'q=((nombre:'+termino+') OR (sinonimos:'+termino+')'+
                            ' OR (nombres_comunes:'+termino+'))',
                    contentType: 'application/json',dataType:'json',crossDomain: true,
                    success : function (res) {
                        response($.map(res.response.docs, function (item){
                            var desc = [];
                            var i = 0;
                            while(item.sinonimos && i < item.sinonimos.length)
                                desc.push(toTitleCase2(item.sinonimos[i++]))
								i = 0;
                    		while(item.nombres_comunes && i < item.nombres_comunes.length)
                        		desc.push(toTitleCase2(item.nombres_comunes[i++]));
                            var texto = item.nombre;
                            if(item.categoria_taxonomica == 'genero')
                                texto += ' (Género)';
                            else if(item.categoria_taxonomica != 'especie')
                                texto += ' ('+toTitleCase(item.categoria_taxonomica)+')';
                            var obj_ret = {label:texto,value:item.nombre,tax_obj:item};
                            if(desc)
                                obj_ret['desc'] = desc;
                            return obj_ret;
                        }));
                    }
                });
            }
        });
    });
}

$( document ).ready(function() {
    var sort_submit = document.getElementsByClassName("sort_submit");
    var itemFilePicker = document.getElementById('itemFilePicker');
    var addItemForm = document.getElementById('addItemForm');

    if (itemFilePicker && addItemForm) {
    	errorList = [];
    	successList = [];
		itemFileList = [];
		req_count = 0;

        itemFilePicker.addEventListener('change',function(e){
            itemFileList = [];
            for (var i=0; i<itemFilePicker.files.length;i++) {
                itemFileList.push(itemFilePicker.files[i]);
            }
        });

        addItemForm.addEventListener('submit',function(e){
            e.preventDefault();
            document.getElementById('selected_objects').style.display = "none";
            document.getElementById('filePickerContainer').style.display="none";
			addItemForm.style.display = "none";
			document.getElementById('progress_upload').style.display = "block";

            var url = this.action+"&async=true";
			var total_files = itemFileList.length;

            if (total_files > 0){
	            for (var i=0;i<total_files;i++){
	                submitSingle(i,itemFileList[i],url,total_files);
	            }
            } else {
            	alert("{% trans 'No selected files. Please select at least one file to upload' %}");
            }
        });
    }

    if (sort_submit.length > 0){
        sort_submit[0].onchange = function(){
            document.getElementById('filter_form').submit();
        }
    }
});

