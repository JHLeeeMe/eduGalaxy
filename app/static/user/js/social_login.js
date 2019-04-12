function buildQuery(params) {
    return Object.keys(params).map(function (key) {return key + '=' + encodeURIComponent(params[key])}).join('&')
}

function buildUrl(baseUrl, queries) {
    return baseUrl + '?' + buildQuery(queries)
}

function naverLogin() {
    params = {
        response_type: 'code',
        client_id: 'pPM3VjFMgEpE_fsUrjFd',
        redirect_uri: location.origin + '/user/login/social/naver/callback' + location.search,
        state: document.querySelector('[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://nid.naver.com/oauth2.0/authorize', params)
    location.replace(url)
}

function kakaoLogin(){
    Kakao.init('fd54fd347f0e7fb3d7da8df54c044e99');
    // 로그인 창을 띄웁니다.
    Kakao.Auth.login({
        success: function(authObj) {
            alert(JSON.stringify(authObj));
            alert('success');
            // 로그인 성공시, API를 호출합니다.
					Kakao.API.request({
						url: '/v1/user/me',
						success: function(res) {
							console.log(res);

							var userID = res.id;						//유저의 카카오톡 고유 id
							var userNickName = res.properties.nickname;	//유저가 등록한 별명

							console.log(userID);
							console.log(userNickName);
						},
						fail: function(error) {
							alert(JSON.stringify(error));
						}
					});
        },
        fail: function(errorObj) {
            alert(JSON.stringify(errorObj));
            alert('fail');
        }
    });
}

function checkLoginStatus() {
    var loginBtn = document.querySelector('#loginBtn');
    if(gauth.isSignedIn.get()) {
        loginBtn.value = 'Logout';
        window.profile = gauth.currentUser.get().getBasicProfile();
    } else {
         loginBtn.value = 'Login';
    }
}

function init() {
    gapi.load('auth2', function() {
        window.gauth = gapi.auth2.init({
            client_id: '442447136305-6l8ogrdbvnr20m29kh2claiejbpm94sa.apps.googleusercontent.com',
            ux_mode: 'redirect',
            redirect_uri: 'http://localhost:8000/user/login/social/google/callback'
        })
    gauth.then(function() {
        checkLoginStatus();
    }, function() {
        alert('googleAuth Fail');
        });
    });
}

function googleLogin() {
    gauth.signIn().then(function() {
        checkLoginStatus();
    });
    post_to_url();
}

function post_to_url() {
    method = "post"; // 전송 방식 기본값을 POST로

    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", location.origin + '/user/login/social/google/callback/' + location.search);
    //히든으로 값을 주입시킨다.
    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("name", 'id');
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("value", profile.getId());

    form.appendChild(hiddenField);

    var hiddenFieldForCsrf = document.createElement("input");
    hiddenFieldForCsrf.setAttribute("type", "hidden");
    hiddenFieldForCsrf.setAttribute("name", 'csrfmiddlewaretoken');
    hiddenFieldForCsrf.setAttribute("value", getCookie('csrftoken'));

    form.appendChild(hiddenFieldForCsrf);

    document.body.appendChild(form);
    form.submit();
}

function getCookie(name) {
    console.log('getCookie');
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log('cookie:' + cookieValue);
    return cookieValue;
}