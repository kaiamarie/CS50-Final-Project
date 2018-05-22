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

function class_scroll(content) {
    var elmnt = document.getElementById(content);
    elmnt.scrollIntoView();
    window.scrollBy(0, -100);
}


$(document).ready(function(){
    // Activate Carousel
    $("#myCarousel").carousel();

    // Enable Carousel Indicators
    $(".item1").click(function(){
        $("#myCarousel").carousel(0);
    });
    $(".item2").click(function(){
        $("#myCarousel").carousel(1);
    });
    $(".item3").click(function(){
        $("#myCarousel").carousel(2);
    });
    $(".item4").click(function(){
        $("#myCarousel").carousel(3);
    });

    // Enable Carousel Controls
    $(".left").click(function(){
        $("#myCarousel").carousel("prev");
    });
    $(".right").click(function(){
        $("#myCarousel").carousel("next");
    });
});
