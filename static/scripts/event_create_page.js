console.log('Event Creation Script Init...')
main();

function get_cookie_dict(cookie_str) {
    let cookie_dict = {}
    let all_cookies = document.cookie.split(';')
    all_cookies.forEach(element => {
        let key_value = element.trim().split('=')
        cookie_dict[key_value[0]] = key_value[1]
    });

    return cookie_dict
}


function main(){
    const eventform = document.getElementById('eventform')
    eventform.addEventListener('submit', function (event) {
        event.preventDefault();
        console.log(event)

        const cookie_dict = get_cookie_dict(document.cookie)

        let formData = new FormData(event.target)

        let object = {}

        formData.forEach((value, key) => {
            object[key] = value;
        });

        console.log(object)

        let l_body = JSON.stringify(object);
        console.log(l_body)

        fetch(event.target.action,{
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${cookie_dict['access']}`,
                'Content-Type': 'application/json',
            },
            body: l_body
        })
        .then((response) => {
            if (!response.ok){
                if (response.status == 429){
                    alert('You have reached the limit of requests allowed!')
                }else{
                    throw new Error(`Error occured with status code: ${response.status}`);
                }
                
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            alert(data['data']);
            window.location.href = 'http://127.0.0.1:8000/ems/user/dashboard/';
        })
        .then(error => console.log(error))
    })
}

function createEvent(){
    fetch(p_url,{
        method: 'POST',
        headers:{
            // 
        },
    })
}