const profBtn = document.getElementById("profBtn");
const loginBtn = document.getElementById("loginBtn");

profBtn.addEventListener("mousedown", function() {
  profBtn.style.backgroundColor = "#d9d9d9";
});

profBtn.addEventListener("mouseup", function() {
  profBtn.style.backgroundColor = "#f2f2f2";
  window.location.href = "/inkfluence/profile/";
});