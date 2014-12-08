msgformPost = function () {
  // Do something
  var input = document.getElementById("msg_form");
  var inputData = encodeURIComponent(input.value);
  sendMessage("/send_message", "to=" + receiverName + "&msg=" + inputData);
  messages.push({"msg": input.value});
  updateMessageWindow();
  input.value = '';
  document.getElementById("msg_form").focus();
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
  console.log(newMessage);
  messages.push(newMessage);
  updateMessageWindow();
}

updateMessageWindow = function() {
  var htmlString = "<ul>";

  console.log(messages);

  for (i = 0; i < messages.length; i++) {
    if (messages[i].from) {
      htmlString += "<li><div class=\"bubble\"><a class=\"user-name\" href=\"\">";
      htmlString += messages[i].from;      
    }
    else {
      htmlString += "<li class=\"current-user\"><div class=\"bubble\"><a class=\"user-name\" href=\"\">";
      htmlString += "Me";
    }

    htmlString += "</a><p class=\"message\">"
    htmlString += messages[i].msg;
    htmlString += "</p>";
    htmlString += "</div></li>"
  }

  htmlString += "</ul>";

  $("#message_window").html(htmlString);

  var objDiv = document.getElementById("message_window");
  objDiv.scrollTop = objDiv.scrollHeight;
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
var messages = [];
setTimeout(initialize, 100);

$(document).ready(function() {
  $('.friend').on("click", function() {
    var user_name =  $(this).attr("id");
    if (receiverName != user_name) {
      receiverName = user_name;
      $("#chat_title").html("<i class=\"icon-comments\"></i>Chat with " + user_name + "<i class=\"icon-cog pull-right\"></i><i class=\"icon-smile pull-right\"></i>");
      $("#message_input").html("<form action=\"javascript:msgformPost();\"><input class=\"form-control\" placeholder=\"Input Message...\" type=\"text\" id=\"msg_form\"><input type=\"submit\" value=\"Send\" id=\"send_msg_btn\"></form>");
      messages = [];
      updateMessageWindow();
    }
    document.getElementById("msg_form").focus();
  });
});