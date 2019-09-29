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

function addField() {
    var items = document.createElement('p');
    items.innerHTML = document.getElementById('p_graduation').innerHTML;
    document.getElementById('div_graduation').appendChild(items);
}

function removeField(obj) {
    document.getElementById('div_graduation').removeChild(obj.parentNode);
}
