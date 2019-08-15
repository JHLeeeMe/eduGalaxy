function buildQuery(params) {
    console.log('buildQuery()');
    return Object.keys(params).map(function (key) {return key + '=' + encodeURIComponent(params[key])}).join('&')
}

function buildUrl(baseUrl, queries) {
    console.log('buildUrl()');
    return baseUrl + '?' + buildQuery(queries)
}

function naverLogin() {
    console.log('naverLogin()');
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
    console.log('kakaoLogin()');
    provider = 'kakao'

    Kakao.init('fd54fd347f0e7fb3d7da8df54c044e99');
    // 로그인 창을 띄웁니다.
    Kakao.Auth.login({
        success: function(authObj) {
            console.log(JSON.stringify(authObj));
            // 로그인 성공시, API를 호출합니다.
            Kakao.API.  request({
                url: '/v1/user/me',
                success: function(res) {
                    window.userID = res.id;						//유저의 카카오톡 고유 id
                    window.userNickName = res.properties.nickname;	//유저가 등록한 별명

                    post_to_url(); // Id 값과 nickname 값을 백엔드로 input 태그를 이용해 보냄
                },
                fail: function(error) {
                    alert(JSON.stringify(error));
                }
            });
        },
        fail: function(errorObj) {
            alert(JSON.stringify(errorObj));
            alert('Login failed');
        }
    });
}

function checkLoginStatus() {
    console.log('checkLoginStatus()');
    if(gauth.isSignedIn.get()) {
//        window.profile = gauth.currentUser.get().getBasicProfile();
        window.profile = gauth.currentUser.get();
        console.log(profile.getId())
    } else {
        console.log('is not SignedIn');
    }
}

function init() {
    console.log('init()');
    gapi.load('auth2', function() {
        console.log('gapi.load()');
        window.gauth = gapi.auth2.init({
            client_id: '442447136305-6l8ogrdbvnr20m29kh2claiejbpm94sa.apps.googleusercontent.com',
//            ux_mode: 'redirect',
            redirect_uri: 'http://localhost:8000/user/login/social/google/callback',
            fetch_basic_profile: false,
            scope: 'profile'
        })
    gauth.then(function() {
        checkLoginStatus();
    }, function() {
        alert('googleAuth Fail');
    });
    });
}

function googleLogin() {
    console.log('googleLogin()');
    window.provider = 'google'
    gauth.signIn().then(function() {
        checkLoginStatus();
        if (profile.getId() != null) {
            post_to_url();
        } else {
            alert('login failed')
        }
    });
}

function post_to_url() {
    console.log('post_to_url()');
    method = "post"; // 전송 방식 기본값을 POST로

    if (provider == 'google') {
        console.log('provider = ' + provider)
        inputHiddenForm();
        form.setAttribute("action", location.origin + '/user/login/social/google/callback/' + location.search);
        hiddenField.setAttribute("value", profile.getId());

    } else if (provider == 'kakao') {
        inputHiddenForm();
        form.setAttribute("action", location.origin + '/user/login/social/kakao/callback/' + location.search);
        hiddenField.setAttribute("value", userID);
    } else {
        console.log('provider is null')
    }
    form.appendChild(hiddenField);
    form.appendChild(hiddenFieldForCsrf);
    document.body.appendChild(form);
    form.submit();

    function inputHiddenForm() {
        console.log('inputHiddenForm()');
        window.form = document.createElement("form");
        form.setAttribute("method", method);

        //히든으로 값을 주입시킨다.
        window.hiddenField = document.createElement("input");
        hiddenField.setAttribute("name", 'id');
        hiddenField.setAttribute("type", "hidden");

        window.hiddenFieldForCsrf = document.createElement("input");
        hiddenFieldForCsrf.setAttribute("type", "hidden");
        hiddenFieldForCsrf.setAttribute("name", 'csrfmiddlewaretoken');
        hiddenFieldForCsrf.setAttribute("value", getCookie('csrftoken'));
    }
}

function getCookie(name) {
    console.log('getCookie()');
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
    return cookieValue;
}