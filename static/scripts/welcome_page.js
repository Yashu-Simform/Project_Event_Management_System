main();

function main() {
    const welcome_btn = document.getElementById('welcome-btn')

    welcome_btn.addEventListener('click', function () {
        //Welcome btn clicked
        console.log('Welcome Btn clicked!')

        //Check user authentication
        const cookie_dict = get_cookie_dict(document.cookie)

        // if (!cookie_dict['access'] || !cookie_dict['refresh']){
        //     window.location.href = 'http://127.0.0.1:8000/ems/user/login/'
        // }else{

        // }

        fetch('http://127.0.0.1:8000/ems/user/dashboard/',{
            method: 'GET',
            headers: {
                'Authentication': `Bearer ${cookie_dict['access']}`
            }
        })
        .then(response => {
            console.log(response)
            console.log('Authenticated!')
            return response.text()
        })
        .then(
            data => {
                window.location.href = 'http://127.0.0.1:8000/ems/user/dashboard/'
            // document.open()
            // document.write(data)
            // document.close()
            // window.location.replace()
            }
        )
    })
}