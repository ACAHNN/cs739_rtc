msgformPost = function () {
  // Do something
  var input = document.getElementById("msg_form");
  var inputData = encodeURI(input.value);
  sendMessage("/send_message", "to=" + receiverName + "&msg=" + inputData);
  input.value = '';
}

getHttpRequest = function () {
    var xmlhttp;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    } else {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    return xmlhttp;
}

sendMessage = function(path, msg) {
  var xhr = getHttpRequest();
  xhr.open('POST', path, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send(msg);
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

var receiverName;
setTimeout(initialize, 100);
$(document).ready(function() {
  $('.friend').on("click", function() {
    var user_name =  $(this).attr("id");
    receiverName = user_name;
    $("#chat_title").html("<i class=\"icon-comments\"></i>Chat with " + user_name + "<i class=\"icon-cog pull-right\"></i><i class=\"icon-smile pull-right\"></i>");
    $("#message_input").html("<form action=\"javascript:msgformPost();\"><input class=\"form-control\" placeholder=\"Input Message...\" type=\"text\" id=\"msg_form\"><input type=\"submit\" value=\"Send\" id=\"send_msg_btn\"></form>")
  });
});