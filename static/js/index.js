
// error callback
function error_cb(error) {
    console.log(error);
}

/*
 *
 *    Likes
 *
 */


// 下面的$$('.submit-like').on('click', function() {
//   create_like.call(this, like_update_view, error_cb);
// });     说到：
// 当调用里create_like后，根据不同当结果我会有不同当call back.

// OVERALL: 通过create_like里ajax的url path找到urls.py 的 /Insta/like/ -> 调用views.py的addLike -> 返回结果到这里的create_like
// 如果成功创建了Like, 那就回调like_update_view；失败的话就call back error_cb()
function create_like(success_cb, error_cb) {
    //从当前的html里的icon （this)看下有没有siblings, 如果它们有hidden-data的话，
    // 找到hidden-data里的post-pk转为text, 赋值到 var post_pk
    // 
    var post_pk = $(this).siblings('.hidden-data').find('.post-pk').text();
    console.log(post_pk);

    // ajax对当前界面进行一个局部更改：发生POST请求to url /Insta/like with the data post_pk
    $.ajax({
        type: "POST",
        url: '/like',
        data: {
            post_pk: post_pk //key: value
        },
        success: function(data) { success_cb(data); },
        error: function(error) { error_cb(error); }
    });
}

//success_cb for create_like success callback
function like_update_view(data) {
    console.log(data);

    // toggle heart
    var $hiddenData = $('.hidden-data.' + data.post_pk);//data is what ajax's data above has: post_pk, pulled from index.html's (for post in posts.objects)
    if (data.result) {//if 1: 找到hidden-data的同级submit-like，弄走小空心，加上小红心
      $hiddenData.siblings('.submit-like').removeClass('fa-heart-o').addClass('fa-heart');
    } else {//if 0: 
      $hiddenData.siblings('.submit-like').removeClass('fa-heart').addClass('fa-heart-o');
    }
  
    // update like count
    var difference = data.result ? 1 : -1; //if result = 1:点赞，那么+1; 否则-1
    var $post = $('.view-update.' + data.post_pk);
    var $likes = $post.find('.likes');
    var likes = parseInt($likes.text());
    likes = likes + difference;
  
    console.log('likes', likes);
  
    if (likes == null || isNaN(likes)) {
      $likes.text('1 like');
    } else if (likes === 0) {
      $likes.text('');
    } else if (likes === 1) {
      $likes.text('1 like');
    } else {
      $likes.text(likes + ' likes');
    }
}
 
// 在index.html, post_detail.html等地方，在点赞那一块儿的DOM(document object model)里有
// <i class="fa {% has_user_liked_post post user %} submit-like" aria-hidden="true"></i>
// 这个icon里面有三个class，其中一个class是 submit-like：专门为了index.js找得到这个class
// $('.submit-like') 是去html里找属于submit-like这个class的attributes 
// (如index.html和post_detail.html里各有一个这么个submit-like的attribute)
// 这里制作一个Listener, 如果click的话，就用当前的object (this) 去调用一个function：create_like
// 并且传入两个参数： success_cb, error_cb
$('.submit-like').on('click', function() {
    create_like.call(this, like_update_view, error_cb);
});

  
/*
*
*    Comments
*
*/
  
function enterPressed(e) {
    if (e.key === "Enter") { return true; }
    return false;
}
   
function validComment(text) {
    if (text == '') return false;
    return true;
}
  
function create_comment(success_cb, error_cb) {
    var comment_text = $(this).val();
    var post_pk = $(this).parent().siblings('.hidden-data').find('.post-pk').text();
  
    console.log(comment_text, post_pk);
  
    $.ajax({
      type: "POST",
      url: '/comment',
      data: {
        comment_text: comment_text,
        post_pk: post_pk
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}

function comment_update_view(data) {
    console.log(data);
    var $post = $('.hidden-data.' + data.post_pk);
    var commentHTML = '<li class="comment-list__comment"><a class="user"> ' + data.commenter_info.username + '</a> <span class="comment">'
                    + data.commenter_info.comment_text +'</span></li>'
  
    $post.closest('.view-update').find('.comment-list').append(commentHTML);
  }
  
  $('.add-comment').on('keyup', function(e) {
    if (enterPressed(e)) {
      if (validComment($(this).val())) {
        create_comment.call(this, comment_update_view, error_cb);
        $(this).val('');
      }
    }
  });
  

/*
 *
 *    Follow/Unfollow
 *
 */

function follow_user(success_cb, error_cb, type) {
    var follow_user_pk = $(this).attr('id');
    console.log(follow_user_pk);
  
    $.ajax({
      type: "POST",
      url: '/togglefollow',
      data: {
        follow_user_pk: follow_user_pk,
        type: type
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}
  
function update_follow_view(data) {
    console.log('calling update_follow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('unfollow-user').removeClass('follow-user');
    $button.text('Unfollow');

    var $span = $('.follower_count');
    var span_text = parseInt(document.getElementById("follower_id").innerText);
    $span.text(span_text + 1);
}

function update_unfollow_view(data) {
    console.log('calling update_unfollow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('follow-user').removeClass('unfollow-user');
    $button.text('Follow');

    var $span = $('.follower_count');
    var span_text = parseInt(document.getElementById("follower_id").innerText);
    $span.text(span_text - 1);
}


$('.follow-toggle__container').on('click', '.follow-user', function() {
    follow_user.call(this, update_follow_view, error_cb, 'follow');
});

$('.follow-toggle__container').on('click', '.unfollow-user', function() {
    follow_user.call(this, update_unfollow_view, error_cb, 'unfollow');
});