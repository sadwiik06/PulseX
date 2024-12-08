   

    $(".menu > ul > li").click(function (e) {
    // remove active from already active
    $(this).siblings().removeClass("active");
    // add active to clicked
    $(this).toggleClass("active");
    // if has sub menu open it
    $(this).find("ul").slideToggle();
    // close other sub menu if any open
    $(this).siblings().find("ul").slideUp();
    // remove active class of sub menu items
    $(this).siblings().find("ul").find("li").removeClass("active");
  });
  
  $(".menu-btn").click(function () {
    $(".sidebar").toggleClass("active");
  });
  
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-btn');
  
    menuBtn.addEventListener('click', function () {
      // Check if the sidebar has the class "hidden" (for mobile) or "active" (for desktop)
      if (window.innerWidth <= 768) {
        // Toggle hidden class for mobile devices
        sidebar.classList.toggle('hidden');
      } else {
        // Toggle active class for larger screens
        sidebar.classList.toggle('active');
      }
    });

  