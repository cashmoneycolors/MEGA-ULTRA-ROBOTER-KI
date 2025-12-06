// app.js

const state = {
  user: null,
  products: [
    { id: 1, name: "Strategieberatung", description: "Analyse und Roadmap für Wachstum.", icon: "??", price: 199 },
    { id: 2, name: "Software-Entwicklung", description: "Digitale Lösungen für Unternehmen.", icon: "??", price: 499 },
    { id: 3, name: "Cloud-Migration", description: "Effizienter Umzug Ihrer Infrastruktur.", icon: "??", price: 299 },
    { id: 4, name: "Cyber Security", description: "Schutz vor Bedrohungen.", icon: "??", price: 399 }
  ],
  metrics: { umsatz: "€ 129.870", kunden: 51, leads: 9 }
};

function renderLogin() {
  document.getElementById('app').innerHTML = `
    <h2>Login</h2>
    <input id="username" placeholder="Benutzername"><br>
    <input id="password" type="password" placeholder="Passwort"><br>
    <button onclick="login()">Anmelden</button>
  `;
}

function login() {
  const u = document.getElementById('username').value;
  const p = document.getElementById('password').value;
  if (u === "mitarbeiter" && p === "pass123") {
    state.user = u;
    renderDashboard();
  } else {
    alert("Benutzername oder Passwort falsch.");
  }
}

function renderDashboard() {
  document.getElementById('app').innerHTML = `
    <h2>Dashboard</h2>
    <div>Umsatz (Monat): <b>${state.metrics.umsatz}</b></div>
    <div>Neue Kunden: <b>${state.metrics.kunden}</b></div>
    <div>Offene Leads: <b>${state.metrics.leads}</b></div>
    <button onclick="renderProducts()">Katalog</button>
    <button onclick="renderContact()">Kontakt</button>
    <button onclick="logout()">Logout</button>
  `;
}

function renderProducts() {
  document.getElementById('app').innerHTML = `
    <h2>Katalog</h2>
    <ul>
      ${state.products.map(p => `
        <li>
          <span style="font-size:2em">${p.icon}</span>
          <b>${p.name}</b> - ${p.price}€
          <button onclick="renderProductDetail(${p.id})">Details</button>
          <button onclick="buyProduct(${p.id})">Kaufen</button>
        </li>
      `).join('')}
    </ul>
    <button onclick="renderDashboard()">Zurück</button>
  `;
}

function renderProductDetail(id) {
  const p = state.products.find(x => x.id === id);
  document.getElementById('app').innerHTML = `
    <h2>${p.name}</h2>
    <div style="font-size:3em">${p.icon}</div>
    <p>${p.description}</p>
    <div>Preis: <b>${p.price}€</b></div>
    <button onclick="buyProduct(${p.id})">Jetzt kaufen</button>
    <button onclick="renderProducts()">Zurück zum Katalog</button>
  `;
}

function buyProduct(id) {
  alert("Demo: Zahlungsvorgang für Produkt " + id + " (hier würde Stripe/PayPal integriert werden)");
  renderProducts();
}

function renderContact() {
  document.getElementById('app').innerHTML = `
    <h2>Kontaktformular</h2>
    <input id="name" placeholder="Name"><br>
    <input id="email" placeholder="E-Mail"><br>
    <textarea id="message" placeholder="Nachricht"></textarea><br>
    <button onclick="sendContact()">Senden</button>
    <button onclick="renderDashboard()">Zurück</button>
  `;
}

function sendContact() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const message = document.getElementById('message').value;
  if (!name || !email || !message || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    alert("Bitte alle Felder korrekt ausfüllen.");
    return;
  }
  alert("Nachricht gesendet! Vielen Dank.");
  renderDashboard();
}

function logout() {
  state.user = null;
  renderLogin();
}

window.onload = renderLogin;
