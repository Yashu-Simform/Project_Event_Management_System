const myevents = document.getElementById('myevents')
const logoutbtn = document.getElementById('logoutbtn')

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