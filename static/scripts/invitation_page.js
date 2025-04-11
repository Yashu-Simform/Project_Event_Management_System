const sendInviteBtn = document.getElementById('sendInviteBtn')

function get_cookie_dict(cookie_str) {
    let cookie_dict = {}
    let all_cookies = document.cookie.split(';')
    all_cookies.forEach(element => {
        let key_value = element.trim().split('=')
        cookie_dict[key_value[0]] = key_value[1]
    });

    return cookie_dict
}


sendInviteBtn.addEventListener('click', function (event) {
    event.preventDefault();

    const email = document.getElementById('participantEmail')
    console.log(email.value)
    const event_id = document.getElementById('id_events')
    console.log(event_id.value)

    const cookie_dict = get_cookie_dict(document.cookie)

    if (email.value != null){
        fetch(`http://127.0.0.1:8000/api/invite/${event_id.value}/save/`,{
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${cookie_dict['access']}`,
                'Content-Type': 'application/json',
            },
            body:{
                'email': email,
                // 'event_id': 
            }
        })
        .then(res => {
            if (res.ok){
                console.log('Invite sent successfully!');
                return res.json();
            }
            return res.json()
        })
        .then(data => {
            console.log(data);
        })
    }
})