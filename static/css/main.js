const btn = document.querySelector(".btn");
const cbtn = document.querySelector(".closeBtn");

btn.addEventListener("input", function () {
  btn.classList.add("active");
  cbtn.classList.add("active");
});
cbtn.addEventListener("click", function () {
  cbtn.classList.remove("active");
  btn.classList.remove("active");

  const getValue = document.getElementById("city");
  if (getValue.value != "") getValue.value = "";
});