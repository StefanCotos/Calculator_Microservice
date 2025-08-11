let current = "";

function append(val) {
    current += val;
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;
}

function clearScreen() {
    current = "";
    document.getElementById("screen").innerText = "";
    document.getElementById("expression").value = "";
}

function backspace() {
    current = current.slice(0, -1);
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;
}

function getAuthHeaders() {
    const token = localStorage.getItem("jwt_token");
    return token ? { "Authorization": "Bearer " + token } : {};
}

async function callFactorial() {
    if (!/^\d+$/.test(current)) {
        alert("You must enter an integer!");
        return;
    }

    const n = parseInt(current);
    if (isNaN(n)) return alert("Please enter a valid number for factorial.");

    const response = await fetch('/api/factorial', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ n: n })
    });

    if (response.status === 401) {
        alert("You must be authenticated!");
        return;
    }

    const data = await response.json();
    current = data.result.toString();
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;

    loadHistory();
}

async function callFibonacci() {
    if (!/^\d+$/.test(current)) {
        alert("You must enter an integer!");
        return;
    }

    const n = parseInt(current);
    if (isNaN(n)) return alert("Please enter a valid number for fibonacci.");

    const response = await fetch('/api/fibonacci', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ n: n })
    });

    if (response.status === 401) {
        alert("You must be authenticated!");
        return;
    }

    const data = await response.json();
    current = data.result.toString();
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;

    loadHistory();
}

async function callPow() {
    const [base, exponent] = current.split("^").map(Number);
    if (isNaN(base) || isNaN(exponent)) {
        return alert("Enter the expression as 'x^y' (e.g., 2^3)");
    }

    const response = await fetch('/api/pow', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify({ x: base, y: exponent })
    });

    if (response.status === 401) {
        alert("You must be authenticated!");
        return;
    }

    const data = await response.json();
    current = data.result.toString();
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;

    loadHistory();
}

async function loadHistory() {
    const response = await fetch("/history", {
        headers: { ...getAuthHeaders() }
    });
    const data = await response.json();

    const list = document.getElementById("history-list");
    list.innerHTML = "";

    data.forEach(entry => {
        const li = document.createElement("li");
        li.textContent = `${entry.expression} = ${entry.result}`;
        list.appendChild(li);
    });
}

async function deleteHistory() {
    const confirmare = confirm("Are you sure you want to delete all history?");
    if (!confirmare) return;

    await fetch("/history", { method: "DELETE", headers: { ...getAuthHeaders() } });
    loadHistory();
}

function setupLogout() {
    document.querySelectorAll('a[href="/logout"]').forEach(function (link) {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            localStorage.removeItem("jwt_token");
            window.location.href = "/";
        });
    });
}

async function showUserBar() {
    const token = localStorage.getItem("jwt_token");
    const authBar = document.querySelector(".auth-bar");
    if (!authBar) return;
    if (!token) {
        authBar.innerHTML = `<a href="/login" class="button" type="button">Login</a>
                             <a href="/register" class="button" type="button">Register</a>`;
        setupLogout();
        return;
    }
    const response = await fetch("/me", { headers: { "Authorization": "Bearer " + token } });
    if (response.ok) {
        const data = await response.json();
        authBar.innerHTML = `Hello, ${data.username} <a href="/logout" class="button" type="button">Logout</a>`;
    } else {
        authBar.innerHTML = `<a href="/login" class="button" type="button">Login</a>
                             <a href="/register" class="button" type="button">Register</a>`;
    }
    setupLogout();
}

document.addEventListener("DOMContentLoaded", function () {
    loadHistory();
    showUserBar();

    const calcForm = document.getElementById("calc-form");
    if (calcForm) {
        calcForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const expression = document.getElementById("expression").value;

            const response = await fetch("/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    ...getAuthHeaders()
                },
                body: "expression=" + encodeURIComponent(expression)
            });

            const html = await response.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newScreen = doc.getElementById("screen");
            const result = newScreen ? newScreen.innerText : "";

            document.getElementById("screen").innerText = result;

            loadHistory();
            showUserBar();
        });
    }

    const exportBtn = document.getElementById("export-btn");
    if (exportBtn) {
        exportBtn.addEventListener("click", async function () {
            const response = await fetch("/history/export", {
                headers: { ...getAuthHeaders() }
            });
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);

                const a = document.createElement("a");
                a.href = url;
                a.download = "history.csv";
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            } else {
                alert("Could not download history.");
            }
        });
    }
});

