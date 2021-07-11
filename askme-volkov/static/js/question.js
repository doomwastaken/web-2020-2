function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function create_like(id, type, is_positive) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/ajax/like/',
        type: 'post',
        data: {id: id, type: type, is_positive: is_positive},
        success: function(data) {
            document.getElementById('rating_' + type + '_' + id).textContent = data.likes_count;
            if (is_positive) {
           //   document.getElementById('upvote_' + type + '_' + id).setAttribute("disabled", true)
              var upvote_img = document.getElementById('upvote_' + type + '_' + id + '_img')
              upvote_img.src = '/static/svg/arrow_up_fill.svg'
            }
            if (!is_positive) {
              // document.getElementById('downvote_' + type + '_' + id).setAttribute("disabled", true)
               var downvote_img = document.getElementById('downvote_' + type + '_' + id + '_img')
               downvote_img.src = '/static/svg/arrow_down_fill.svg'
             }
        },
        failure: function(data) {
            alert('error')
        }
    })
};

function mark_as_correct(qid) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/ajax/mark_correct/',
        type: 'post',
        data: {id: qid},
        success: function(data) {
          var chkbox = document.getElementById('answer_' + qid + '_checked')
          chkbox.setAttribute('checked', data.is_correct)
          if (data.is_correct) {
            chkbox.setAttribute('disabled', true)
          } else {
            chkbox.setAttribute('enabled', true)  
          }
        },
        failure: function(data) {
            alert('error')
        }
    })
}


// $('.js_correct').click(function (ev) {
//     // ev.preventDefault()
//     var $this = $(this),
//         answer_id = $this.data('aid'),
//         question_id = $this.data('qid');
//     $.ajax('/mark_correct/', {
//         method: 'POST',
//         data: {
//             answer_id: answer_id,
//             question_id: question_id,
//         }
//     })
// })
