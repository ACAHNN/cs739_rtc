$(document).ready(function(){
  $('.friend').on("click",function(){
    var user_name =  $(this).attr("id");
    $("#chat_title").html("<i class=\"icon-comments\"></i>Chat with " + user_name + "<i class=\"icon-cog pull-right\"></i><i class=\"icon-smile pull-right\"></i>")
    $("#message_input").html("<input class=\"form-control\" placeholder=\"Input Message...\" type=\"text\"><input type=\"submit\" value=\"Send\">")
  })
});