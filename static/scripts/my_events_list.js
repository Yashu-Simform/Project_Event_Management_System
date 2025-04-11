const vieweventbtns = document.getElementsByName('vieweventbtn')

vieweventbtns.forEach(viewbtn => {
    viewbtn.addEventListener('click', function (event) {
        // event.preventDefault();
    
            console.log(viewbtn)
            console.log(viewbtn.id)
        fetch(`http://127.0.0.1:8000/ems/event/${viewbtn.id}/retrive/`,{
            method: "GET",
        })
        .then(res => res.text())
        .then(data => {
            // HTML Response is coming!
            const parent = document.getElementById('main-content')
            const event_detail_card = document.getElementById('exampleModal');
            event_detail_card.innerHTML = data;
        })
    })
});


const updatebtns = document.getElementsByName('updateeventbtn')
console.log(updatebtns)

updatebtns.forEach(updbtn => {
    updbtn.addEventListener('click', function (event) {
        let event_id = updbtn.id
        event_id = event_id.slice(9, event_id.length)
        console.log(event_id)
        window.location.href = `http://127.0.0.1:8000/ems/event/${event_id}/update/`
    })
});


const deletebtns = document.getElementsByName('deleteeventbtn')
deletebtns.forEach(delbtn => {
    delbtn.addEventListener('click', function (event) {
        let event_id = delbtn.id
        event_id = event_id.slice(9, event_id.length)
        console.log(event_id)
        const confirmdelbody = document.getElementsByName('confirmdelbody');
        confirmdelbody[0].id = `${event_id}`;
    })
});

const confirmdelbtn = document.getElementById('confirmdelbtn')
    confirmdelbtn.addEventListener('click', function (event) {

        const confirmdelbody = document.getElementsByName('confirmdelbody');
        const event_id = confirmdelbody[0].id

        fetch(`http://127.0.0.1:8000/api/event/${event_id}/delete/`,{
            method: 'DELETE'
        })
        .then(res => {
            if (res.ok){
                console.log('Deleted Successfully!')
                window.location.href = "http://127.0.0.1:8000/ems/user/dashboard/myevents/";
            }else{
                return res.json();
            }
        })
        .then(data => console.log(data))
})

const invitebtns = document.getElementsByName('invitebtn')

invitebtns.forEach(invitebtn => {
    
});