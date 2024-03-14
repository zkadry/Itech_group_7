const profBtn = document.getElementById("profBtn");
const edtBtn = document.getElementById("edtBtn");

profBtn.addEventListener("mousedown", function() {
  profBtn.style.backgroundColor = "#d9d9d9";
});

profBtn.addEventListener("mouseup", function() {
  profBtn.style.backgroundColor = "#f2f2f2";
  window.location.href = "/inkfluence/profile/";
});

edtBtn.addEventListener("mousedown", function() {
  edtBtn.style.backgroundColor = "#d9d9d9";
});

edtBtn.addEventListener("mouseup", function() {
  edtBtn.style.backgroundColor = "#f2f2f2";
  window.location.href = "/inkfluence/profile/edit/";
});