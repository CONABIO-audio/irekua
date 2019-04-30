var dataPointsRes = null;

function init_map(){
    $.ajax({url:mapUrl,
      type:"GET",
      success: function(result){
          dataPoints
          alert(JSON.stringify(result));

      },
      error:function(error){
        alert("Error")
      }
    });
}

$(document).ready(function() {
  init_map();
});