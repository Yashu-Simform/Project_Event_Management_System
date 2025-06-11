const registrationForm = document.getElementById('registrationForm')

registrationForm.addEventListener('submit', function (event) {
    event.preventDefault();
    
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
            'Content-Type': 'application/json',
        },
        body: l_body
    })
    .then((res) => res.json(), (reason) => {console.log(reason)})
    .then(data => {
        console.log(data)
        if(data['success']){
            if (data['data']){
                document.cookie = `access=${data['data']['access']}; path=/;`
                document.cookie = `refresh=${data['data']['refresh']}; path=/;`
                alert('Registration Successfully!');
                document.location.href = 'http://127.0.0.1:8000/ems/user/dashboard/';
            }else{
                console.log('No response data!')
            }
        }
        else{
            console.log(data['error'])
        }
    })
});