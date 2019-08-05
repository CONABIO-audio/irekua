$( document ).ready(function() {

		var canvas = document.getElementById('canvas');

		if (canvas) {
			HTMLCanvasElement.prototype.fit_to_img = function() {
				this.image = new Image();
				this.image.src = this.img_url;
				this.img_coeff = this.image.height/this.image.width;
				this.height = Math.round(this.width*this.img_coeff);
			}
			HTMLCanvasElement.prototype.clean_canvas = function() {
		    	this.getContext('2d').clearRect(0,0,this.width,this.height);
		    	this.tmp_ann = null;
			}
			HTMLCanvasElement.prototype.init_image_annotator = function(img_url) {
				this.img_url = img_url;
				this.tmp_ann = null;
				this.image = null;
				this.img_coeff = null;

				this.ctx = this.getContext('2d');
				this.client_rect = canvas.getBoundingClientRect();
		        this.scaleX = this.width / this.client_rect.width;
		        this.scaleY = this.height / this.client_rect.height;
				this.pos_x = this.client_rect.left;
				this.pos_y = this.client_rect.top;

				this.fit_to_img()
			}
			HTMLCanvasElement.prototype.load_annotation = function(px_x,px_y,px_width,px_height){

			    dwidth = Math.round((px_width/this.image.width)*this.width);
			    dheight = Math.round((px_height/this.image.height)*this.height);
			    dul_x = Math.round((px_x/this.image.height)*this.height);
			    dul_y = Math.round((px_y/this.image.height)*this.height);
				
		        this.ctx.clearRect(0,0,this.width,this.height);
		        this.ctx.beginPath();
		        this.ctx.setLineDash([]);
		        this.ctx.rect(dul_x,dul_y,dwidth,dheight);
		        this.ctx.strokeStyle = "yellow";
		        this.ctx.lineWidth = 5;
		        this.ctx.stroke();

			}

			HTMLCanvasElement.prototype.draw_annotation = function(mouse_x,mouse_y,width,height,color='red',line_dash=[10, 15],clear_prev=true,persist=false) {

				if (clear_prev){
		        	this.ctx.clearRect(0,0,this.width,this.height);
				}

		        this.ctx.beginPath();
		        this.ctx.setLineDash(line_dash);
		        this.ctx.rect(mouse_x,mouse_y,width,height);
		        this.ctx.strokeStyle = color;
		        this.ctx.lineWidth = 5;
		        this.ctx.stroke();

		        if (persist){
			        dwidth = Math.round((width/this.width)*this.image.width);
			        dheight = Math.round((height/this.height)*this.image.height);
			        dul_x = Math.round((mouse_x/this.width)*this.image.width);
			        dul_y = Math.round((mouse_y/this.height)*this.image.height);

				    this.tmp_ann = {"width":dwidth,"height":dheight,"ul_x":dul_x,"ul_y":dul_y};
		        }
			}

			var addAnnForm = document.getElementById('addAnnForm');

			if (addAnnForm){
				var img_url = document.getElementById('img_url').value;

				canvas.init_image_annotator(img_url);

				var clean_canvas_btn = document.getElementById('canvas_clean');
				var last_mousex = last_mousey = width = height = 0;
				var mousex = mousey = 0;
				var mousedown = false;

				asigna_autocomplete_tax($('#tax_label'));

				var prev_annotation = document.getElementById('prev_annotation');
				var prev_label = document.getElementById('prev_label');
				
				if (prev_annotation){
					var annotation = JSON.parse(prev_annotation.value.replace(/\'/g,'"'));
					canvas.load_annotation(annotation["ul_x"],annotation["ul_y"],annotation["width"],annotation["height"]);
					document.getElementById("annotation_field").value = prev_annotation.value.replace(/\'/g,'"');
				}
				if (prev_label){
					var label_json = JSON.parse(prev_label.value.replace(/\'/g,'"'));
					document.getElementById("tax_label").value = label_json["especie"];
				}

		        addAnnForm.addEventListener('submit',function(e){
		            e.preventDefault();

		            var url = this.action;
		            var raw_label = document.getElementById('tax_label').value;
		            var annotation = document.getElementById('annotation_field').value;

		            form_complete = true;

		            if (!raw_label){
		            	form_complete = false;
		            } else {
		            	if (raw_label == ""){
		            		form_complete = false;
		            	}
		            }

		            if (annotation == "{}"){
		            	form_complete = false;
		            	alert("Dibuja un recuadro alrededor del objeto identificado")
		            }

		            if (form_complete){
			            var formData = new FormData($('#addAnnForm')[0]);
					 	var request = new XMLHttpRequest();
					 	var label_obj = {"especie":raw_label}
					 	formData.set('label',JSON.stringify(label_obj));
					 	request.open("POST",url,false);
					 	request.send(formData);
					 	window.location.href = url+"&finalize=true";
		            }
		        });

				clean_canvas_btn.onclick = function(){
					canvas.clean_canvas();
					width = 0;
					height = 0;
				}

				$(canvas).on('mousedown', function(e) {
				    last_mousex = Math.min(canvas.width,Math.max(0,Math.round((e.clientX-canvas.pos_x + $("#view_content").scrollLeft())*canvas.scaleX)));
					last_mousey = Math.min(canvas.height,Math.max(0,Math.round((e.clientY-canvas.pos_y + $("#view_content").scrollTop())*canvas.scaleY)));
					width = 0;
					height = 0;
				    mousedown = true;
				});

				$(document).on('mouseup', function(e) {
					if (mousedown){

						mousedown = false;

					    if (Math.abs(width) > 10 && Math.abs(height) > 10){

					        canvas.draw_annotation(last_mousex,last_mousey,width,height,'yellow',[],true,true);

						    document.getElementById("annotation_field").value = JSON.stringify(canvas.tmp_ann);

					    	width = 0;
					    	height = 0;
						    //alert(document.getElementById("annotation_field").value)
					    } else {
					    	canvas.clean_canvas();
					    	width = 0;
					    	height = 0;
					    }

					}
				});

				$(document).on('mousemove', function(e) {
				    mousex = Math.min(canvas.width,Math.max(0,Math.round((e.clientX-canvas.pos_x + $("#view_content").scrollLeft())*canvas.scaleX)));
					mousey = Math.min(canvas.height,Math.max(0,Math.round((e.clientY-canvas.pos_y + $("#view_content").scrollTop())*canvas.scaleY)));

				    if(mousedown) {

				        width = mousex-last_mousex;
				        height = mousey-last_mousey;

						canvas.draw_annotation(last_mousex,last_mousey,width,height);
				    }
				});


			} else {
				var img_url = document.getElementById('img_url').value;
				canvas.init_image_annotator(img_url);
				var row_arr = document.getElementsByClassName('list_item');
				if (row_arr){
					row_arr[0].classList.add("selected_ann");
					var annotation = JSON.parse(row_arr[0].querySelector("input").value.replace(/\'/g,'"'));
					canvas.load_annotation(annotation["ul_x"],annotation["ul_y"],annotation["width"],annotation["height"]);
				}

				$('.list_item').on('click', function() {
					var selected_arr = document.getElementsByClassName('selected_ann');
					for (var i=0;i<selected_arr.length;i++){
						selected_arr[i].classList.remove("selected_ann");
					}
					this.classList.add("selected_ann");
					var annotation = JSON.parse(this.querySelector("input").value.replace(/\'/g,'"'));
					canvas.load_annotation(annotation["ul_x"],annotation["ul_y"],annotation["width"],annotation["height"]);

				});

			}


		}
});