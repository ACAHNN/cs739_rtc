$(document).ready(function(){
  $('.friend').on("click",function(){
    var user_name =  $(this).attr("id");
    $("#chat_title").html("<i class=\"icon-comments\"></i>Chat with " + user_name + "<i class=\"icon-cog pull-right\"></i><i class=\"icon-smile pull-right\"></i>")
    $("#message_input").html("<input class=\"form-control\" placeholder=\"Input Message...\" type=\"text\"><input type=\"submit\" value=\"Send\">")
  })
});

sendMessage = function(path, opt_param) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send();
};

onOpened = function() {
  //sendMessage('/send_message');
};

onMessage = function(m) {
  newMessage = JSON.parse(m.data);
  updateMessageBox();
}

openChannel = function() {
  var channel = new goog.appengine.Channel(token);
  var handler = {
    'onopen': onOpened,
    'onmessage': onMessage,
    'onerror': function() {},
    'onclose': function() {}
  };
  var socket = channel.open(handler);
  socket.onopen = onOpened;
  socket.onmessage = onMessage;
}

initialize = function() {
  openChannel();
  //onMessage({data: '{{ initial_message }}'});
}

setTimeout(initialize, 100);  