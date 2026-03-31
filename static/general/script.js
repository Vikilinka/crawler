const get = async (params) => {
    let response = await fetch(`${window.location.pathname}?${new URLSearchParams(params)}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json;charset=utf-8',
        }
    });
    return await response.json();
}

const post = async (data) => {
    let response = await fetch(window.location.pathname, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify(data),
    })
    return await response.json();
}
