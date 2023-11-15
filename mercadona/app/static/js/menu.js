document.addEventListener("DOMContentLoaded", function() {
    var menuIcon = document.getElementById("menu_icon");
    var menuTxt = document.getElementById("menu_txt");
      
    menuIcon.addEventListener("click", function() {
      // Toggle la classe "show" pour afficher ou masquer le menu
      menuTxt.classList.toggle("show");
    });
  });
  