function renderKeywordResults(data) {
    const resultsDiv = document.getElementById("results");

    if (!data || data.length === 0) {
        resultsDiv.innerHTML = "<p>No matching publications found.</p>";
        return;
    }

    let html = "<h2>Keyword Search Results</h2>";

    data.forEach(item => {
        html += `
            <div style="border:1px solid #ccc; padding:15px; margin:15px 0; border-radius:8px;">
                <h3>${item.title || "No title"}</h3>
                <p><strong>Authors:</strong> ${item.authors || "N/A"}</p>
                <p><strong>Journal:</strong> ${item.journal || "N/A"}</p>
                <p><strong>Abstract:</strong> ${(item.abstract || "").substring(0, 400)}...</p>
                ${item.doi ? `<p><a href="https://doi.org/${item.doi}" target="_blank">View DOI</a></p>` : ""}
            </div>
        `;
    });

    resultsDiv.innerHTML = html;
}

function renderNameResults(data) {
    const resultsDiv = document.getElementById("results");

    if (data.error) {
        resultsDiv.innerHTML = `<p>${data.error}</p>`;
        return;
    }

    let html = `
        <h2>Researcher Search Result</h2>
        <p><strong>Name:</strong> ${data.name || "N/A"}</p>
        <p><strong>ORCID:</strong> ${data.orcid || "N/A"}</p>
        <p><strong>PI_ID:</strong> ${data.pi_id || "N/A"}</p>
    `;

    if (!data.publications || data.publications.length === 0) {
        html += "<p>No publications found for this researcher.</p>";
        resultsDiv.innerHTML = html;
        return;
    }

    html += "<h3>Publications</h3>";

    data.publications.forEach(item => {
        html += `
            <div style="border:1px solid #ccc; padding:15px; margin:15px 0; border-radius:8px;">
                <h4>${item.title || "No title"}</h4>
                <p><strong>Authors:</strong> ${item.authors || "N/A"}</p>
                <p><strong>Journal:</strong> ${item.journal || "N/A"}</p>
                <p><strong>Abstract:</strong> ${(item.abstract || "").substring(0, 400)}...</p>
                ${item.doi ? `<p><a href="https://doi.org/${item.doi}" target="_blank">View DOI</a></p>` : ""}
            </div>
        `;
    });

    resultsDiv.innerHTML = html;
}

function search() {
    let q = document.getElementById("searchBox").value;

    fetch(`/search?q=${encodeURIComponent(q)}`)
        .then(res => res.json())
        .then(data => renderKeywordResults(data))
        .catch(err => {
            document.getElementById("results").innerHTML = "Search error: " + err;
        });
}

function searchName() {
    let name = document.getElementById("nameBox").value;

    fetch(`/search_name?name=${encodeURIComponent(name)}`)
        .then(res => res.json())
        .then(data => renderNameResults(data))
        .catch(err => {
            document.getElementById("results").innerHTML = "Search Name error: " + err;
        });
}