let ws;

function startResearch() {
    const progressDiv = document.getElementById("progress");
    const clusterSelectionDiv = document.getElementById("cluster-selection");

    // Clear previous progress messages and reset UI elements
    progressDiv.innerHTML = "";  
    clusterSelectionDiv.style.display = "none";  

    // Open WebSocket connection
    ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = function(event) {
        const message = event.data;

        // Show cluster input only for manual selection prompt
        if (message.includes("Please review the options and select the correct cluster")) {
            clusterSelectionDiv.style.display = "flex"; 
        }

        // Create a new message element and add it to the progress section
        const messageElement = document.createElement("p");
        messageElement.innerText = message;
        progressDiv.appendChild(messageElement);

        // Auto-scroll to the latest message
        progressDiv.scrollTop = progressDiv.scrollHeight;
    };

    ws.onopen = function() {
        const companyName = document.getElementById("companyName").value;
        const companyUrl = document.getElementById("companyUrl").value;
        const outputFormat = document.getElementById("outputFormat").value;
        ws.send(JSON.stringify({ companyName, companyUrl, outputFormat }));
    };

    ws.onclose = function() {
        const message = document.createElement("p");
        message.innerText = "Process Finished";
        progressDiv.appendChild(message);

        // Ensure auto-scroll on close message
        progressDiv.scrollTop = progressDiv.scrollHeight;
    };

    ws.onerror = function(error) {
        console.error("WebSocket error:", error);
    };
}

function submitClusterSelection() {
    const clusterSelection = document.getElementById("cluster-input").value;
    ws.send(clusterSelection);
    document.getElementById("cluster-selection").style.display = "none";  
}
