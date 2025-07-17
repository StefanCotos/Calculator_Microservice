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

async function callFactorial() {
    if (!/^\d+$/.test(current)) {
        alert("Trebuie să introduci un număr întreg!");
        return;
    }

    const n = parseInt(current);
    if (isNaN(n)) return alert("Introduceți un număr valid pentru factorial.");

    const response = await fetch('/api/factorial', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n: n })
    });

    const data = await response.json();
    current = data.result.toString();
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;

    loadHistory();
}

async function callFibonacci() {
    if (!/^\d+$/.test(current)) {
        alert("Trebuie să introduci un număr întreg!");
        return;
    }

    const n = parseInt(current);
    if (isNaN(n)) return alert("Introduceți un număr valid pentru fibonacci.");

    const response = await fetch('/api/fibonacci', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n: n })
    });

    const data = await response.json();
    current = data.result.toString();
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;

    loadHistory();
}

async function callPow() {
    const [base, exponent] = current.split("^").map(Number);
    if (isNaN(base) || isNaN(exponent)) {
        return alert("Introduceți expresia ca 'x^y' (ex: 2^3)");
    }

    const response = await fetch('/api/pow', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x: base, y: exponent })
    });

    const data = await response.json();
    current = data.result.toString();
    document.getElementById("screen").innerText = current;
    document.getElementById("expression").value = current;

    loadHistory();
}

async function loadHistory() {
    const response = await fetch("/history");
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
    const confirmare = confirm("Sigur vrei să ștergi tot istoricul?");
    if (!confirmare) return;

    await fetch("/history", { method: "DELETE" });
    loadHistory();
}


document.addEventListener("DOMContentLoaded", loadHistory);
