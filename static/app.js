async function search() {
    let q = document.getElementById("keyword").value;

    let res = await fetch(`/search?q=${q}`);
    let data = await res.json();

    render(data);
}

async function searchName() {
    let name = document.getElementById("name").value;

    let res = await fetch(`/search_name?name=${name}`);
    let data = await res.json();

    render(data);
}

function render(data) {
    let div = document.getElementById("results");
    div.innerHTML = "";

    if (!data || data.length === 0) {
        div.innerHTML = "<p>No results found</p>";
        return;
    }

    data.forEach(p => {
        div.innerHTML += `
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h3>${p.title || "No title"}</h3>
                <p><b>Authors:</b> ${p.authors || ""}</p>
                <p>${(p.abstract || "").substring(0, 300)}...</p>
                ${p.doi ? `<a href="https://doi.org/${p.doi}" target="_blank">View Paper</a>` : ""}
            </div>
        `;
    });
}