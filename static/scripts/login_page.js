import {get_cookie_dict} from "./utils";

main();


function main() {
    login();
}

function login() {
    console.log('Logging ...')
    const loginbtn = document.getElementById('loginbtn')

    if (loginbtn){
        loginbtn.addEventListener('click', async function (event) {
            event.preventDefault();

            let csrf_token = document.getElementsByName('csrfmiddlewaretoken')
            console.log(csrf_token)

            let username_field = document.getElementsByName('username')
            console.log(username_field)

            let pass_field = document.getElementsByName('password')
            console.log(pass_field.value)

            const data_body = {"csrfmiddlewaretoken": csrf_token[0].value.toString(), "username": username_field[0].value.toString(), "password": pass_field[0].value.toString()}

            await submitForm("http://127.0.0.1:8000/api/user/api/token/", data_body);
            console.log('Loggedin.')
        })
    }
}


async function submitForm(p_url, p_body){
    console.log(p_url)
    fetch(p_url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username: p_body['username'], password: p_body['password']})
    })
    .then(response => response.json())
    .then(
        data => {
            if (data){
            console.log(data)
            if (data['status']){
                const cookie_dict = get_cookie_dict(document.cookie)
                if (!cookie_dict['token']){
                    document.cookie = `token=${data['data']['token']}; path=/;`
                }
            }
            }
            else{
                console.log('No response received!')
            }
        }
    )
    .catch(error => console.error('Error:', error));
}