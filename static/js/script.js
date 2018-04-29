$(function(){
  $('.sec-block-set__color-choose li').on('click',function(){
    $('.sec-block-set__color-choose li').removeClass('active');
    $(this).addClass('active');
  })
  $('.sec-block-set__top td').on('click',function(){
    var color = $('.sec-block-set__color-choose').find('.active').attr('id');
    $(this).removeClass();
    $(this).addClass(color);
  })
  $('.sec-block-set__button-block').on('click',function(){
    $('.sec-block-set__button-block').removeClass('active');
    $('.sec-block-set__color-choose li').removeClass('active');
    $(this).addClass('active');
  })
})
