$(document).ready(function(){
    $(".pro_ul").on("click",".pro_item",function(){
        $(".pro_ul").children().attr("class","pro_item")
        $(this).attr("class","pro_item active");
    });
});
