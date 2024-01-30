// Handle form submission
document
  .getElementById("uploadForm")
  .addEventListener("submit", handleFormSubmit);

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("document");
  if (fileInput) {
    fileInput.addEventListener(
      "change",
      function () {
        console.log("Files changed:", fileInput.files); // Debugging line
        displayFileNames();
      },
      false
    );
  } else {
    console.log("File input not found."); // Debugging line
  }
});

function handleFormSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const files = form.querySelector('input[type="file"]').files;

  // Check the number of files
  if (files.length > 3) {
    alert("You can only upload a maximum of 3 files.");
    return;
  }

  // Check the size of each file
  for (let i = 0; i < files.length; i++) {
    if (files[i].size > 5242880) {
      // 5 MB in bytes
      alert("Each file must be no larger than 5 MB.");
      return;
    }
  }

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

function displayFileNames() {
  const fileInput = document.getElementById("document");
  const fileNamesDiv = document.getElementById("fileNames");

  if (fileInput.files.length > 0) {
    fileNamesDiv.innerHTML =
      "Selected files: " +
      Array.from(fileInput.files)
        .map((file) => file.name)
        .join(", ");
  } else {
    fileNamesDiv.innerHTML = "";
  }
}
