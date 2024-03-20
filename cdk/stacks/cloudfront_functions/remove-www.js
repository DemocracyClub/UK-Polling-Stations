async function handler(event) {
    const request = event.request;
    const headers = request.headers;
    let host = headers.host;
    if (host === undefined) {
        host = "";
    } else {
        host = host.value
    }


    if (host.startsWith('www.')) {
        const new_url = 'https://' + host.substring(4) + request.uri
        return {
            statusCode: 301,
            statusDescription: 'Moved Permanently',
            headers:
                {"location": {"value": new_url}}
        };

    }
    return request;
}
