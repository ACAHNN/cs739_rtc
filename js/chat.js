msgformPost = function () {
  // Do something
  var input = document.getElementById("msg_form");
  var inputData = encodeURIComponent(input.value);
  sendMessage("/send_message", "to=" + receiverName + "&msg=" + inputData);
  messages.push({"to":receiverName, "msg": input.value});
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
  //console.log(newMessage);
  if (newMessage.control) {
    //alert("User login in other place!");
    //$(location).attr('href',"/login");
    if (newMessage.control == 'logout') {
      for (var i = 0; i < friends.length; i++) {
        if (friends[i].online && friends[i].user_name == newMessage.user_name) {
          friends[i].online = false;
        }
      }
    }
    else if (newMessage.control == 'logon') {
      for (var i = 0; i < friends.length; i++) {
        if (!friends[i].online && friends[i].user_name == newMessage.user_name) {
          friends[i].online = true;
        }
      }
    }
    refreshFriendList(friends);
    if (newMessage.control == 'logout' && newMessage.user_name == receiverName) {
      $("#chat_title").html("");
      $("#message_input").html("");
      receiverName = "";
    }
  }
  else {
    //console.log(newMessage);
    messages.push(newMessage);
    updateMessageWindow();
  }
}

getFriendList = function() {
  $.ajax({
    url: '/friend_list',
    type: 'GET',
    success: function(data, status){
      //console.log("Data = " + data +", status = " + status);
      friends = JSON.parse(data);
      refreshFriendList(friends);
    }
  });
}

friendItemHtmlString = function(friend_name, online) {
  var htmlString = "<li><a ";

  if (online) {
    htmlString += "class=\"friend\" href=\"javascript:void(0)\" id=" + friend_name + ">" + friend_name;
    htmlString += "<i class=\"icon-circle text-success\"></i></a></li>"
  }
  else {
    htmlString += "id=" + friend_name + ">" + friend_name;
    htmlString += "<i class=\"icon-circle text-danger\"></i></a></li>"
  }
  return htmlString;
}

refreshFriendList = function(friends) {
  var htmlString = "<div class=\"heading\">Contacts(";
  htmlString += friends.length;
  htmlString += ")<a class=\"icon-plus pull-right\" href=\"/add_friend\"></a></div>";
  htmlString += "<ul>";

  var onlineFriends = [];
  var offlineFriends = [];

  for (var i in friends) {
    if (friends[i].online) {
      onlineFriends.push(friends[i]);
    }
    else {
      offlineFriends.push(friends[i]);
    }
  }

  for (var i in onlineFriends) {
    htmlString += friendItemHtmlString(onlineFriends[i].user_name, true);
  }

  for (var i in offlineFriends) {
    htmlString += friendItemHtmlString(offlineFriends[i].user_name, false);
  }

  htmlString += "</ul>";
  htmlString += "</div>";
  $("#friend_list").html(htmlString);

  $('.friend').on("click", function() {
    var user_name =  $(this).attr("id");
    if (receiverName != user_name) {
      receiverName = user_name;
      $("#chat_title").html("<i class=\"icon-comments\"></i>Chat with " + user_name + "<i class=\"icon-cog pull-right\"></i><i class=\"icon-smile pull-right\"></i>");
      $("#message_input").html("<form action=\"javascript:msgformPost();\"><input class=\"form-control\" placeholder=\"Input Message...\" type=\"text\" id=\"msg_form\"><input type=\"submit\" value=\"Send\" id=\"send_msg_btn\"></form>");
      updateMessageWindow();
    }
    document.getElementById("msg_form").focus();
  });
}

updateMessageWindow = function() {
  var htmlString = "<ul>";

  //console.log(messages);

  for (i = 0; i < messages.length; i++) {
    var validMessage = false;
    if (messages[i].from) {
      if (messages[i].from == receiverName) {
        htmlString += "<li><div class=\"bubble\"><a class=\"user-name\" href=\"\">";
        htmlString += messages[i].from;
        validMessage = true;
      }
    }
    else {
      if (messages[i].to == receiverName) {
        htmlString += "<li class=\"current-user\"><div class=\"bubble\"><a class=\"user-name\" href=\"\">";
        htmlString += "Me";
        validMessage = true;
      }
    }

    if (validMessage) {
      htmlString += "</a><p class=\"message\">"
      htmlString += messages[i].msg;
      htmlString += "</p>";
      htmlString += "</div></li>";
    }
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
    'onerror': function() {console.log("channel in error!")},
    'onclose': function() {console.log("closed!")}
  };
  var socket = channel.open(handler);
  socket.onopen = onOpened;
  socket.onmessage = onMessage;
}

initialize = function() {
  openChannel();
  //onMessage({data: '{{ initial_message }}'});
}

var receiverName = "";
var messages = [];
var friends = [];

setTimeout(initialize, 100);

$(document).ready(function() {
  getFriendList();
});