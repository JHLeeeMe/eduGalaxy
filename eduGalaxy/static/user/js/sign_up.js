function Change_Email(){

    var form = document.Signup_Form;        // 폼 저장
    var target = document.getElementById("select");
    var sel = target.options[target.selectedIndex].value;
    var dis = 0;
    var readonly = 1;

    if(sel=="direct"){
        sel = "";
        readonly = 0;
    }

    if(sel=="select"){
        sel = "";
    }

    // 값과 활성화 여부 컨트롤
    form.email2.value = sel;
    form.email2.disabled = dis;
    form.email2.readonly = readonly;
}

// document.getElementById(아이디) : 해당 아이디의 요소를 선택함.
// options[아이디.selectedIndex].text : select 박스 옵션에 맞는 텍스트
// options[아이디.selectedIndex].value : 옵션에 맞는 값

var cnt = 6
function addField() {
    if (cnt > 0) {
        var items = document.createElement('p');
        items.innerHTML = document.getElementById('p_graduation').innerHTML;
        document.getElementById('div_graduation').appendChild(items);
        cnt -= 1
    } else {
        alert('더는 추가할 수 없습니다.')
    }
}

function removeField(obj) {
    if (cnt < 6) {
        document.getElementById('div_graduation').removeChild(obj.parentNode);
        cnt += 1
    }
}

function address_search() {
    new daum.Postcode({
        oncomplete: function(data) {
            var addr = ''; // 주소 변수
            //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
            if (data.userSelectedType === 'R') { // 사용자가 도로명 주소를 선택했을 경우
                addr = data.roadAddress;
            } else { // 사용자가 지번 주소를 선택했을 경우(J)
                addr = data.jibunAddress;
            }
            document.getElementById("address1").value = addr;
            // 커서를 상세주소 필드로 이동한다.
            document.getElementById("address2").focus();
        }
    }).open();
}