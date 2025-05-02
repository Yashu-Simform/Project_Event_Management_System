const myevents = document.getElementById('myevents')
const invitations = document.getElementById('invitations')
const logoutbtn = document.getElementById('logoutbtn')

function get_cookie_dict(cookie_str) {
    let cookie_dict = {}
    let all_cookies = document.cookie.split(';')
    all_cookies.forEach(element => {
        let key_value = element.trim().split('=')
        cookie_dict[key_value[0]] = key_value[1]
    });

    return cookie_dict
}

myevents.addEventListener('click', function (event) {
    event.preventDefault();
    console.log('my events called!')
    fetch('http://127.0.0.1:8000/ems/user/dashboard/myevents/', {
        method: 'GET',
    })
    .then(response => {
        if (response.ok){
            window.location.href = "http://127.0.0.1:8000/ems/user/dashboard/myevents/";
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
});

invitations.addEventListener('click', function (event) {
    event.preventDefault();
    console.log('Invitations button called!');
    fetch('http://127.0.0.1:8000/ems/user/dashboard/invitations/', {
        method: 'GET',
    })
    .then(response => {
        if (response.ok){
            window.location.href = "http://127.0.0.1:8000/ems/user/dashboard/invitations/";
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
});

logoutbtn.addEventListener('click', function (event) {
    event.preventDefault();
    console.log('Logout button clicked!')

    fetch('http://127.0.0.1:8000/ems/user/logout/',{
        method: "GET",
    })
    .then(response => {
        if (response.ok){
            window.location.href = "http://127.0.0.1:8000/ems/"
        }
        return response.json()
    })
    .then(data => {
        console.log(data)
    })
})

try {
    const participateBtns = document.getElementsByName('participateBtn')

    const cookie_dict = get_cookie_dict(document.cookie)

    participateBtns.forEach(participateBtn => {
        participateBtn.addEventListener('click',function (event) {
            event.preventDefault();
    
            if (cookie_dict['access'] == undefined || (('access' in cookie_dict) == false)) {
                window.location.href = 'http://127.0.0.1:8000/ems/user/login/'
            }else{
                data = {
                    event_id: participateBtn.id,
                    sent_to: participateBtn.dataset.host,
                }

                console.log(data)
    
                fetch('http://127.0.0.1:8000/api/invite/participate-request/',{
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${cookie_dict['access']}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        event_id: participateBtn.id,
                        sent_to: participateBtn.dataset.host,
                    })
                })
                .then(res => {
                    if (! res.ok){
                        alert('Erro occured in sending the participation request!');
                    }
                    return res.json();
                })
                .then(
                    data => {
                        console.log(data);
                        alert(data['data']);
                        window.location.reload();
                    }
                )
            }
        })
    });

    
} catch (error) {
    
}