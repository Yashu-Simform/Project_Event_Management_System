main();

function main() {
    welcome_btn_fun();
}

function welcome_btn_fun(){
    const welcome_btn = document.getElementById('welcome-btn')

    welcome_btn.addEventListener('click', function () {
        //Welcome btn clicked
        console.log('Welcome Btn clicked!')
    })
}