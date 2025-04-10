const updatebtn = document.getElementById('updatebtn');
const eventupdateform = document.getElementById('eventupdateform');

eventupdateform.addEventListener('submit', function (event) {
    event.preventDefault();

    // console.log(document.URL)
    const curr_page_url = document.URL

    const path = curr_page_url.split('/')

    const event_id = path[path.length - 3]
    // console.log(event_id)

    const cookie_dict = get_cookie_dict(document.cookie)

    let formData = new FormData(event.target)

    let object = {}

    formData.forEach((value, key) => {
        object[key] = value;
    });

    console.log(object)

    let l_body = JSON.stringify(object);
    console.log(l_body)


    fetch(`http://127.0.0.1:8000/api/event/${event_id}/update/`,{
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${cookie_dict['access']}`,
            'Content-Type': 'application/json',
        },
        body: l_body
    })
    .then(res => {
        if (res.ok){
            console.log('Updated Successfully!')
            window.location.href = "http://127.0.0.1:8000/ems/user/dashboard/myevents/";
        }else
        {return res.json();}
    })
    .then(data => console.log(data))
})