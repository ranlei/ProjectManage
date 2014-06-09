$(document).ready(function(){
	judge();
			
	$.ajax({
		type:"GET",
		contentType: "application/json",
		// url:"http://localhost/newindex/index.php/admin_view/stu_info",
		url:"http://newindex.stuzone.com/index.php/admin_view/stu_info",

		async:true,
		dataType:'json',
		success:function(data){
			var info = "<tbody>";
			$.each(data,function(i,n){
				if(n['channel']==='guwen'){
						n['var']="故问";
					}else if(n['channel']==='shijue'){
						n['var']="视觉";	
					}else if(n['channel']==='shipin'){
						n['var']="视频";
					}else if(n['channel']==='tuijian'){
						n['var']="推荐";
					}else if(n['channel']==='zixun'){
						n['var']="资讯";
					}else if(n['channel']==='xiazai'){
						n['var']="下载";
					}else if(n['channel']==='shichang'){
						n['var']="市场";
					}

					info += "<tr><td>" +i+ "</td>" + "<td id=\"title_info\">" + n['any_title'] + "</td><td>" + n['var'] + "</td><td><button "+ "data=\""+n['self_id'] +"\" type=\"button\" data-toggle=\"modal\" data-target=\"#myModal\" class=\"infob btn-primary btn-sm\">修改</button></td></tr>";
				
			});
			info += "</tbody>";
			$("#info").append(info);
			var title_num =0;
			$('.infob').click(function() {
				title_num = $(this).attr("data");
				$.ajax({
						type:"POST",
						// url:"http://localhost/newindex/index.php/admin_view/modify_title",
						url:"http://newindex.stuzone.com/index.php/admin_view/modify_title",
						async:true,
						data:{content:title_num},
						
						success:function(data){
							var obj=eval("("+data+")");
							var mod_title = obj.any_title;
							$("#editor").html(mod_title);


							$('#submit_mod').click(function(){
								var title_mod_id = title_num;
								var title_con = $('#editor').html();
								$.ajax({

										type:"POST",
										// url:"http://localhost/newindex/index.php/admin_view/modify_title_out",
										url:"http://newindex.stuzone.com/index.php/admin_view/modify_title_out",
										async:true,
										data:{modify_title_id:title_mod_id,modify_title_con:title_con},
										dataType:"html",
										error:function(){
											alert("修改失败");
											console.log("fail");
										},
										success:function(){
											alert("修改成功");
											location.href="info_list.html";
											}

									});

							});
							
						}

					});


			});
			
		}

	});
	
	
});