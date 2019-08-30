class FileUploader {
	constructor(parent,form,title){
		this.parent = parent;
		this.form = form;
		this.title = title;
		this.initialize();
	}
	initialize() {
		this.files = [];
		this.last_id = 0;
		this.file_page_number = 1;
		this.duplicate_page_number = 1;
		this.error_page_number = 1;
		this.upload_page_number = 1;
		this.total_file_pages = 0;
		this.total_duplicate_pages = 0;
		this.total_error_pages = 0;
		this.total_upload_pages = 0;
		this.per_page = 10;
		this.build_view();
	}
	build_view() {
		this.build_top_toolbar();
		this.build_progress_bar();
		this.build_body();
	}
	build_progress_bar() {
		this.progress_container = document.createElement('div');
		this.progress_container.className = "row p-2 w-100";
		this.progress_container.style.display = "none";

		var progress_outer = document.createElement('div');
		progress_outer.className = "progress w-100";

		this.progress_bar = document.createElement('div');
		this.progress_bar.className = "progress-bar progress-bar-success progress-bar-striped";
		this.progress_bar.role = "progressbar";
		this.progress_bar.style.width = "0%";
		this.progress_bar.setAttribute('aria-valuenow','0');
		this.progress_bar.setAttribute('aria-valuemin','0');
		this.progress_bar.setAttribute('aria-valuemax','100');
		
		this.progress_bar_label = document.createElement('span');
		this.progress_bar_label.innerHTML = '0%';

		this.progress_bar.appendChild(this.progress_bar_label);
		progress_outer.appendChild(this.progress_bar);

		this.progress_container.appendChild(progress_outer);

	}
	build_top_toolbar() {
		if (this.top_toolbar){
			$(this.top_toolbar).remove();
		}
		var widget = this;

		this.top_toolbar = document.createElement('div');
		this.top_toolbar.className = 'row w-100';

		var toolbar_container = document.createElement('div');
		toolbar_container.className = "container-fluid p-2 w-100 bg-dark rounded";
		
		var row = document.createElement('div');
		row.className = "row";
		row.align = "center";


		var file_picker_col = document.createElement('div');
		file_picker_col.className = "col";

		var file_btn = document.createElement('label');
		file_btn.htmlFor = "file_picker";
		file_btn.className ="upload_tool text-light";

		var add_label = document.createTextNode("Agregar ");
		var add_icon = document.createElement('i');
		add_icon.className = "fas fa-plus";
		file_btn.appendChild(add_label);
		file_btn.appendChild(add_icon);

		this.file_picker = document.createElement('input');
		this.file_picker.id = "file_picker";
		this.file_picker.type = "file";
		this.file_picker.style.display = "none";
		this.file_picker.setAttribute("multiple","");

		file_picker_col.appendChild(file_btn);
		file_picker_col.appendChild(this.file_picker);


		var upload_col = document.createElement('div');
		upload_col.className = "col";

		var upload_dropdown = document.createElement('div');
		upload_dropdown.className = "dropdown";

		var upload_anchor = document.createElement('a');
		upload_anchor.setAttribute('data-toggle','dropdown');
		upload_anchor.setAttribute('role','button');
		upload_anchor.setAttribute('aria-expanded',false);
		upload_anchor.setAttribute('aria-controls','collapseUpload')

		var upload_btn_label = document.createElement('label');
		upload_btn_label.className ="upload_tool text-light";
		var upload_label = document.createTextNode('Subir ');
		var upload_icon = document.createElement('i');

		upload_icon.className = "fas fa-upload";
		upload_btn_label.appendChild(upload_label);
		upload_btn_label.appendChild(upload_icon);

		upload_anchor.appendChild(upload_btn_label);
		upload_dropdown.appendChild(upload_anchor);

		var upload_dropdown_menu = document.createElement('div');
		upload_dropdown_menu.className = "dropdown-menu text-light";
		upload_dropdown_menu.style["background-color"] = "#454d54";
		upload_dropdown_menu.style.width = "auto";
		upload_dropdown_menu.setAttribute('aria-labelledby','dropdownMenuButton');

		var upload_dropdown_menu_inner = document.createElement('div');
		upload_dropdown_menu_inner.className = "container-fluid";

		var upload_all_btn_row = document.createElement('div');
		upload_all_btn_row.className = "row upload_tool justify-content-center";

		this.upload_all_btn = document.createElement("a");
		this.upload_all_btn.innerHTML = "<h6>Listos</h6";
		upload_all_btn_row.appendChild(this.upload_all_btn);

		var upload_selected_btn_row = document.createElement('div');
		upload_selected_btn_row.className = "row upload_tool justify-content-center";

		this.upload_selected_btn = document.createElement("a");
		this.upload_selected_btn.innerHTML = "<h6>Selección</h6>";
		upload_selected_btn_row.appendChild(this.upload_selected_btn);

		upload_dropdown_menu_inner.appendChild(upload_selected_btn_row);
		upload_dropdown_menu_inner.appendChild(upload_all_btn_row);

		upload_dropdown_menu.appendChild(upload_dropdown_menu_inner);
		upload_dropdown.appendChild(upload_dropdown_menu);

		upload_col.appendChild(upload_dropdown);



		var remove_col = document.createElement('div');
		remove_col.className = "col";

		var remove_dropdown = document.createElement('div');
		remove_dropdown.className = "dropdown";

		var remove_anchor = document.createElement('a');
		remove_anchor.setAttribute('data-toggle','dropdown');
		remove_anchor.setAttribute('role','button');
		remove_anchor.setAttribute('aria-expanded',false);
		remove_anchor.setAttribute('aria-controls','collapseUpload')

		var remove_btn_label = document.createElement('label');
		remove_btn_label.className ="upload_tool text-light";
		var remove_label = document.createTextNode('Cancelar ');
		var remove_icon = document.createElement('i');

		remove_icon.className = "fas fa-trash";
		remove_btn_label.appendChild(remove_label);
		remove_btn_label.appendChild(remove_icon);



		remove_anchor.appendChild(remove_btn_label);
		remove_dropdown.appendChild(remove_anchor);

		var remove_dropdown_menu = document.createElement('div');
		remove_dropdown_menu.className = "dropdown-menu text-light";
		remove_dropdown_menu.style["background-color"] = "#454d54";
		remove_dropdown_menu.style.width = "auto";
		remove_dropdown_menu.setAttribute('aria-labelledby','dropdownMenuButton');

		var remove_dropdown_menu_inner = document.createElement('div');
		remove_dropdown_menu_inner.className = "container-fluid";

		var remove_all_btn_row = document.createElement('div');
		remove_all_btn_row.className = "row upload_tool justify-content-center";

		this.remove_all_btn = document.createElement("a");
		this.remove_all_btn.innerHTML = "<h6>Todo</h6>";

		remove_all_btn_row.appendChild(this.remove_all_btn);

		var remove_selected_btn_row = document.createElement('div');
		remove_selected_btn_row.className = "row upload_tool justify-content-center";

		this.remove_selected_btn = document.createElement("a");
		this.remove_selected_btn.innerHTML = "<h6>Selección</h6>";
		remove_selected_btn_row.appendChild(this.remove_selected_btn);

		remove_dropdown_menu_inner.appendChild(remove_selected_btn_row);
		remove_dropdown_menu_inner.appendChild(remove_all_btn_row);

		remove_dropdown_menu.appendChild(remove_dropdown_menu_inner);
		remove_dropdown.appendChild(remove_dropdown_menu);

		remove_col.appendChild(remove_dropdown);

		var date_toggle_col = document.createElement('div');
		date_toggle_col.className = "col";

		var date_toggle_dropdown = document.createElement('div');
		date_toggle_dropdown.className = "mb-0";

		var date_toggle_anchor = document.createElement('a');
		date_toggle_anchor.className = "dropdown-toggle";
		date_toggle_anchor.setAttribute('data-toggle','collapse');
		date_toggle_anchor.setAttribute('href','#date_tools');

		var date_toggle_btn_label = document.createElement('label');
		date_toggle_btn_label.className ="upload_tool text-light";
		var date_toggle_label = document.createTextNode('Editar momento ');
		//var date_toggle_icon = document.createElement('i');

		//date_toggle_icon.className = "fas fa-trash";
		date_toggle_btn_label.appendChild(date_toggle_label);
		//date_toggle_btn_label.appendChild(date_toggle_icon);

		date_toggle_anchor.appendChild(date_toggle_btn_label);
		date_toggle_dropdown.appendChild(date_toggle_anchor);

		date_toggle_col.appendChild(date_toggle_dropdown);

		row.appendChild(file_picker_col);
		row.appendChild(upload_col);
		row.appendChild(remove_col);
		row.appendChild(date_toggle_col);


    	var row2 = document.createElement("div");
		row2.className = "row collapse justify-content-between";
		row2.id = "date_tools";
		row2.style["padding-left"] = "60px";

		var date_pattern_col = document.createElement('div');

		date_pattern_col.className = "col";
		var date_pattern_label = document.createElement('label');
		date_pattern_label.className = "upload_tool text-light";
		date_pattern_label.appendChild(document.createTextNode('Patrón: '));
		date_pattern_label.htmlFor = "itemDatePattern";

		this.date_pattern_input = document.createElement('input');
		this.date_pattern_input.style.width = "300px";
		this.date_pattern_input.className = "incorrect_pattern";
		this.date_pattern_input.type = "text";
		this.date_pattern_input.id = "itemDatePattern";
		this.date_pattern_input.placeholder = "<YYYY>-<MM>-<DD>_<hh>:<mm>:<ss>_.wav";

		var date_pattern_apply_dropdown = document.createElement('div');
		date_pattern_apply_dropdown.className = "dropdown";

		var date_pattern_apply_anchor = document.createElement('a');
		date_pattern_apply_anchor.setAttribute('data-toggle','dropdown');
		date_pattern_apply_anchor.setAttribute('role','button');
		date_pattern_apply_anchor.setAttribute('aria-expanded',false);
		date_pattern_apply_anchor.setAttribute('aria-controls','collapseUpload')

		var date_pattern_apply_btn_label = document.createElement('label');
		date_pattern_apply_btn_label.className ="upload_tool text-light";
		var date_pattern_apply_icon = document.createElement('i');
		date_pattern_apply_icon.className = "fas fa-arrow-alt-circle-right";

		date_pattern_apply_btn_label.appendChild(date_pattern_apply_icon);


		date_pattern_apply_anchor.appendChild(date_pattern_apply_btn_label);
		date_pattern_apply_dropdown.appendChild(date_pattern_apply_anchor);

		var date_pattern_apply_dropdown_menu = document.createElement('div');
		date_pattern_apply_dropdown_menu.className = "dropdown-menu text-light";
		date_pattern_apply_dropdown_menu.style["background-color"] = "#454d54";
		date_pattern_apply_dropdown_menu.style.width = "auto";
		date_pattern_apply_dropdown_menu.setAttribute('aria-labelledby','dropdownMenuButton');

		var date_pattern_apply_dropdown_menu_inner = document.createElement('div');
		date_pattern_apply_dropdown_menu_inner.className = "container-fluid";

		var date_pattern_apply_all_btn_row = document.createElement('div');
		date_pattern_apply_all_btn_row.className = "row upload_tool justify-content-center";

		this.date_pattern_apply_all_btn = document.createElement("a");
		this.date_pattern_apply_all_btn.innerHTML = "<h6>Todo</h6>";

		date_pattern_apply_all_btn_row.appendChild(this.date_pattern_apply_all_btn);

		var date_pattern_apply_selected_btn_row = document.createElement('div');
		date_pattern_apply_selected_btn_row.className = "row upload_tool justify-content-center";

		this.date_pattern_apply_selected_btn = document.createElement("a");
		this.date_pattern_apply_selected_btn.innerHTML = "<h6>Selección</h6>";
		date_pattern_apply_selected_btn_row.appendChild(this.date_pattern_apply_selected_btn);

		date_pattern_apply_dropdown_menu_inner.appendChild(date_pattern_apply_selected_btn_row);
		date_pattern_apply_dropdown_menu_inner.appendChild(date_pattern_apply_all_btn_row);

		date_pattern_apply_dropdown_menu.appendChild(date_pattern_apply_dropdown_menu_inner);
		date_pattern_apply_dropdown.appendChild(date_pattern_apply_dropdown_menu);

		var date_pattern_row = document.createElement('div');
		date_pattern_row.className = "row d-flex";

		date_pattern_row.appendChild(date_pattern_label);
		date_pattern_row.appendChild(this.date_pattern_input);
		date_pattern_row.appendChild(date_pattern_apply_dropdown)

		date_pattern_col.appendChild(date_pattern_row);

		//Date

		var date_col = document.createElement('div');
		date_col.className = "col";
		var date_label = document.createElement('label');
		date_label.className = "upload_tool text-light";
		date_label.appendChild(document.createTextNode('Fecha: '));
		date_label.htmlFor = "itemDate";

		this.date_input = document.createElement('input');
		this.date_input.className = "incorrect_pattern";
		this.date_input.style.width = "110px";
		this.date_input.type = "text";

		$(this.date_input).datetimepicker({
			format:'Y-m-d',
			timepicker: false,
			closeOnDateSelect: true,
			validateOnBlur: false,
			onChangeDateTime: function(dp,$input){
		        var date_input = widget.validate_datetime($input.val());
		        if (date_input){
		          $($input).removeClass('incorrect_pattern');
		        } else {
		          $($input).addClass('incorrect_pattern');
		        }
		    }
		});


        this.date_input.placeholder = "YYYY-MM-DD";


		var date_apply_dropdown = document.createElement('div');
		date_apply_dropdown.className = "dropdown";

		var date_apply_anchor = document.createElement('a');
		date_apply_anchor.setAttribute('data-toggle','dropdown');
		date_apply_anchor.setAttribute('role','button');
		date_apply_anchor.setAttribute('aria-expanded',false);
		date_apply_anchor.setAttribute('aria-controls','collapseUpload')

		var date_apply_btn_label = document.createElement('label');
		date_apply_btn_label.className ="upload_tool text-light";
		var date_apply_icon = document.createElement('i');
		date_apply_icon.className = "fas fa-arrow-alt-circle-right";

		date_apply_btn_label.appendChild(date_apply_icon);


		date_apply_anchor.appendChild(date_apply_btn_label);
		date_apply_dropdown.appendChild(date_apply_anchor);

		var date_apply_dropdown_menu = document.createElement('div');
		date_apply_dropdown_menu.className = "dropdown-menu text-light";
		date_apply_dropdown_menu.style["background-color"] = "#454d54";
		date_apply_dropdown_menu.style.width = "auto";
		date_apply_dropdown_menu.setAttribute('aria-labelledby','dropdownMenuButton');

		var date_apply_dropdown_menu_inner = document.createElement('div');
		date_apply_dropdown_menu_inner.className = "container-fluid";

		var date_apply_all_btn_row = document.createElement('div');
		date_apply_all_btn_row.className = "row upload_tool justify-content-center";

		this.date_apply_all_btn = document.createElement("a");
		this.date_apply_all_btn.innerHTML = "<h6>Todo</h6>";

		date_apply_all_btn_row.appendChild(this.date_apply_all_btn);

		var date_apply_selected_btn_row = document.createElement('div');
		date_apply_selected_btn_row.className = "row upload_tool justify-content-center";

		this.date_apply_selected_btn = document.createElement("a");
		this.date_apply_selected_btn.innerHTML = "<h6>Selección</h6>";
		date_apply_selected_btn_row.appendChild(this.date_apply_selected_btn);

		date_apply_dropdown_menu_inner.appendChild(date_apply_selected_btn_row);
		date_apply_dropdown_menu_inner.appendChild(date_apply_all_btn_row);

		date_apply_dropdown_menu.appendChild(date_apply_dropdown_menu_inner);
		date_apply_dropdown.appendChild(date_apply_dropdown_menu);

		var date_row = document.createElement('div');
		date_row.className = "row d-flex";

		date_row.appendChild(date_label);
		date_row.appendChild(this.date_input);
		date_row.appendChild(date_apply_dropdown)

		date_col.appendChild(date_row);




		var time_col = document.createElement('div');
		time_col.className = "col";
		var time_label = document.createElement('label');
		time_label.className = "upload_tool text-light";
		time_label.appendChild(document.createTextNode('Tiempo: '));
		time_label.htmlFor = "itemDate";

		this.time_input = document.createElement('input');
		this.time_input.className = "incorrect_pattern";
		this.time_input.style.width = "80px";
		this.time_input.type = "text";

		$(this.time_input).datetimepicker({
			format:'H:i:s',
			datepicker: false,
			closeOnDateSelect: true,
			validateOnBlur: false,
			onChangeDateTime: function(dp,$input){
		        var time_input = widget.validate_datetime($input.val(),'time');
		        if (time_input){
		          $($input).removeClass('incorrect_pattern');
		        } else {
		          $($input).addClass('incorrect_pattern');
		        }
		    }
		});

        this.time_input.placeholder = "hh:mm:ss";


		var time_apply_dropdown = document.createElement('div');
		time_apply_dropdown.className = "dropdown";

		var time_apply_anchor = document.createElement('a');
		time_apply_anchor.setAttribute('data-toggle','dropdown');
		time_apply_anchor.setAttribute('role','button');
		time_apply_anchor.setAttribute('aria-expanded',false);
		time_apply_anchor.setAttribute('aria-controls','collapseUpload')

		var time_apply_btn_label = document.createElement('label');
		time_apply_btn_label.className ="upload_tool text-light";
		var time_apply_icon = document.createElement('i');
		time_apply_icon.className = "fas fa-arrow-alt-circle-right";

		time_apply_btn_label.appendChild(time_apply_icon);


		time_apply_anchor.appendChild(time_apply_btn_label);
		time_apply_dropdown.appendChild(time_apply_anchor);

		var time_apply_dropdown_menu = document.createElement('div');
		time_apply_dropdown_menu.className = "dropdown-menu text-light";
		time_apply_dropdown_menu.style["background-color"] = "#454d54";
		time_apply_dropdown_menu.style.width = "auto";
		time_apply_dropdown_menu.setAttribute('aria-labelledby','dropdownMenuButton');

		var time_apply_dropdown_menu_inner = document.createElement('div');
		time_apply_dropdown_menu_inner.className = "container-fluid";

		var time_apply_all_btn_row = document.createElement('div');
		time_apply_all_btn_row.className = "row upload_tool justify-content-center";

		this.time_apply_all_btn = document.createElement("a");
		this.time_apply_all_btn.innerHTML = "<h6>Todo</h6>";

		time_apply_all_btn_row.appendChild(this.time_apply_all_btn);

		var time_apply_selected_btn_row = document.createElement('div');
		time_apply_selected_btn_row.className = "row upload_tool justify-content-center";

		this.time_apply_selected_btn = document.createElement("a");
		this.time_apply_selected_btn.innerHTML = "<h6>Selección</h6>";
		time_apply_selected_btn_row.appendChild(this.time_apply_selected_btn);

		time_apply_dropdown_menu_inner.appendChild(time_apply_selected_btn_row);
		time_apply_dropdown_menu_inner.appendChild(time_apply_all_btn_row);

		time_apply_dropdown_menu.appendChild(time_apply_dropdown_menu_inner);
		time_apply_dropdown.appendChild(time_apply_dropdown_menu);

		var time_row = document.createElement('div');
		time_row.className = "row d-flex";

		time_row.appendChild(time_label);
		time_row.appendChild(this.time_input);
		time_row.appendChild(time_apply_dropdown)

		time_col.appendChild(time_row);


		var metadata_date_col = document.createElement('div');
		metadata_date_col.className = "col";
		metadata_date_col.align = "center";

		var metadata_date_dropdown = document.createElement('div');
		metadata_date_dropdown.className = "dropdown";

		var metadata_date_anchor = document.createElement('a');
		metadata_date_anchor.setAttribute('data-toggle','dropdown');
		metadata_date_anchor.setAttribute('role','button');
		metadata_date_anchor.setAttribute('aria-expanded',false);
		metadata_date_anchor.setAttribute('aria-controls','collapseUpload')

		var metadata_date_btn_label = document.createElement('label');
		metadata_date_btn_label.className ="upload_tool text-light";
		var metadata_date_label = document.createTextNode('Restaurar ');
		var metadata_date_icon = document.createElement('i');

		metadata_date_icon.className = "fas fa-cog";
		metadata_date_btn_label.appendChild(metadata_date_label);
		metadata_date_btn_label.appendChild(metadata_date_icon);


		metadata_date_anchor.appendChild(metadata_date_btn_label);
		metadata_date_dropdown.appendChild(metadata_date_anchor);

		var metadata_date_dropdown_menu = document.createElement('div');
		metadata_date_dropdown_menu.className = "dropdown-menu text-light";
		metadata_date_dropdown_menu.style["background-color"] = "#454d54";
		metadata_date_dropdown_menu.style.width = "auto";
		metadata_date_dropdown_menu.setAttribute('aria-labelledby','dropdownMenuButton');

		var metadata_date_dropdown_menu_inner = document.createElement('div');
		metadata_date_dropdown_menu_inner.className = "container-fluid";

		var metadata_date_all_btn_row = document.createElement('div');
		metadata_date_all_btn_row.className = "row upload_tool justify-content-center";

		this.metadata_date_all_btn = document.createElement("a");
		this.metadata_date_all_btn.innerHTML = "<h6>Todo</h6>";

		metadata_date_all_btn_row.appendChild(this.metadata_date_all_btn);

		var metadata_date_selected_btn_row = document.createElement('div');
		metadata_date_selected_btn_row.className = "row upload_tool justify-content-center";

		this.metadata_date_selected_btn = document.createElement("a");
		this.metadata_date_selected_btn.innerHTML = "<h6>Selección</h6>";
		metadata_date_selected_btn_row.appendChild(this.metadata_date_selected_btn);

		metadata_date_dropdown_menu_inner.appendChild(metadata_date_selected_btn_row);
		metadata_date_dropdown_menu_inner.appendChild(metadata_date_all_btn_row);

		metadata_date_dropdown_menu.appendChild(metadata_date_dropdown_menu_inner);
		metadata_date_dropdown.appendChild(metadata_date_dropdown_menu);

		metadata_date_col.appendChild(metadata_date_dropdown);


		row2.appendChild(date_col);
		row2.appendChild(time_col);
		row2.appendChild(date_pattern_col);
		row2.appendChild(metadata_date_col);



		toolbar_container.appendChild(row);
		toolbar_container.appendChild(row2);

		this.top_toolbar.appendChild(toolbar_container);


	    this.date_input.addEventListener('input',function(e){
	        var date_input = widget.validate_datetime(this.value);
	        if (date_input){
	          $(this).removeClass('incorrect_pattern');
	        } else {
	          $(this).addClass('incorrect_pattern');
	        }
	      });

	    this.time_input.addEventListener('input',function(e){
	        var time_input = widget.validate_datetime(this.value,'time');
	        if (time_input){
	          $(this).removeClass('incorrect_pattern');
	        } else {
	          $(this).addClass('incorrect_pattern');
	        }
	      });

	    this.metadata_date_all_btn.addEventListener('click',function(e){
	    	var fixable = widget.files.filter(widget.is_fixable);

	    	for (var i=0;i<fixable.length;i++){
	    		if (fixable[i].media_info){
	    			var datetime_original = fixable[i].media_info.DateTimeOriginalParsed;

	    			if (typeof(datetime_original) !== 'undefined'){
	    				var datetime_arr = datetime_original.split(" ");
	    				fixable[i].captured_on_date = datetime_arr[0];
	    				fixable[i].captured_on_time = datetime_arr[1];

	    			} else {
	    				fixable[i].captured_on_date = null;
	    				fixable[i].captured_on_time = null;
	    			}

	    		}
	    	}

	    	widget.render_by_name(['files']);

		});

	    this.metadata_date_selected_btn.addEventListener('click',function(e){
	    	var id_arr = widget.get_checked_ids();

	    	for (var i=0;i<id_arr.length;i++){
	    		var file = widget.get_file_by_id(id_arr[i]);
	    		if (file){
		    		if (file.media_info){
		    			var datetime_original = file.media_info.DateTimeOriginalParsed;
						var dinput = document.getElementById("date_input_file_"+file.file_id);
						var tinput = document.getElementById("time_input_file_"+file.file_id);
							
		    			if (typeof(datetime_original) !== 'undefined'){
		    				var datetime_arr = datetime_original.split(" ");
		    				file.captured_on_date = datetime_arr[0];
		    				file.captured_on_time = datetime_arr[1];
		    				dinput.value = datetime_arr[0];
		    				tinput.value = datetime_arr[1];
		    			} else {
		    				file.captured_on_date = null;
		    				file.captured_on_time = null;
		    				dinput.value = "";
		    				tinput.value = "";
		    			}

		    			widget.toggle_status(file.file_id);

		    		}	
	    		}

	    	}


		});

	    this.upload_all_btn.addEventListener('click',function(e){
	    	widget.upload_multiple(widget.is_uploadable);
		});

	    this.upload_selected_btn.addEventListener('click',function(e){
	        var id_arr = widget.get_checked_ids();

	    	widget.upload_multiple(function(f){return widget.is_uploadable(f) && id_arr.includes(f.file_id); });
		});

		this.remove_selected_btn.addEventListener('click',function(e){
			widget.remove_multiple(widget.get_checked_ids());
			widget.render_by_name(['files']);
		});

		this.remove_all_btn.addEventListener('click',function(e){
			widget.remove_all();

			widget.render_by_name(['files']);
		});

		this.date_pattern_apply_selected_btn.addEventListener('click',function(e){
			var parser_map = widget.validate_parser_map(widget.date_pattern_input.value);
			if (parser_map){
				var check_boxes = widget.file_list.querySelectorAll('input[type=checkbox]:checked');

				for (var i=0;i<check_boxes.length;i++){
					if (check_boxes[i].file_id != "all"){
						var file = widget.get_file_by_id(check_boxes[i].file_id);
						if (file){
							var dinput = document.getElementById("date_input_file_"+check_boxes[i].file_id);
							var tinput = document.getElementById("time_input_file_"+check_boxes[i].file_id);
							var datetime_obj = widget.parse_datetime(file.name,parser_map);

							var valid_date = widget.validate_datetime(datetime_obj.date);
							var valid_time = widget.validate_datetime(datetime_obj.time,'time');

							if (valid_date){
								file.captured_on_date = valid_date;
								dinput.value = valid_date;
							}

							if (valid_time){
								file.captured_on_time = valid_time;
								tinput.value = valid_time;							
							}

							widget.toggle_status(check_boxes[i].file_id);
						}
					}
				}
			}
		});

		this.date_pattern_apply_all_btn.addEventListener('click',function(e){
			var parser_map = widget.validate_parser_map(widget.date_pattern_input.value);
			if (parser_map){
				var files = widget.files.filter(widget.is_fixable);
				for (var i=0;i<files.length;i++){
					var datetime_obj = widget.parse_datetime(file.name,parser_map);
					var valid_date = widget.validate_datetime(datetime_obj.date);
					var valid_time = widget.validate_datetime(datetime_obj.time,'time');
					
					if (valid_date){
						file.captured_on_date = valid_date;
					}

					if (valid_time){
						file.captured_on_time = valid_time;
					}
				}

				widget.render_by_name(['files']);

			}
		});

		this.time_apply_all_btn.addEventListener('click',function(e){
			var valid_time = widget.validate_datetime(widget.time_input.value,'time');
			if (valid_time){
				var files = widget.files.filter(widget.is_fixable);
				for (var i=0;i<files.length;i++){
					files[i].captured_on_time = valid_time;
				}
				widget.render_by_name(['files']);
			}
		});

		this.time_apply_selected_btn.addEventListener('click',function(e){
			var valid_time = widget.validate_datetime(widget.time_input.value,'time');
			if (valid_time){
				var check_boxes = widget.file_list.querySelectorAll('input[type=checkbox]:checked');
				for (var i=0;i<check_boxes.length;i++){
					if (check_boxes[i].file_id != "all"){
						var file = widget.get_file_by_id(check_boxes[i].file_id);
						if (file){
							file.captured_on_time = valid_time;
							var dinput = document.getElementById("time_input_file_"+check_boxes[i].file_id);
							dinput.value = valid_time;
							widget.toggle_status(check_boxes[i].file_id);
						}
					}
				}
			}
		});

		this.date_apply_all_btn.addEventListener('click',function(e){
			var valid_date = widget.validate_datetime(widget.date_input.value);
			if (valid_date){
				var files = widget.files.filter(widget.is_fixable);
				for (var i=0;i<files.length;i++){
					files[i].captured_on_date = valid_date;
				}
				widget.render_by_name(['files']);
			}
		});

		this.date_apply_selected_btn.addEventListener('click',function(e){
			var valid_date = widget.validate_datetime(widget.date_input.value);
			if (valid_date){
				var check_boxes = widget.file_list.querySelectorAll('input[type=checkbox]:checked');
				for (var i=0;i<check_boxes.length;i++){
					if (check_boxes[i].file_id != "all"){
						var file = widget.get_file_by_id(check_boxes[i].file_id);
						if (file){
							file.captured_on_date = valid_date;
							var dinput = document.getElementById("date_input_file_"+check_boxes[i].file_id);
							dinput.value = valid_date;
							widget.toggle_status(check_boxes[i].file_id);
						}
					}
				}
			}
		});

		this.file_picker.addEventListener('change',function(e){
			function finalize_callback() {
				widget.render_by_name(['files','errors'])
			}

			widget.add_file_multiple(this.files,finalize_callback);
		});

		this.date_pattern_input.addEventListener('input',function(e){
			var parser_map = widget.validate_parser_map(this.value);
			if (parser_map){
				$(this).removeClass('incorrect_pattern');
			} else {
				$(this).addClass('incorrect_pattern');
			}
		});

		this.parent.appendChild(this.top_toolbar);
	}
	build_body() {
		if (this.body){
			$(this.body).remove();
		}
		this.body = document.createElement('div');
		this.body.className = "row justify-content-between w-100";

		this.body.style["padding-top"] = "10px";
		this.body.style["padding-bottom"] = "10px";

		this.body.style["padding-left"] = "20px";
		this.body.style["padding-right"] = "20px";

		this.build_files_section();
		this.build_results_section();
		this.parent.appendChild(this.body);
	}
	build_files_section() {
		if (this.files_section){
			$(this.files_section).remove();
		}
		var section_col = document.createElement('div');
		section_col.className = "col-8 justify-content-center w-100";

		this.files_section = document.createElement('div');
		this.files_section.className = "container-fluid justify-content-center p-2";

		this.file_list_container = document.createElement('div');
		this.file_list_container.className = "row justify-content-center container-fluid";
		this.file_list_container.style.display = "none";

		this.build_file_list();

		section_col.appendChild(this.progress_container);
		section_col.appendChild(this.files_section);
		this.body.appendChild(section_col);
	}
	build_results_section() {
		if (this.results_section){
			$(this.results_section).remove();
		}

		this.results_section = document.createElement('div');
		this.results_section.className = "col";

		var header = document.createElement('div');
		header.className = "row";
		this.results_header_tabs = document.createElement('ul');
		this.results_header_tabs.className = "nav w-100 nav-tabs upload_tabs";

		var error_tab = document.createElement('li');
		error_tab.className = "nav-item";
		this.error_link = document.createElement('a');
		this.error_link.className = "nav-link active";
		this.error_link.href = "#";
		this.error_link.innerHTML = "Errores (0)";
		error_tab.appendChild(this.error_link);


		var duplicate_tab = document.createElement('li');
		duplicate_tab.className = "nav-item";
		this.duplicate_link = document.createElement('a');
		this.duplicate_link.className = "nav-link";
		this.duplicate_link.href = "#";
		this.duplicate_link.innerHTML = "Duplicados (0)";
		duplicate_tab.appendChild(this.duplicate_link);


		var upload_tab = document.createElement('li');
		upload_tab.className = "nav-item";
		this.upload_link = document.createElement('a');
		this.upload_link.className = "nav-link";
		this.upload_link.href = "#";
		this.upload_link.innerHTML = "Subidos (0)";
		upload_tab.appendChild(this.upload_link);


		this.results_header_tabs.appendChild(error_tab);
		this.results_header_tabs.appendChild(duplicate_tab);
		this.results_header_tabs.appendChild(upload_tab);

		header.appendChild(this.results_header_tabs);

		this.error_container = document.createElement('div');
		this.error_list_container = document.createElement('div');
		this.error_list_container.className = "row container-fluid";
		this.error_list_container.style.display = "none";

		this.duplicate_container = document.createElement('div');
		this.duplicate_container.style.display = "none";
		this.duplicate_list_container = document.createElement('div');
		this.duplicate_list_container.className = "row container-fluid";
		this.duplicate_list_container.style.display = "none";

		this.upload_container = document.createElement('div');
		this.upload_container.style.display = "none";
		this.upload_list_container = document.createElement('div');
		this.upload_list_container.className = "row container-fluid";
		this.upload_list_container.style.display = "none";

		this.build_error_list();
		this.build_duplicate_list();
		this.build_upload_list();

		this.current_results_tab = this.error_container;

		var widget = this;

		this.error_link.addEventListener('click',function(e){
			if (widget.current_results_tab != widget.error_container){
				$( widget.results_header_tabs ).find( '.active' ).removeClass( 'active' );
				widget.current_results_tab.style.display = "none";
				widget.current_results_tab = widget.error_container;
				widget.current_results_tab.style.display = "block";
				$(this).addClass('active');
			}
		});

		this.duplicate_link.addEventListener('click',function(e){
			if (widget.current_results_tab != widget.duplicate_container){
				$( widget.results_header_tabs ).find( '.active' ).removeClass( 'active' );
				widget.current_results_tab.style.display = "none";
				widget.current_results_tab = widget.duplicate_container;
				widget.current_results_tab.style.display = "block";
				$(this).addClass('active');
			}
		});

		this.upload_link.addEventListener('click',function(e){
			if (widget.current_results_tab != widget.upload_container){
				$( widget.results_header_tabs ).find( '.active' ).removeClass( 'active' );
				widget.current_results_tab.style.display = "none";
				widget.current_results_tab = widget.upload_container;
				widget.current_results_tab.style.display = "block";
				$(this).addClass('active');
			}
		});

		this.error_container.appendChild(this.error_list_container);
		this.error_container.appendChild(this.blank_error_list);
		this.duplicate_container.appendChild(this.duplicate_list_container);
		this.duplicate_container.appendChild(this.blank_duplicate_list);
		this.upload_container.appendChild(this.upload_list_container);
		this.upload_container.appendChild(this.blank_upload_list);

		this.results_section.appendChild(header);
		this.results_section.appendChild(this.error_container);
		this.results_section.appendChild(this.duplicate_container);
		this.results_section.appendChild(this.upload_container);

		this.body.appendChild(this.results_section);
	}
	build_file_list(){
		this.file_list_table = document.createElement('div');
		this.file_list_table.className = "justify-content-center w-100";

		this.blank_file_list = document.createElement('div');
		this.blank_file_list.className = "row justify-content-center blank_item_list w-100";
		this.blank_file_list.height = "600px";


		var file_picker_col = document.createElement('div');
		var file_btn = document.createElement('label');
		file_btn.htmlFor = "alter_file_picker";
		file_btn.className ="upload_tool";


		var add_label = document.createTextNode("Agregar archivos ");
		var add_icon = document.createElement('i');
		add_icon.className = "fas fa-plus";
		file_btn.appendChild(add_label);
		file_btn.appendChild(add_icon);

		this.alter_file_picker = document.createElement('input');
		this.alter_file_picker.id = "alter_file_picker";
		this.alter_file_picker.type = "file";
		this.alter_file_picker.style.display = "none";
		this.alter_file_picker.setAttribute("multiple","");

		file_picker_col.appendChild(file_btn);
		file_picker_col.appendChild(this.alter_file_picker);

		this.blank_file_list.appendChild(file_picker_col);

		var paginator = document.createElement('div');
		paginator.className = "row justify-content-center w-100";
		paginator.align = "center";

		var prev_col = document.createElement('div');
		prev_col.className = "col p-3 text-center";
		this.prev_file_btn = document.createElement('button');
		this.prev_file_btn.className = "btn btn-primary";
		var prev_label = document.createTextNode("Anterior");
		this.prev_file_btn.appendChild(prev_label);
		prev_col.appendChild(this.prev_file_btn);

		var file_page_col = document.createElement('div');
		file_page_col.className = "col p-3 text-center";
		this.file_page_label = document.createElement('h6');
		file_page_col.appendChild(this.file_page_label);

		var next_col = document.createElement('div');
		next_col.className = "col p-3 text-center";
		this.next_file_btn = document.createElement('button');
		this.next_file_btn.className = "btn btn-primary";
		var next_label = document.createTextNode("Siguiente");
		this.next_file_btn.appendChild(next_label);
		next_col.appendChild(this.next_file_btn);

		paginator.appendChild(prev_col);
		paginator.appendChild(file_page_col);
		paginator.appendChild(next_col);

		var widget = this;

		this.next_file_btn.onclick = function(e){
			var page = widget.get_next_page("file_list");
			widget.render_file_list(page);
		}
		this.prev_file_btn.onclick = function(e){
			var page = widget.get_prev_page("file_list");
			widget.render_file_list(page);
		}

		this.alter_file_picker.addEventListener('change',function(e){
			function finalize_callback() {
				widget.render_by_name(['files','errors'])
			}

			widget.add_file_multiple(this.files,finalize_callback);
		});

		var header = document.createElement('div');
		header.className = 'row d-flex justify-content-between header_item w-100';
		header.align = "center";
		header.style["margin"] = "10px";

		var header_checkCol = document.createElement('div');
		header_checkCol.className = 'col-1  justify-content-center text-center item_col';

		var header_descrCol = document.createElement('div');
		header_descrCol.className = 'col-3  justify-content-center text-center item_col';

		var header_dateCol = document.createElement('div');
		header_dateCol.className = 'col-2  justify-content-center text-center item_col';

		var header_timeCol = document.createElement('div');
		header_timeCol.className = 'col-2  justify-content-center text-center item_col';

		var header_statusCol = document.createElement('div');
		header_statusCol.className = 'col-3  justify-content-center text-center item_col';

		var header_checkFile = document.createElement('input');
		header_checkFile.type = 'checkbox';
		header_checkFile.className = 'item_checkbox header_title';
		header_checkFile["file_id"] = "all";
		header_checkCol.appendChild(header_checkFile);

		var fileTitle = document.createElement('div');
    	fileTitle.textContent = 'Archivo';
    	fileTitle.className = 'ml-4 ellipsise text-light header_title';
    	header_descrCol.appendChild(fileTitle);

		var dateTitle = document.createElement('div');
    	dateTitle.textContent = 'Fecha';
    	dateTitle.className = 'ml-4 ellipsise text-light header_title';
    	header_dateCol.appendChild(dateTitle);

		var timeTitle = document.createElement('div');
    	timeTitle.textContent = 'Tiempo';
    	timeTitle.className = 'ml-4 ellipsise text-light header_title';
    	header_timeCol.appendChild(timeTitle);

	    var statusTitle = document.createElement('div');
	    statusTitle.className = 'ml-4 ellipsise text-light header_title';
	    statusTitle.textContent = "Estado";
	    header_statusCol.appendChild(statusTitle);

		header_checkFile.addEventListener('input',function(e){
			var check_boxes = widget.file_list.querySelectorAll('input[type=checkbox]');
			if (this.checked){
				for (var i=0;i<check_boxes.length;i++){
					check_boxes[i].checked = true;
				}
			} else {
				for (var i=0;i<check_boxes.length;i++){
					check_boxes[i].checked = false;
				}
			}

		});

	    header.appendChild(header_checkCol);
	    header.appendChild(header_descrCol);
	    header.appendChild(header_dateCol);
	    header.appendChild(header_timeCol);
	    header.appendChild(header_statusCol);

	    this.file_list = document.createElement('div');
	    this.file_list.className = "upload_list";
	    this.file_list.style["min-height"] = "450px";
	    this.file_list.style["max-height"] = "450px";

	    this.file_list_table.appendChild(header);
	    this.file_list_table.appendChild(this.file_list);

		this.file_list_container.appendChild(this.file_list_table);
		this.file_list_container.appendChild(paginator);

		this.files_section.appendChild(this.blank_file_list);
		this.files_section.appendChild(this.file_list_container);
	}
	build_error_list(){
		var paginator = document.createElement('div');
		paginator.className = "row justify-content-center w-100";
		paginator.align = "center";

		var prev_col = document.createElement('div');
		prev_col.className = "col p-3 text-center";
		this.prev_error_btn = document.createElement('button');
		this.prev_error_btn.className = "btn btn-primary";
		var prev_label = document.createTextNode("Anterior");
		this.prev_error_btn.appendChild(prev_label);
		prev_col.appendChild(this.prev_error_btn);

		var page_col = document.createElement('div');
		page_col.className = "col p-3 text-center";
		this.error_page_label = document.createElement('h6');
		page_col.appendChild(this.error_page_label);

		var next_col = document.createElement('div');
		next_col.className = "col p-3 text-center";
		this.next_error_btn = document.createElement('button');
		this.next_error_btn.className = "btn btn-primary";
		var next_label = document.createTextNode("Siguiente");
		this.next_error_btn.appendChild(next_label);
		next_col.appendChild(this.next_error_btn);

		paginator.appendChild(prev_col);
		paginator.appendChild(page_col);
		paginator.appendChild(next_col);

		var widget = this;

		this.next_error_btn.onclick = function(e){
			var page = widget.get_next_page("error_list");
			widget.render_error_list(page);
		}
		this.prev_error_btn.onclick = function(e){
			var page = widget.get_prev_page("error_list");
			widget.render_error_list(page);
		}

		this.error_list_table = document.createElement('div');
		this.error_list_table.className = "row justify-content-center w-100";

		var header = document.createElement('div');
		header.className = 'row d-flex justify-content-between header_item w-100';
		header.align = "center";
		header.style["margin"] = "10px";

		var header_descrCol = document.createElement('div');
		header_descrCol.className = 'col-6 text-center item_col';

		var header_statusCol = document.createElement('div');
		header_statusCol.className = 'col-6 text-center item_col';

		var fileTitle = document.createElement('div');
    	fileTitle.textContent = 'Archivo';
    	fileTitle.className = 'ml-4 ellipsise text-light header_title';
    	header_descrCol.appendChild(fileTitle);

	    var statusTitle = document.createElement('div');
	    statusTitle.className = 'ml-4 ellipsise text-light header_title';
	    statusTitle.textContent = "Descripción";
	    header_statusCol.appendChild(statusTitle);

	    header.appendChild(header_descrCol);
	    header.appendChild(header_statusCol);

	    this.error_list = document.createElement('div');
	    this.error_list.className = "upload_list";

	    this.error_list_table.appendChild(header);
	    this.error_list_table.appendChild(this.error_list);


		this.error_list_container.appendChild(this.error_list_table);
		this.error_list_container.appendChild(paginator);

		this.blank_error_list = document.createElement('div');
		this.blank_error_list.className = "row blank_item_list justify-content-center w-100";
		this.blank_error_list.style.border = "none";
		this.blank_error_list.height = "300px";

		var blank_message = document.createElement('a');
		blank_message.innerHTML = "No hay errores"
		this.blank_error_list.appendChild(blank_message);
	}
	build_duplicate_list(){
		var paginator = document.createElement('div');
		paginator.className = "row justify-content-center w-100";
		paginator.align = "center";

		var prev_col = document.createElement('div');
		prev_col.className = "col p-3 text-center";
		this.prev_duplicate_btn = document.createElement('button');
		this.prev_duplicate_btn.className = "btn btn-primary";
		var prev_label = document.createTextNode("Anterior");
		this.prev_duplicate_btn.appendChild(prev_label);
		prev_col.appendChild(this.prev_duplicate_btn);

		var page_col = document.createElement('div');
		page_col.className = "col p-3 text-center";
		this.duplicate_page_label = document.createElement('h6');
		page_col.appendChild(this.duplicate_page_label);

		var next_col = document.createElement('div');
		next_col.className = "col p-3 text-center";
		this.next_duplicate_btn = document.createElement('button');
		this.next_duplicate_btn.className = "btn btn-primary";
		var next_label = document.createTextNode("Siguiente");
		this.next_duplicate_btn.appendChild(next_label);
		next_col.appendChild(this.next_duplicate_btn);

		paginator.appendChild(prev_col);
		paginator.appendChild(page_col);
		paginator.appendChild(next_col);

		var widget = this;

		this.next_duplicate_btn.onclick = function(e){
			var page = widget.get_next_page("duplicate_list");
			widget.render_duplicate_list(page);
		}
		this.prev_duplicate_btn.onclick = function(e){
			var page = widget.get_prev_page("duplicate_list");
			widget.render_duplicate_list(page);
		}

		this.duplicate_list_table = document.createElement('div');
		this.duplicate_list_table.className = "row justify-content-center w-100";

		var header = document.createElement('div');
		header.className = 'row d-flex justify-content-between header_item w-100';
		header.align = "center";
		header.style["margin"] = "10px";
		header.style["padding-right"] = "0px !important";

		var header_descrCol = document.createElement('div');
		header_descrCol.className = 'col-5 text-center item_col';

		var header_statusCol = document.createElement('div');
		header_statusCol.className = 'col-5 text-center item_col';

		var fileTitle = document.createElement('div');
    	fileTitle.textContent = 'Artículo';
    	fileTitle.className = 'ml-4 ellipsise text-light header_title';
    	header_descrCol.appendChild(fileTitle);

	    var statusTitle = document.createElement('div');
	    statusTitle.className = 'ml-4 ellipsise text-light header_title';
	    statusTitle.textContent = "Link";
	    header_statusCol.appendChild(statusTitle);

	    header.appendChild(header_descrCol);
	    header.appendChild(header_statusCol);

	    this.duplicate_list = document.createElement('div');
	    this.duplicate_list.className = "upload_list";

	    this.duplicate_list_table.appendChild(header);
	    this.duplicate_list_table.appendChild(this.duplicate_list);

		this.duplicate_list_container.appendChild(this.duplicate_list_table);
		this.duplicate_list_container.appendChild(paginator);

		this.blank_duplicate_list = document.createElement('div');
		this.blank_duplicate_list.className = "row blank_item_list justify-content-center w-100";
		this.blank_duplicate_list.style.border = "none";
		this.blank_duplicate_list.height = "300px";

		var blank_message = document.createElement('a');
		blank_message.innerHTML = "No hay duplicados"
		this.blank_duplicate_list.appendChild(blank_message);
	}
	build_upload_list(){
		var paginator = document.createElement('div');
		paginator.className = "row justify-content-center w-100";
		paginator.align = "center";

		var prev_col = document.createElement('div');
		prev_col.className = "col p-3 text-center";
		this.prev_upload_btn = document.createElement('button');
		this.prev_upload_btn.className = "btn btn-primary";
		var prev_label = document.createTextNode("Aanterior");
		this.prev_upload_btn.appendChild(prev_label);
		prev_col.appendChild(this.prev_upload_btn);

		var page_col = document.createElement('div');
		page_col.className = "col p-3 text-center";
		this.upload_page_label = document.createElement('h6');
		page_col.appendChild(this.upload_page_label);

		var next_col = document.createElement('div');
		next_col.className = "col p-3 text-center";
		this.next_upload_btn = document.createElement('button');
		this.next_upload_btn.className = "btn btn-primary";
		var next_label = document.createTextNode("Siguiente");
		this.next_upload_btn.appendChild(next_label);
		next_col.appendChild(this.next_upload_btn);

		paginator.appendChild(prev_col);
		paginator.appendChild(page_col);
		paginator.appendChild(next_col);

		var widget = this;

		this.next_upload_btn.onclick = function(e){
			var page = widget.get_next_page("upload_list");
			widget.render_upload_list(page);
		}
		this.prev_upload_btn.onclick = function(e){
			var page = widget.get_prev_page("upload_list");
			widget.render_upload_list(page);
		}

		this.upload_list_table = document.createElement('div');
		this.upload_list_table.className = "row justify-content-center w-100";

		var header = document.createElement('div');
		header.className = 'row d-flex justify-content-between header_item w-100';
		header.align = "center";
		header.style["margin"] = "10px";

		var header_descrCol = document.createElement('div');
		header_descrCol.className = 'col-5 text-center item_col';

		var header_statusCol = document.createElement('div');
		header_statusCol.className = 'col-5 text-center item_col';

		var fileTitle = document.createElement('div');
    	fileTitle.textContent = 'Artículo';
    	fileTitle.className = 'ml-4 ellipsise text-light header_title';
    	header_descrCol.appendChild(fileTitle);

	    var statusTitle = document.createElement('div');
	    statusTitle.className = 'ml-4 ellipsise text-light header_title';
	    statusTitle.textContent = "Link";
	    header_statusCol.appendChild(statusTitle);

	    header.appendChild(header_descrCol);
	    header.appendChild(header_statusCol);

	    this.upload_list = document.createElement('div');
	    this.upload_list.className = "upload_list";

		this.upload_list_table.appendChild(header);
	    this.upload_list_table.appendChild(this.upload_list);

		this.upload_list_container.appendChild(this.upload_list_table);
		this.upload_list_container.appendChild(paginator);

		this.blank_upload_list = document.createElement('div');
		this.blank_upload_list.className = "row blank_item_list justify-content-center w-100";
		this.blank_upload_list.style.border = "none";
		this.blank_upload_list.height = "300px";

		var blank_message = document.createElement('a');
		blank_message.innerHTML = "No se ha subido ningún archivo nuevo"
		this.blank_upload_list.appendChild(blank_message);
	}
	get_file_page(page, per_page, filter_function,sort_function=this.compare_names) {
		var page = page || 1;
		if (page <= 0){
			page = 1;
		}
		var per_page = per_page || 10;

		if (filter_function){
			var filteredItems = this.files.filter(filter_function);
		} else {
			var filteredItems = this.files;
		}
		if (sort_function){
			filteredItems.sort(sort_function);
		}
		

		var total_pages = Math.ceil(filteredItems.length / per_page);

		if (filteredItems.length <= per_page && filteredItems.length > 0){
			total_pages = 1;
		}

		page = Math.min(page,total_pages);

		var offset = (page - 1) * per_page;
		var paginatedItems = filteredItems.slice(offset).slice(0, per_page);

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
	render_file_list(page) {
		while (this.file_list.firstChild) {
			this.file_list.removeChild(this.file_list.firstChild);
		}
		if (page.data.length > 0){
			this.blank_file_list.style.display = "none";
			this.file_list_container.style.display = "flex";
			this.total_file_pages = page.total_pages;
			$(this.file_page_label).html(page.page+"/"+page.total_pages);
			var widget = this;

			for (var i=0;i<page.data.length;i++){
				var row = document.createElement('div');
				row.className = 'row d-flex justify-content-between list_item w-100';
				row.align = "center";
				row.style["margin"] = "10px";

				var checkCol = document.createElement('div');
				checkCol.className = 'col-1 justify-content-center text-center item_col';

				var descrCol = document.createElement('div');
				descrCol.className = 'col-3 justify-content-center  text-center item_col';

				var dateCol = document.createElement('div');
				dateCol.className = 'col-2 justify-content-center  text-center item_col w-100';
				dateCol.align = "center";

				var timeCol = document.createElement('div');
				timeCol.className = 'col-2 justify-content-center  text-center item_col w-100';
				timeCol.align = "center";

				var statusCol = document.createElement('div');
				statusCol.className = 'col-3 justify-content-center  text-center item_col';


				var checkFile = document.createElement('input');
				checkFile.type = 'checkbox';
				checkFile.className = 'item_checkbox file_title';
				checkFile["file_id"] = page.data[i].file_id;

				checkCol.appendChild(checkFile);

		        var fileName = document.createElement('div');
		        fileName.className = "text-muted ml-4 ellipsise file_title";
		        fileName.textContent = page.data[i].name;
		        fileName.title = page.data[i].name;


		        descrCol.appendChild(fileName);

		        var dateInput = document.createElement('input');
		        dateInput.type = "text";
		        dateInput.style["text-align"]="center";
		        dateInput.style.width = "115px";
		        dateInput.className = "incorrect_pattern ml-4 file_title";
		        dateInput.id = "date_input_file_"+page.data[i]["file_id"];
          		dateInput.placeholder = "YYYY-MM-DD";
          		dateInput["file_id"] = page.data[i]["file_id"];

          		var valid_date = false;

		        $(dateInput).datetimepicker({
					format:'Y-m-d',
					file_id: page.data[i]["file_id"],
					validateOnBlur: false,
					timepicker: false,
					onChangeDateTime: function(dp,$input){
				        var date_input = widget.validate_datetime($input.val());

				        if (date_input){
				          var file = widget.get_file_by_id($input[0].file_id);
				          file.captured_on_date = date_input;
				        }

				        widget.toggle_status($input[0].file_id);
				    }
				});

		        if (page.data[i].captured_on_date){
		        	dateInput.value = page.data[i].captured_on_date;
		        	$(dateInput).removeClass('incorrect_pattern');
		        }

		        dateCol.appendChild(dateInput);

		        var timeInput = document.createElement('input');
		        timeInput.type = "text";
		        timeInput.style["text-align"]="center";
		        timeInput.style.width = "110px";
		        timeInput.className = "incorrect_pattern ml-4 file_title";
		        timeInput.id = "time_input_file_"+page.data[i]["file_id"];
          		timeInput.placeholder = "hh:mm:ss";
          		timeInput["file_id"] = page.data[i]["file_id"];

          		var valid_time = false;

		        $(timeInput).datetimepicker({
					format:'H:i:s',
					datepicker: false,
					file_id: page.data[i]["file_id"],
					validateOnBlur: false,
					onChangeDateTime: function(dp,$input){
				        var time_input = widget.validate_datetime($input.val(),'time');
				        if (time_input){
				          var file = widget.get_file_by_id($input[0].file_id);
				          file.captured_on_time = time_input;
				        }
				        widget.toggle_status($input[0].file_id);
				    }
				});

		        if (page.data[i].captured_on_time){
		        	timeInput.value = page.data[i].captured_on_time;
		        	$(timeInput).removeClass('incorrect_pattern');
		        }

		        timeCol.appendChild(timeInput);

				var status_btn = document.createElement('div');
				status_btn.className ="col text-muted ml-4 ellipsise file_title";
				status_btn.id = "status_btn_"+page.data[i]["file_id"];
				status_btn["file_id"] = page.data[i].file_id;
				status_btn.style.display = "none";
				status_btn.style.cursor = "pointer";

				var status_label = document.createTextNode("Listo ");
				var status_icon = document.createElement('i');
				status_icon.className = "fas fa-upload";
				

				status_btn.appendChild(status_label);
				status_btn.appendChild(status_icon);

				var status_div =  document.createElement('div');
				status_div.className = "row";

		        var statusText = document.createElement('div');
		        statusText.className = "col text-muted ml-4 ellipsise file_title";
		        statusText.id = "status_text_"+page.data[i]["file_id"];

		        var status = "";

		        if (!page.data[i].captured_on_time && !page.data[i].captured_on_date){
		        	status = "Sin momento";
		        } else if (!page.data[i].captured_on_time) {
		        	status = "Sin tiempo";
		        } else if (!page.data[i].captured_on_date) {
		        	status = "Sin fecha";
		        } else {
		        	status = "Listo";
		        }

		        statusText.textContent = status;

		        if (status == "Listo"){
		        	statusText.style.display = "none";
					status_btn.style.display = "inline-block";
		        	$(timeInput).removeClass('incorrect_pattern');
		        } else {
		        	statusText.style.display = "inline-block";
					status_btn.style.display = "none";     	
		        }
		        
		        status_div.appendChild(statusText);
		        status_div.appendChild(status_btn);
		        statusCol.appendChild(status_div);


			    $(dateInput).datetimepicker("option", "onSelect", function(){
			        var date_input = widget.validate_datetime(this.value);

			        if (date_input){
			          var file = widget.get_file_by_id(this.file_id);
			          file.captured_on_date = date_input;
			        }

			        widget.toggle_status($input[0].file_id);
			    });

			      dateInput.addEventListener('input',function(e){
			        var date_input = widget.validate_datetime(this.value);
			        var file = widget.get_file_by_id(this.file_id);

			        if (date_input){
			          file.captured_on_date = date_input;
			        } else {
			          file.captured_on_date = null;
			        }

			        widget.toggle_status(this.file_id);

			      });

			    $(timeInput).datetimepicker("option", "onSelect", function(){
			        var time_input = widget.validate_datetime(this.value,'time');

			        if (time_input){
			          var file = widget.get_file_by_id(this.file_id);
			          file.captured_on_time = time_input;
			        }

			        widget.toggle_status(this.file_id);
			    });

			      timeInput.addEventListener('input',function(e){
			        var time_input = widget.validate_datetime(this.value,'time');
			        var file = widget.get_file_by_id(this.file_id);

			        if (time_input){
			          file.captured_on_time = time_input;
			        } else {
			          file.captured_on_time = null;
			        }
			        widget.toggle_status(this.file_id);
			      });

			      status_btn.addEventListener('click',function(e){
			      		var file_id = this.file_id;
			      		widget.upload_multiple(function(f){return f.file_id == file_id});
			      });

		        row.appendChild(checkCol);
				row.appendChild(descrCol);
				row.appendChild(dateCol);
				row.appendChild(timeCol);
				row.appendChild(statusCol);
				this.file_list.appendChild(row)
				
			}




		} else {
			this.file_list_container.style.display = "none";
			this.blank_file_list.style.display = "flex";
		}
	}
	render_error_list(page) {
		while (this.error_list.firstChild) {
			this.error_list.removeChild(this.error_list.firstChild);
		}

		this.error_link.innerHTML = "Errores ("+page.total+")";

		if (page.data.length > 0){
			this.blank_error_list.style.display = "none";
			this.error_list_container.style.display = "flex";
			this.total_error_pages = page.total_pages;
			$(this.error_page_label).html(page.page+"/"+page.total_pages);
			var widget = this;
			
			for (var i=0;i<page.data.length;i++){
				var row = document.createElement('div');
				row.className = 'row d-flex justify-content-between error_item w-100';
				row.align = "center";
				row.style["margin"] = "10px";

				var descrCol = document.createElement('div');
				descrCol.className = 'col-6 text-center item_col';

				var statusCol = document.createElement('div');
				statusCol.className = 'col-6 text-center item_col';

		        var fileName = document.createElement('div');
		        fileName.className = "text-muted ml-4 ellipsise";
		        fileName.textContent = page.data[i].name;
		        fileName.title = page.data[i].name;

		        descrCol.appendChild(fileName);

		        var statusText = document.createElement('div');
		        statusText.className = "text-muted ml-4 ellipsise";
		        statusText.id = "status_text_"+page.data[i]["file_id"];

		        var status = "";
		        if (!page.data[i].item_type){
		        	status = "Tipo incorrecto";
		        }
		        statusText.textContent = status;

		        statusCol.appendChild(statusText);

				row.appendChild(descrCol);
				row.appendChild(statusCol);

				this.error_list.appendChild(row);

			}

		} else {
			this.error_list_container.style.display = "none";
			this.blank_error_list.style.display = "flex";
		}
	}
	render_duplicate_list(page) {
		while (this.duplicate_list.firstChild) {
			this.duplicate_list.removeChild(this.duplicate_list.firstChild);
		}

		this.duplicate_link.innerHTML = "Duplicados ("+page.total+")";

		if (page.data.length > 0){
			this.blank_duplicate_list.style.display = "none";
			this.duplicate_list_container.style.display = "flex";
			this.total_duplicate_pages = page.total_pages;
			$(this.duplicate_page_label).html(page.page+"/"+page.total_pages);
			var widget = this;

			for (var i=0;i<page.data.length;i++){
				var row = document.createElement('div');
				row.className = 'row d-flex justify-content-between duplicate_item w-100';
				row.align = "center";
				row.style["margin"] = "10px";

				var descrCol = document.createElement('div');
				descrCol.className = 'col-5 justify-content-center text-center item_col';

				var statusCol = document.createElement('div');
				statusCol.className = 'col-5 text-center item_col';

		        var fileImage_div = document.createElement('div');
		        fileImage_div.className = "justify-content-center media";
		        var fileImage = document.createElement('img');
		        fileImage.className = "itemimage_tiny ml-4";
		        fileImage.setAttribute('src',page.data[i].upload_response.result.item.url);
		        fileImage_div.appendChild(fileImage);

		        descrCol.appendChild(fileImage_div);

		        var itemLink = document.createElement('a');
		        itemLink.className = "btn-link ml-4 ellipsise";
		        itemLink.setAttribute('href',page.data[i].upload_response.result.item.detail_url)
		        itemLink.setAttribute('target','_blank');
		        itemLink.innerHTML = "<h6>Artículo "+page.data[i].upload_response.result.item.pk+"</h6>";
		        
		        statusCol.appendChild(itemLink);

				row.appendChild(descrCol);
				row.appendChild(statusCol);

				this.duplicate_list.appendChild(row);

			}
		} else {
			
			this.duplicate_list_container.style.display = "none";
			this.blank_duplicate_list.style.display = "flex";
		}
	}
	render_upload_list(page) {
		while (this.upload_list.firstChild) {
			this.upload_list.removeChild(this.upload_list.firstChild);
		}

		this.upload_link.innerHTML = "Subidos ("+page.total+")";

		if (page.data.length > 0){
			this.blank_upload_list.style.display = "none";
			this.upload_list_container.style.display = "flex";
			this.total_upload_pages = page.total_pages;
			$(this.upload_page_label).html(page.page+"/"+page.total_pages);
			var widget = this;

			for (var i=0;i<page.data.length;i++){
				var row = document.createElement('div');
				row.className = 'row d-flex justify-content-between uploaded_item w-100';
				row.align = "center";
				row.style["margin"] = "10px";

				var descrCol = document.createElement('div');
				descrCol.className = 'col-5 text-center item_col';

				var statusCol = document.createElement('div');
				statusCol.className = 'col-5 text-center item_col';


		        var fileImage_div = document.createElement('div');
		        fileImage_div.className = "justify-content-center media";
		        var fileImage = document.createElement('img');
		        fileImage.className = "itemimage_tiny ml-4";
		        fileImage.setAttribute('src',page.data[i].upload_response.result.item.url);
		        fileImage_div.appendChild(fileImage);

		        descrCol.appendChild(fileImage_div);

		        var itemLink = document.createElement('a');
		        itemLink.className = "btn-link ml-4 ellipsise";
		        itemLink.setAttribute('href',page.data[i].upload_response.result.item.detail_url)
		        itemLink.setAttribute('target','_blank');
		        itemLink.innerHTML = "<h6>Artículo "+page.data[i].upload_response.result.item.pk+"</h6>";

		        statusCol.appendChild(itemLink);

				row.appendChild(descrCol);
				row.appendChild(statusCol);

				this.upload_list.appendChild(row);

			}
		} else {
			this.upload_list_container.style.display = "none";
			this.blank_upload_list.style.display = "flex";
		}
	}
	get_checked_ids(){
    	var check_boxes = this.file_list.querySelectorAll('input[type=checkbox]:checked');
		var id_arr = [];
		for (var i=0;i<check_boxes.length;i++){
			if (check_boxes[i].file_id != "all"){
				id_arr.push(check_boxes[i].file_id);
			}
		}

		return id_arr;
	}
	parse_datetime(fileName,parser_map){
	  var date_context = fileName.match(parser_map["regexp"]);
	  var date = "";
	  var time = "";

	  if (date_context){
	    if ("year" in parser_map){
		    date = date + date_context.toString().substring(parser_map["year"]["limits"][0],parser_map["year"]["limits"][1]);
		    if ("month" in parser_map){
			    date = date + "-" + date_context.toString().substring(parser_map["month"]["limits"][0],parser_map["month"]["limits"][1]);
			    if ("day" in parser_map){
			    	date = date + "-" + date_context.toString().substring(parser_map["day"]["limits"][0],parser_map["day"]["limits"][1]);
			    }
			    
		    }

	    }

	    if ("hour" in parser_map){
		    time = time + date_context.toString().substring(parser_map["hour"]["limits"][0],parser_map["hour"]["limits"][1]);
		    if ("minute" in parser_map){
			    time = time + ":" + date_context.toString().substring(parser_map["minute"]["limits"][0],parser_map["minute"]["limits"][1]);
			    if ("second" in parser_map){
			    	time = time + ":" + date_context.toString().substring(parser_map["second"]["limits"][0],parser_map["second"]["limits"][1]);
			    }
			    
		    }
	    }


	    return {"date":date,"time":time};
	  }

	  return {"date":"","time":""};
	}
	retrieve_media_info(file,callback) {
		if (file.type == 'image/jpeg'){
			var fr = new FileReader();
			var widget = this;
			fr.onloadend = function(){
				var exif = null;

				try {
					exif = EXIF.readFromBinaryFile(this.result);
				} catch(error) {
					exif = null;
				}
				

          		if (exif) {

          			file.media_info = exif;
          			var date_time_original = exif.DateTimeOriginal;

          			if (typeof(date_time_original) !== 'undefined'){
          				var date_time_arr = date_time_original.split(" ");
          				var date = date_time_arr[0].replace(/:/g,'-');
          				var time = date_time_arr[1]
          				var valid_date = widget.validate_datetime(date);
          				var valid_time = widget.validate_datetime(time,'time');

				        if (valid_date && valid_time){
				        	file.media_info["DateTimeOriginalParsed"] = valid_date+" "+valid_time;
				        	file.captured_on_date = valid_date;
				        	file.captured_on_time = valid_time;

				        }
          			}
          		}

				if (callback){
					callback(file);
				}
			}
			fr.readAsArrayBuffer(file);
		} else {
			if (callback){
				callback(file);
			}
		}
	}
	validate_parser_map(map_string){
	      var pattern_mask = "";
	      var pieces = [];
	      var date_parser_map = {};
	      var bad_date_map = false;
	      var date_regexp = null;

	      if (map_string.includes('<') && map_string.includes('>')){

	        for(var i=0; i<map_string.length;i++) {
	          if (map_string[i] == "<"){
	            pattern_mask = pattern_mask + map_string[i];
	            for (var j=i+1; j<map_string.length; j++){
	              pattern_mask = pattern_mask + map_string[j];
	              if (map_string[j] == ">"){
	                pieces.push([i+1,j]);
	                i = j;
	                break;
	              } else if (map_string[j] == "<") {
	                i = map_string.length;
	                break;
	              }
	            }
	          } else {
	            pattern_mask = pattern_mask + "_";
	          }
	        }

	        if (pieces.length > 0){
	          date_regexp = map_string.substring(pieces[0][0]-1,pieces[pieces.length-1][1]+1);
	          var cut_pattern = pattern_mask.substring(pieces[0][0]-1,pieces[pieces.length-1][1]+1).replace(/</g,"").replace(/>/g,"");

	          for (var p=0;p<pieces.length;p++){
	            var substr = map_string.substring(pieces[p][0],pieces[p][1]);
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
	              if ('year' in date_parser_map || ('hour' in date_parser_map && 'minute' in date_parser_map)){
		       	      if ('month' in date_parser_map && !('year' in date_parser_map)){
		              	bad_date_map = true;
		              }
		              if ('day' in date_parser_map && !('month' in date_parser_map)){
		              	bad_date_map = true;
		              }

		              if ('minute' in date_parser_map && !('hour' in date_parser_map)){
		              	bad_date_map = true;
		              }

		              if ('second' in date_parser_map && !('minute' in date_parser_map)){
		              	bad_date_map = true;
		              }

		              if (!bad_date_map){
		              	date_parser_map["regexp"] = date_regexp;
		              	return date_parser_map;
		              }
	              }
	          }
	        }
	      }

	      return false;
	}
	validate_datetime(dateString,type="date"){
	  if (dateString != ""){
	  	var formats = [];
	  	var aux_obj = "";
	  	switch(type){
	  		case "date": {
	  			var date_arr = dateString.split("-");
	  			var date_len = date_arr.length;

	  			switch (date_len){
		  				case 1:{
		  					aux_obj = dateString + "-01-01";
		  					break;
		  				}
		  				case 2:{
		  					aux_obj = dateString + "-01";
		  					break;
		  				}
		  				case 3:{
		  					aux_obj = dateString;
		  					break;
		  				}
		  				default:{
		  					break;
		  				}
	  			}

	  			formats = ["YYYY-MM-DD"]
	  			break;
	  		}
	  		case "time": {
	  			aux_obj = "2019-01-01 "+dateString;
	  			formats = ["YYYY-MM-DD HH:ss","YYYY-MM-DD HH:mm:ss"]
	  			break;
	  		}

	  		default: {
	  			aux_obj = dateString;
	  			formats = ["YYYY-MM-DD HH:ss","YYYY-MM-DD HH:mm:ss"]
	  			break;
	  		}
	  	}


		for (var i=0;i<formats.length;i++){
			if (moment(aux_obj,formats[i],true).isValid()){
				return dateString;
			}
		}
	  }

	  return false;
	}
	get_next_page(list_name){
		var page = null;
		switch(list_name){
			case "file_list":{
				page = this.get_file_page(this.file_page_number+1, this.per_page, this.is_fixable)
				this.file_page_number = page.page;
				this.total_file_pages = page.total_pages;
				break;
			}
			case "error_list":{
				page = this.get_file_page(this.error_page_number+1, this.per_page, this.has_errors)
				this.error_page_number = page.page;
				this.total_error_pages = page.total_pages;
				break;
			}
			case "duplicate_list":{
				page = this.get_file_page(this.duplicate_page_number+1, this.per_page, this.is_duplicate)
				this.duplicate_page_number = page.page;
				this.total_duplicate_pages = page.total_pages;
				break;
			}
			case "upload_list":{
				page = this.get_file_page(this.upload_page_number+1, this.per_page, this.is_uploaded)
				this.duplicate_page_number = page.page;
				this.total_upload_pages = page.total_pages;
				break;
			}
			default:{
				return null;
				break;
			}
		}

		return page;
	}
	get_prev_page(list_name){
		var page = null;
		switch(list_name){
			case "file_list":{
				page = this.get_file_page(this.file_page_number-1, this.per_page, this.is_fixable)
				this.file_page_number = page.page;
				this.total_file_pages = page.total_pages;
				break;
			}
			case "error_list":{
				page = this.get_file_page(this.error_page_number-1, this.per_page, this.has_errors)
				this.error_page_number = page.page;
				this.total_error_pages = page.total_pages;
				break;
			}
			case "duplicate_list":{
				page = this.get_file_page(this.duplicate_page_number-1, this.per_page, this.is_duplicate)
				this.duplicate_page_number = page.page;
				this.total_duplicate_pages = page.total_pages;
				break;
			}
			case "upload_list":{
				page = this.get_file_page(this.upload_page_number-1, this.per_page, this.is_uploaded)
				this.duplicate_page_number = page.page;
				this.total_upload_pages = page.total_pages;
				break;
			}
			default:{
				return null;
				break;
			}
		}

		return page;
	}
	generate_id() {
		var new_id = this.last_id + 1;
		this.last_id = this.last_id + 1;

		return new_id;
	}
	is_uploadable(file){
		if (file.item_type){
			if ((file.captured_on_date && file.captured_on_time) || file.force_upload){
				return true;
			}
		}
		return false;
	}
	is_uploading(file){
		if (file.upload_response){
			if (file.upload_response != "uploading"){
				return true;
			}
		}

		return false;
	}
	is_duplicate(file){
		if (file.upload_response){
			if (file.upload_response != "uploading"){
				if (file.upload_response.result_type == "duplicate"){
					return true;
				}
			}
		}
		return false;
	}
	is_uploaded(file){
		if (file.upload_response){
			if (file.upload_response != "uploading"){
				if (file.upload_response.result_type == "success"){
					return true;
				}
			}
		}
		return false;
	}
	is_fixable(file){
		if (file.item_type && !file.upload_response){
			return true;
		}
		return false;
	}
	is_force(file){
		if (file.force){
			return true;
		}
		return false;
	}
	has_media_info(file){
		if (file.media_info){
			return true;
		}

		return false;
	}
	has_errors(file){
		if (!file.item_type){
			return true;
		}
		return false;
	}
	compare_names(f1,f2){
		if (f1.name < f2.name){
			return -1;
		}
		if (f1.name > f2.name){
			return 1;
		}
		return 0;
	}
	get_item_type(file){
	  switch (file.type){
	    case 'image/jpeg':
	    case 'image/jpg':{
	      return "Foto de Camara Trampa (jpg)";
	    }
	    case 'image/png':{
	      return "Foto de Camara Trampa (png)";
	    }
	    default:{
	      return null;
	    }
	  }
	}
	upload_single(file,callback) {
	  var url = this.form.action;
	  var formData = new FormData($(this.form)[0]);
	  
	  formData.set('item_file', file);
	  formData.set('item_type',file.item_type);

	  if (file.captured_on_date){
	  	var date_arr = file.captured_on_date.split("-");
	  	var date_len = date_arr.length;
	  	switch (date_len){
	  		case 1:{
				formData.set('captured_on_year',date_arr[0]);
	  			break;
	  		}
	  		case 2:{
				formData.set('captured_on_year',date_arr[0]);
				formData.set('captured_on_month',date_arr[1]);
	  			break;
	  		}
	  		case 3:{
				formData.set('captured_on_year',date_arr[0]);
				formData.set('captured_on_month',date_arr[1]);
				formData.set('captured_on_day',date_arr[2]);
	  			break;
	  		}
	  	}
	  }
	  if (file.captured_on_time){
	  	var time_arr = file.captured_on_time.split(":");
	  	var time_len = time_arr.length;
	  	switch (time_len){
	  		case 2:{
				formData.set('captured_on_hour',time_arr[0]);
				formData.set('captured_on_minute',time_arr[1]);
	  			break;
	  		}
	  		case 3:{
				formData.set('captured_on_hour',time_arr[0]);
				formData.set('captured_on_minute',time_arr[1]);
				formData.set('captured_on_second',time_arr[2]);
	  			break;
	  		}
	  	}
	  }

	  $.ajax({
		  url: url,
		  data: formData,
		  processData: false,
		  contentType: false,
		  cache: false,
		  enctype: 'multipart/form-data',
		  type: 'POST',

		  success: function(data){
	  	  	  var response_obj = null;
			  try {
			    response_obj = JSON.parse(data.responseText);
			    file["upload_response"] = response_obj;
			  } catch (error) {
			  	file["upload_response"] = null;
			  }

			  if (callback){
			  	callback(response_obj);
			  }
	      },
	      error: function(data){
	  	  	  var response_obj = null;
			  try {
			    response_obj = JSON.parse(data.responseText);
			    file["upload_response"] = response_obj;
			  } catch (error) {
			  	file["upload_response"] = null;
			  }

			  if (callback){
			  	callback(response_obj);
			  }
	      }
	  });
	}
	render_by_name(name_arr){
		if (!name_arr){
			name_arr = ['files','errors','duplicates','uploads'];
		}
		if (name_arr.includes('files')){
			var file_page = this.get_file_page(this.file_page_number, this.per_page, this.is_fixable);
			this.render_file_list(file_page);
		}
		if (name_arr.includes('errors')){
			var error_page = this.get_file_page(this.error_page_number, this.per_page, this.has_errors);
			this.render_error_list(error_page);
		}
		if (name_arr.includes('duplicates')){
			var duplicate_page = this.get_file_page(this.duplicate_page_number, this.per_page, this.is_duplicate);
			this.render_duplicate_list(duplicate_page);
		}
		if (name_arr.includes('uploads')){
			var upload_page = this.get_file_page(this.upload_page_number, this.per_page, this.is_uploaded);
			this.render_upload_list(upload_page);
		}
	}
	progress_upload(count,total){
  		var percent = Math.round((count * 100) / total);
  		$(this.progress_bar)
    		.css('width', percent + '%')
    		.attr('aria-valuenow', percent);
  		$(this.progress_bar_label).html(percent + '%');
	}

	upload_multiple(filter_function,finalize_callback){
		var to_upload = this.files.filter(filter_function);

		for (var i=0;i<to_upload.length;i++){
			to_upload[i]["upload_response"] = "uploading";
		}

		this.render_by_name(['files']);

		var file_count = 0;
		var total_files = to_upload.length;

		var widget = this;

		function gather(response){
			file_count++;
			widget.render_by_name(['errors','duplicates','uploads']);
			widget.progress_upload(file_count,total_files);
			
			if (file_count >= total_files-1){
				setTimeout(function() {
					widget.progress_container.style.display = "none";
					widget.progress_upload(0,total_files);
				}, 2000);
			}
		}

		this.progress_container.style.display = "block";

		for (var i=0;i<to_upload.length;i++){
			this.upload_single(to_upload[i],gather);
		}
	}
	add_file(file,callback){
		file["captured_on_date"] = null;
		file["captured_on_time"] = null;
		file["item_type"] = this.get_item_type(file);
		file["media_info"] = null;
		file["veto_upload"] = false;
		file["force_upload"] = false;
		file["upload_response"] = null;
		file["file_id"] = this.generate_id();
		this.files.push(file);

		this.retrieve_media_info(this.files[this.files.length-1],callback);
	}
	add_file_multiple(file_arr,finalize_callback){
		var file_count = 0;
		var total_files = file_arr.length;

		function gather(f){
			file_count++;
			if (file_count >= total_files-1){
				finalize_callback();
			}
		}

		for (var i=0;i<file_arr.length;i++){
			this.add_file(file_arr[i],gather);
		}
	}
	remove_multiple(id_arr){
		this.files = this.files.filter(function(f){return !id_arr.includes(f.file_id); });
	}
	remove_all(){
		this.files = [];
	}
	remove_file_by_id(file_id){
		var result = this.files.findIndex(function(f){return f.file_id==file_id});

		if (result >= 0){
			this.files.splice(result,1);
		}

		return true;
	}
	remove_files(filter_function) {
		var result = this.files.findIndex(filter_function);
		var removed_ids = []
		for (var i=0;i<result.length;i++){
			this.files.splice(result[i],1);
			removed_ids.push(result[i])
		}
		this.refresh_view();
		return removed_ids;
	}
	get_file_by_id(file_id) {
		var result = this.files.filter(function(f){return f.file_id==file_id});

		if (result.length > 0){
			return result[0];
		}

		return null;
	}
	toggle_status(file_id) {
		var file = this.get_file_by_id(file_id);
		if (file){
			var message = "Listo";
			var date_ready = true;
			var time_ready = true;
			var tinput = document.getElementById("time_input_file_"+file_id);
			var dinput = document.getElementById("date_input_file_"+file_id);
			var status_btn = document.getElementById("status_btn_"+file_id);
			var statustext = document.getElementById("status_text_"+file_id);
			

			if (!file.captured_on_date){
				date_ready = false;
				$(dinput).addClass("incorrect_pattern");
			} else {
				$(dinput).removeClass("incorrect_pattern");
			}
			if (!file.captured_on_time){
				time_ready = false;
				$(tinput).addClass("incorrect_pattern");
			} else {
				$(tinput).removeClass("incorrect_pattern");
			}

			if (!date_ready && !time_ready){
				message = "Sin momento";
			} else if (!date_ready){
				message = "Sin fecha";
			} else if (!time_ready) {
				message = "Sin tiempo";
			}

			
			statustext.textContent = message;

			if (message == "Listo"){
				statustext.style.display = "none";
				status_btn.style.display = "inline-block";
			} else {
				statustext.style.display = "inline-block";
				status_btn.style.display = "none";
			}

						
		}


	}
}
