$(document).ready(function(){
  $(".archive-year").click(function(){
    if($(this).siblings(".archive-month").css('display') == 'none'){
      $(this).siblings(".archive-month").show();
    }
    else{
      $(this).siblings(".archive-month").hide();
    }
    if($(".archive-module-hide-button").css('display') == 'none'){
      $(".archive-module-hide-button").show();
      $(".archive-module-show-button").hide();
    }
    else{
      $(".archive-module-hide-button").hide();
      $(".archive-module-show-button").show();
    }
  });
});