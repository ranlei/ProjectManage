$(document).ready(function(){
	judge();
			
	$.ajax({
		type:"GET",
		contentType: "application/json",
		// url:"http://localhost/newindex/index.php/admin_view/getAllann",
		url:"http://newindex.stuzone.com/index.php/admin_view/getAllann",

		async:true,
		dataType:'json',
		success:function(data){
			var info = "<tbody>";
			$.each(data,function(i,n){
				
					info += "<tr><td>" +i+ "</td>" + "<td id=\"title_info\">" + n['content'] + "</td>" + "<td><button "+ "data=\""+n['id'] +"\" type=\"button\" data-toggle=\"modal\" data-target=\"#myModal\" class=\"infob btn-primary btn-sm\">修改</button>&nbsp;&nbsp;<button "+ "data=\""+n['id'] +"\" type=\"button\" data-toggle=\"modal\" class=\" del_ann btn-primary btn-sm\">删除</button></td></tr>";
				
			});
			info += "</tbody>";
			$("#info").append(info);
			var del_ann=0;
			$('.del_ann').click(function() {
				del_ann = $(this).attr("data");
				console.log(del_ann);
				$.ajax({
						type:"POST",
						// url:"http://localhost/newindex/index.php/admin_view/delAnn",
						url:"http://newindex.stuzone.com/index.php/admin_view/delAnn",
						async:true,
						data:{ann_id:del_ann},
						error:function(){
							console.log("fail");
						},
						success:function(){
							

							alert("删除成功");
							location.href="ann_list.html"; 
							
						}

					});


			});
			var title_num =0;
			$('.infob').click(function() {
				title_num = $(this).attr("data");
				$.ajax({
						type:"POST",
						// url:"http://localhost/newindex/index.php/admin_view/getModify",
						url:"http://newindex.stuzone.com/index.php/admin_view/getModify",
						async:true,
						data:{ann_id:title_num},
						error:function(){
							console.log("fail");
						},
						success:function(data){
							var obj=eval("("+data+")");
							var mod_title = obj.content;
							console.log();
							$("#editor").html(mod_title);


							$('#submit_mod').click(function(){
								var mod_id = title_num;
								var ann_con = $('#editor').html();
								$.ajax({

										type:"POST",
										// url:"http://localhost/newindex/index.php/admin_view/modifyAnn",
										url:"http://newindex.stuzone.com/index.php/admin_view/modifyAnn",
										async:true,
										data:{ann_id:mod_id,content:ann_con},
										dataType:"html",
										error:function(){
											alert("修改失败");
											console.log("fail");
										},
										success:function(){
											alert("修改成功");
											location.href="ann_list.html"; 
											}

									});

							});
							
						}

					});


			});
			
	

			
			
		}

	});
	
	
});