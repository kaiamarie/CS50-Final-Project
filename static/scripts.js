// function to check in register.html that password and confirm password are the same
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
