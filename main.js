var history = [];
const API_URL = 'http://localhost:8000';

function reload() {
    fetch(`${API_URL}/reload`, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    }).then(response => response.json())
    .then(data => {
        var chatbox = document.getElementById('chatbox');
        chatbox.innerHTML = '';
        history = [];
        chatbox.innerHTML += '<div><div class="ai-message">AI: ' + data.response + '</div></div>';
        history.push({role: 'system', content: data.response});
    });
}

function chat() {
    var query = document.getElementById('query').value;
    var chatbox = document.getElementById('chatbox'); 
    chatbox.innerHTML += '<div><div class="user-message">You: ' + query + '</div></div>';

    fetch(`${API_URL}/chat`, {
        method: 'POST',
        body: JSON.stringify({query: query, history: history}),
        headers: {'Content-Type': 'application/json'}
    }).then(response => response.json())
    .then(data => { 
        chatbox.innerHTML += '<div><div class="ai-message">AI: ' + data.response + '</div></div>'; 
        chatbox.scrollTop = chatbox.scrollHeight; 
        history.push({role: 'system', content: data.response}); 
        history.push({role: 'user', content: query}); 
        document.getElementById('query').value = ''; 
    });
}

