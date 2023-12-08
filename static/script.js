// Handle form submission
document
  .getElementById("uploadForm")
  .addEventListener("submit", handleFormSubmit);

function handleFormSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  toggleElementDisplay("loading", true);

  uploadFormData(formData);
}

function uploadFormData(formData) {
  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then(handleUploadResponse)
    .catch(handleUploadError);
}

function handleUploadResponse(data) {
  toggleElementDisplay("loading", false);
  if (data.message === "Files successfully uploaded") {
    toggleElementDisplay("downloadLink", true);
  } else {
    alert("Error: " + data.error);
  }
}

function handleUploadError(error) {
  toggleElementDisplay("loading", false);
  alert("Error: " + error);
}

function toggleElementDisplay(elementId, show) {
  const element = document.getElementById(elementId);
  element.style.display = show ? "block" : "none";
}

// Handle toggle labels
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toggle-label").forEach((label) => {
    label.addEventListener("click", toggleTextareaDisplay);
  });
});

function toggleTextareaDisplay() {
  const textareaContainer = this.nextElementSibling;
  const icon = this.querySelector(".toggle-icon");
  const isExpanded = textareaContainer.style.maxHeight;

  if (isExpanded) {
    textareaContainer.style.maxHeight = null;
    icon.classList.add("collapsed");
  } else {
    textareaContainer.style.maxHeight = textareaContainer.scrollHeight + "px";
    icon.classList.remove("collapsed");
  }
}
