class FileUploader {
	constructor(parent,form,title){
		this.parent = parent;
		this.form = form;
		this.title = title;
		this.initialize();
	}
	initialize() {
		this.files = [];
		this.last = 0;
		this.build_view();
	}
	build_view() {
		if (this.container){
			$(this.container).remove();
		}
		this.container = document.createElement('div');
		this.container.className = "container";
		this.build_top_toolbar();
		this.build_body();
	}
	build_top_toolbar() {
		if (this.top_toolbar){
			$(this.top_toolbar).remove();
		}
		this.top_toolbar = document.createElement('div');
		this.top_toolbar.className = "row";
		var file_btn = document.createElement('a');
		this.file_picker = document.createElement('input');
		this.file_picker.type = "file";
		file_btn.appendChild(this.file_picker);
		
		this.top_toolbar.appendChild(file_btn);
		this.container.appendChild(this.top_toolbar);
	}
	build_body() {
		if (this.body){
			$(this.body).remove();
		}
		this.body = document.createElement('div');
		this.body.className = "row";
		this.build_files_section();
		this.build_results_section();
		this.container.appendChild(this.body);
	}
	build_files_section() {
		if (this.files_section){
			$(this.files_section).remove();
		}
		this.files_section = document.createElement('div');
		this.files_section.className = "col";
		this.body.appendChild(this.files_section);
	}
	build_results_section() {
		if (this.results_section){
			$(this.results_section).remove();
		}
		this.results_section = document.createElement('div');
		this.results_section.className = "col";
		this.body.appendChild(this.results_section);
	}
	get_file_page(page, per_page, filter_function) {
		var page = page || 1,
		per_page = per_page || 10,
		filteredItems = this.files.filter(filter_function);
		total_pages = Math.ceil(filteredItems.length / per_page);

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
		while ($(this.files_section).firstChild) {
			$(this.files_section).removeChild(this.files_section.firstChild);
		}
		for (var i=0;i<page.data.length;i++){
			var row = document.createElement('div');
			row.className = 'row d-flex justify-content-between list_item';
			row.align = "center";
			row.style["margin"] = "10px";
		}
	}
	retrieve_media_info(file) {
		if (file.item_type){
			var fr = new FileReader;

			fr.onloadend = function(){
				var exif = EXIF.readFromBinaryFile(new BinaryFile(this.result));
				file["media_info"] = exif;
			}

			fr.readAsBinaryString(file);
		}

		return null;
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
	            if ('year' in date_parser_map && 'month' in date_parser_map && 'day' in date_parser_map && 'second' in date_parser_map){
	              date_parser_map["regexp"] = date_regexp;
	              return date_parser_map;
	            }
	          }
	        }
	      }

	      return false;
	}
	generate_id() {
		var new_id = this.last_id + 1;
		this.last_id = this.last_id + 1;

		return new_id;
	}
	is_uploadable(file){
		if (file.item_type){
			if (file.captured_on || file.force_upload){
				return true;
			}
		}
		return false;		
	}
	is_fixable(file){
		if (file.item_type && !file.captured_on){
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
		if (!file.item_type || !file.captured_on){
			return true;
		}
		return false;
	}
	add_file(file){
		file["captured_on"] = null;
		file["item_type"] = null;
		file["media_info"] = null;
		file["veto_upload"] = false;
		file["force_upload"] = false;
		file["file_id"] = this.generate_id();
		this.files.push(file);
	}
	remove_file_by_id(file_id){
		var result = this.files.findIndex(function(f){return f.file_id==file_id});
		
		if (result.length > 0){
			this.files.splice(result[0],1);
		}
		this.refresh_view();
		return true;
	}
	get_file_by_id(file_id) {
		var result = this.files.filter(function(f){return f.file_id==file_id});
		
		if (result.length > 0){
			return result[0];
		}

		return null;
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
}