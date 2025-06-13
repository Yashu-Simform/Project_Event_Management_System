// import { URL_PUBLIC_EVENTS_LIST } from "./urls";
// import {get_cookie_dict} from "./utils";


console.log('Login Script Loaded!')
const loginbtn = document.getElementById('loginbtn')

main();


function main() {
    login();
}

function get_cookie_dict(cookie_str) {
    let cookie_dict = {}
    let all_cookies = document.cookie.split(';')
    all_cookies.forEach(element => {
        let key_value = element.trim().split('=')
        cookie_dict[key_value[0]] = key_value[1]
    });

    return cookie_dict
}

async function getUserInputCredentials(){
    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')
    console.log(csrf_token.value)

    let username_field = document.getElementsByName('username')
    console.log(username_field.value)

    let pass_field = document.getElementsByName('password')
    console.log(pass_field.value)

    p_body = {
        username: username_field.value,
        password: pass_field.value
    }

    return p_body
}

async function login() {
    console.log('Logging ...')
    const loginbtn = document.getElementById('loginbtn')

    if (loginbtn){
        loginbtn.addEventListener('click', async function (event) {
            event.preventDefault();

            let csrf_token = document.getElementsByName('csrfmiddlewaretoken')

            let email_field = document.getElementsByName('email')

            let pass_field = document.getElementsByName('password')

            const data_body = {"csrfmiddlewaretoken": csrf_token[0].value.toString(), "email": email_field[0].value.toString(), "password": pass_field[0].value.toString()}

            const cookie_dict = get_cookie_dict(document.cookie)

            await getAuthJWT("http://127.0.0.1:8000/api/user/login/", data_body, cookie_dict);
            console.log('You are now loggedin.')
        })
    }
    else{
        console.log('No loginbtn found.')
    }
}

async function getAuthJWT(p_url, p_body, cookie_dict) {
    fetch(p_url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({email: p_body['email'], password: p_body['password']})
    })
    .then(
        response => {
            if (!response.ok){
                alert('Invalid Credentials!');
            }else{
                return response.json();
            }
            
        },
        response => console.log(response)
    )
    .then(data => {
        console.log(data)
        if(data['data']['id']){
            document.cookie = `user_id=${data['data']['id']}; path=/; domain=127.0.0.1;`
            document.location.href = 'http://127.0.0.1:8000/ems/user/otp-verify/';
        }
        
    })
}
