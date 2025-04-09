const vieweventbtn = document.getElementById('vieweventbtn')

vieweventbtn.addEventListener('click', function (event) {
    event.preventDefault();

    fetch(`http://127.0.0.1:8000/ems/event/${vieweventbtn[0].value}/retrive/`,{
        method: "GET",
    })
    .then(res => res.text())
    .then(data => {
        // HTML Response is coming!
        const event_detail = document.getElementById('event-detail')
        event_detail.innerHTML = data
    })
})