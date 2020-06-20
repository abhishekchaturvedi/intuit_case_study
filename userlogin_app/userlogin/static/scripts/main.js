var login = function () {
  var $login = $('#login');

  $login.on('submit', function(event) {
    event.preventDefault();

    var url = $login.attr('action');
    var $username = $('#username');
    var $password = $('#password');

    var data = {
      'username': $username.val(),
      'password': $password.val()
    }

    return $.ajax({
      type: 'post',
      url: url,
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(data),
      processData: false,
      success: function(response, status, xhr) {
        window.location.replace(redirect);
      },
      error: function(response, status, xhr) {
        $error.text(response.responseText);
        $error.show();
      }
    });
  });
};


// Initialize everything when the DOM is ready.
$(document).ready(function() {
  login();
});
