function get_cookie_dict(cookie_str) {
    let cookie_dict = {}
    let all_cookies = document.cookie.split(';')
    all_cookies.forEach(element => {
        let key_value = element.trim().split('=')
        cookie_dict[key_value[0]] = key_value[1]
    });

    return cookie_dict
}

document.getElementById("verify-otp-btn").addEventListener("click", function() {
    let otp = document.getElementById("otp-input").value;
    let messageBox = document.getElementById("message");
    const cookie_dict = get_cookie_dict(document.cookie)

    if (otp.length === 6 && /^\d+$/.test(otp)) {
        fetch(
            'http://127.0.0.1:8000/api/user/otp-verify/',
            {method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({raw_otp: otp, id: cookie_dict['user_id']})}
        )
        .then(response => response.json())
        .then(
            data=>{
                if (data){
                    document.cookie = `access=${data['data']['access']}; path=/; domain=127.0.0.1;`
                    document.cookie = `refresh=${data['data']['refresh']}; path=/; domain=127.0.0.1;`
                }
                window.location.href = "http://127.0.0.1:8000/ems/user/dashboard"; // Modify as needed
            }
        )
    } else {
        messageBox.style.display = "block";
    }
});