$(function(){
  //アクションボタンをクリックした場合、クリックしたものにactiveがつく
  $('.sec-block-set__button-block').on('click',function(){
    $('.sec-block-set__button-block').removeClass('active');
    $('.sec-block-set__color-choose').removeClass('active');
    if($(this).hasClass('js-edit')){
      $('.sec-block-set__color-choose').addClass('active');
    }
    $(this).addClass('active');
  });

  //色選択
  $('.sec-block-set__color-choose li').on('click',function(){
    if($('.js-edit').hasClass('active')){ //編集モードのとき
      $('.sec-block-set__color-choose li').removeClass('active');
      $(this).addClass('active');
    }
  })

  //ブロックがクリックされた場合
  $('.sec-block-set__top td').on('click',function(){
    if($('.js-edit').hasClass('active')){ //編集モードのとき
      var color = $('.sec-block-set__color-choose').find('.active').attr('id');
      $(this).removeClass();
      $(this).addClass(color);
      $(this).addClass('on');
      console.log('あれ？？？？？？？？');
    }else if($('.js-delete').hasClass('active')){ //削除モードのとき
      $(this).removeClass();
    }
  });

  //全消しモード
  $('.js-clear').on('click',function(){
    $('.sec-block-set__top td').removeClass();
  });

})
