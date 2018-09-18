// function to check in register.html that password and confirm password are the same
// from https://stackoverflow.com/questions/39473247/javascript-password-and-password-confirmation-match
function passcheck() {

      var password = document.getElementById("password")
        , confirmation = document.getElementById("confirmation");

      function validatePassword(){
        if(password.value != confirmation.value) {
          confirmation.setCustomValidity("Passwords Don't Match");
          confirmation.validity==false;
          return false;
        } else {
          confirmation.setCustomValidity('');
        }
      }
      validatePassword()
}

function class_scroll(content) {
    var elmnt = document.getElementById(content);
    elmnt.scrollIntoView();
    window.scrollBy(0, -100);
}

$(function () {
  $('[data-toggle="popover"]').popover()
})
