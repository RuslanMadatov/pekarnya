jQuery(() => {
  $(".menu-item-has-children [href]").each(function () {
      if (this.href == window.location.href) {
          $(this).addClass("menu_active");
      }
  });
});

jQuery(() => {
  $(".tab_01 ").each(function () {
      if (this.href == window.location.href) {
          $(this).addClass("active");
      }
  });
});