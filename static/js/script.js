document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("upload-form");
  const fileInput = document.getElementById("file-input");
  const classifyBtn = document.getElementById("classify-btn");
  const resultsSection = document.getElementById("results-section");
  const uploadedImage = document.getElementById("uploaded-image");
  const resultText = document.getElementById("result-text");
  const uploadCard = document.getElementById("upload-card");
  const progressBarContainer = document.getElementById(
    "progress-bar-container"
  );
  const progressBar = document.getElementById("progress-bar");
  const uploadText = document.getElementById("upload-text");
  const resultContainer = document.getElementById("result-container");

  // Drag and drop functionality
  uploadCard.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadCard.classList.add("dragover");
  });

  uploadCard.addEventListener("dragleave", () => {
    uploadCard.classList.remove("dragover");
  });

  uploadCard.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadCard.classList.remove("dragover");
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      fileInput.files = files;
      handleFileChange(files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    handleFileChange(file);
  });

  function handleFileChange(file) {
    if (file) {
      uploadText.textContent = file.name;
      classifyBtn.disabled = false;
    } else {
      uploadText.textContent = "Drag & Drop or Click to Upload";
      classifyBtn.disabled = true;
    }
  }

  classifyBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      alert("Please select an image file first.");
      return;
    }

    // Show progress bar and hide previous results
    resultsSection.style.display = "block";
    resultContainer.style.display = "none";
    progressBarContainer.style.display = "block";
    progressBar.style.width = "0%";

    const formData = new FormData(uploadForm);

    // Simulate progress for a better UI experience
    let progress = 0;
    const interval = setInterval(() => {
      if (progress < 90) {
        progress += 5;
        progressBar.style.width = progress + "%";
      }
    }, 100);

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
      });

      clearInterval(interval);
      progressBar.style.width = "100%";

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();

      // Display uploaded image
      const reader = new FileReader();
      reader.onload = (event) => {
        uploadedImage.src = event.target.result;
        uploadedImage.style.display = "block";
      };
      reader.readAsDataURL(file);

      // Hide progress bar and show results
      setTimeout(() => {
        progressBarContainer.style.display = "none";
        resultContainer.style.display = "block";

        if (data.error) {
          resultText.innerHTML = `Error: ${data.error}`;
          resultText.style.color = "#e74c3c";
        } else {
          resultText.innerHTML = `Prediction: <strong>${data.prediction}</strong><br>Confidence: <strong>${data.confidence}</strong>`;
          resultText.style.color = "#2e7d32";
        }
      }, 500);
    } catch (error) {
      console.error("Error:", error);
      resultText.innerHTML = "An error occurred during prediction.";
      resultText.style.color = "#e74c3c";
      uploadedImage.style.display = "none";
      progressBarContainer.style.display = "none";
      resultContainer.style.display = "block";
    } finally {
      classifyBtn.disabled = false;
    }
  });
});
