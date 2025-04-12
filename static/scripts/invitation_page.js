const sendInviteBtn = document.getElementById('sendInviteBtn')
const inviteForm = document.getElementById('inviteform')

function get_cookie_dict(cookie_str) {
    let cookie_dict = {}
    let all_cookies = document.cookie.split(';')
    all_cookies.forEach(element => {
        let key_value = element.trim().split('=')
        cookie_dict[key_value[0]] = key_value[1]
    });

    return cookie_dict
}


inviteForm.addEventListener('submit', function (event) {
    event.preventDefault();

    // const email = document.getElementById('participantEmail')
    // console.log(email.value)
    // const event_id = document.getElementById('id_events')
    // console.log(event_id)

    let formData = new FormData(event.target)

    let object = {}

    formData.forEach((value, key) => {
        object[key] = value;
    });

    let l_body = JSON.stringify(object);
    console.log(l_body)

    const cookie_dict = get_cookie_dict(document.cookie)

    fetch(`http://127.0.0.1:8000/api/invite/save/`,{
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${cookie_dict['access']}`,
            'Content-Type': 'application/json',
        },
        body: l_body
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
})