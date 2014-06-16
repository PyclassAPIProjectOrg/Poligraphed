$(function() {

   $('.menu').click(function(){
    var  $icon = $(this).find('.glyphicon');
     $('.nav-sidebar').collapse();

     if( $icon.hasClass('glyphicon-plus') ) {
      $icon.removeClass('glyphicon-plus');
      $icon.addClass('glyphicon-minus');
     } else if( $icon.hasClass('glyphicon-minus') ) {
      $icon.removeClass('glyphicon-minus');
      $icon.addClass('glyphicon-plus');
     }

   });

});
