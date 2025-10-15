const baseUrl = "http://127.0.0.1:5000";
let token = localStorage.getItem("token");

document.getElementById("btn-login").onclick = async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${baseUrl}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();
  if (res.ok) {
    token = data.access_token;
    localStorage.setItem("token", token);
    document.getElementById("login-result").innerText = "✅ Login success!";
  } else {
    document.getElementById("login-result").innerText = "❌ " + data.error;
  }
};

document.getElementById("btn-refresh-items").onclick = async () => {
  const res = await fetch(`${baseUrl}/items`);
  const data = await res.json();
  const list = document.getElementById("items-list");
  list.innerHTML = "";
  data.items.forEach(i => {
    const li = document.createElement("li");
    li.textContent = `${i.name} (Rp ${i.price})`;
    list.appendChild(li);
  });
};

document.getElementById("btn-update-profile").onclick = async () => {
  if (!token) {
    alert("Please login first!");
    return;
  }
  const name = document.getElementById("profile-name").value;
  const email = document.getElementById("profile-email").value;

  const res = await fetch(`${baseUrl}/profile`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name, email }),
  });

  const data = await res.json();
  document.getElementById("profile-result").innerText = res.ok
    ? `✅ ${data.message}: ${data.profile.name}, ${data.profile.email}`
    : `❌ ${data.error}`;
};
