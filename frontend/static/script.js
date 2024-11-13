let ws;

function startResearch() {
    const progressDiv = document.getElementById("progress");
    const clusterSelectionDiv = document.getElementById("cluster-selection");
    const reportDiv = document.getElementById("report");

    // Clear previous content
    progressDiv.innerHTML = "";
    reportDiv.innerHTML = "";
    clusterSelectionDiv.style.display = "none";

    // Open WebSocket connection
    ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = function(event) {
        const message = event.data;

        if (message.includes("Please review the options and select the correct cluster")) {
            clusterSelectionDiv.style.display = "block";
        }

        // Handle final report differently
        if (message.startsWith("Generated Report:")) {
            // Add just "Generated Report" to progress
            const messageElement = document.createElement("div");
            messageElement.className = "progress-message";
            messageElement.textContent = "Generated Report";
            progressDiv.appendChild(messageElement);
            
            // Add full report content to report section
            reportDiv.innerText = message.replace("Generated Report:", "").trim();
            requestAnimationFrame(() => {
                reportDiv.scrollTop = reportDiv.scrollHeight;
            });
        } else {
            // Create message element with specific styling for all other messages
            const messageElement = document.createElement("div");
            messageElement.className = "progress-message";
            messageElement.textContent = message;
            progressDiv.appendChild(messageElement);
        }

        // Ensure automatic scrolling to the latest message
        requestAnimationFrame(() => {
            progressDiv.scrollTop = progressDiv.scrollHeight;
        });
    };

    ws.onopen = function() {
        const companyName = document.getElementById("companyName").value;
        const companyUrl = document.getElementById("companyUrl").value;
        const outputFormat = document.getElementById("outputFormat").value;
        ws.send(JSON.stringify({ companyName, companyUrl, outputFormat }));
    };

    // ws.onclose = function() {
    //     const messageElement = document.createElement("div");
    //     messageElement.className = "progress-message";
    //     messageElement.textContent = "Process Finished";
    //     progressDiv.appendChild(messageElement);
    //     progressDiv.scrollTop = progressDiv.scrollHeight;
    // };

    ws.onerror = function(error) {
        const messageElement = document.createElement("div");
        messageElement.className = "progress-message";
        messageElement.textContent = "Error: " + error.message;
        messageElement.style.borderLeftColor = "#FE363B"; // Red border for errors
        progressDiv.appendChild(messageElement);
        progressDiv.scrollTop = progressDiv.scrollHeight;
    };
}

function submitClusterSelection() {
    const clusterSelection = document.getElementById("cluster-input").value;
    if (ws && clusterSelection) {
        ws.send(clusterSelection);
        document.getElementById("cluster-selection").style.display = "none";
        document.getElementById("cluster-input").value = "";
    }
}