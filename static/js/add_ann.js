$(document).ready(function(){
	judge();

	$("#sub_con").click(function(){
		var content = $("#editor").html();
		$.ajax({
			type:"POST",
			// url:"http://localhost/newindex/index.php/admin_view/stu_ann",
			url:"http://newindex.stuzone.com/index.php/admin_view/stu_ann",
			async:true,
			data:{content:content},
			dataType:"html",
			error:function(){


				alert("fail");
			},
			success:function(){
				alert("添加成功");
				location.href="ann_list.html";
				
			}

		});


	});

});

