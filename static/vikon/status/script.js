let params = new URLSearchParams(document.location.search);
let id = params.get("id");
if (id) {
    const socket = new WebSocket(`ws://${location.host}:8000/vikon/trace/status/${id}`);
    socket.addEventListener("message", (event) => {
        let window = document.querySelector('.mystery__window');
        let visualization = '';
        visualization += '<div>';
        for (const [key, value] of Object.entries(JSON.parse(event.data))) {
            visualization += `<div>${key}: ${value}</div>`;
        }
        visualization += '</div>';
        window.innerHTML = visualization;
    });
}
