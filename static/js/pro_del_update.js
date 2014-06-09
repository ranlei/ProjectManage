$(document).ready(function(){
	$('.del_num').click(function(){ //删除角色或者职员，顾客
			var num_id = $(this).attr("data_num");
			var name = $(this).attr("data");
			$.ajax({
				type:"POST",
				url:"./del_num",
				data:{num_id:num_id,num_name:name},
				dataType:"text",

				success:function(){
					alert("success!");
					if (name=="role") {
						location.href="/list_role";
					}else if(name=="emp"){
						location.href="/list_employee";
					}else if(name=="cli"){
						location.href="/list_client";
					};

				}
			});
	});


	$('.getall').click(function(){//获取所有信息，以及修改
		var num_id = $(this).attr("data_num");
		var name = $(this).attr("data");
		var guess = $(this).attr("data-guess");
		$.ajax({
			type:"POST",
			url:"/get_all",
			data:{num_id:num_id,num_name:name},
			dataType:"text",
			success:function(data){
				var obj = jQuery.parseJSON(data);
				
				if(guess=="mod"){
					$('#any_name').val(obj.Name);
					$('#any_tel').val(obj.telNo);
					$('#any_addr').val(obj.address);
					$('#any_email').val(obj.empEmailAddress);
					$('#any_zhiwei').text(obj.role_name);

				}else if(guess=="detail"){

					$('#any_name_x').text(obj.Name);
					$('#any_tel_x').text(obj.telNo);
					$('#any_addr_x').text(obj.address);
					$('#any_email_x').text(obj.empEmailAddress);
					if(obj.sex==1){
						$('#any_sex_x').text("男");
					}else{
						$('#any_sex_x').text("女");
					}
					$('#any_power_x').text(obj.role_name);
					

				}

			}
		});


	});
	

});