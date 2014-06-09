function judge(){
	$.ajax({
				type:"POST",
				// url:"http://localhost/newindex/index.php/admin_view/judge_session",
				url:"http://newindex.stuzone.com/index.php/admin_view/judge_session",
				dataType:"json",
				
				success:function(data){
					if(data){
						console.log("success");
					}else{
						location.href="index.html";
					}
					
				}
			});
}

$(document).ready(function(){
	$("#exit_sys").click(function(){
		$.ajax({
				type:"POST",
				// url:"http://localhost/newindex/index.php/admin_view/des_session",
				url:"http://newindex.stuzone.com/index.php/admin_view/des_session",
				dataType:"json",
				success:function(){
					
					location.href="index.html";	
				}
			});

	});

});