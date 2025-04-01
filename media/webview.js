const vscode = acquireVsCodeApi();

document.getElementById('vsdist-form').addEventListener('submit', event => {
    event.preventDefault();
    const formData = {
        burnin: document.getElementById('burnin').value,
        parameters: document.getElementById('parameters').value.split(',').map(param => param.trim()),
        color: document.getElementById('color').value,
    };

    vscode.postMessage({ command: 'submit', data: formData });
});

window.addEventListener('message', event => {
    const message = event.data;
    switch (message.command) {
        case 'displayImage':
            const img = document.createElement('img');
            img.src = 'data:image/png;base64,' + message.image;
            img.style.maxWidth = '100%';
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = "";
            resultDiv.appendChild(img);
            break;
    }
});
