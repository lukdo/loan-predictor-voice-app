// const BACKEND_BASE_URL = "https://loan-backend-849346508536.europe-west1.run.app"; // adjust if needed
const BACKEND_BASE_URL = "http://localhost:8001";

let mediaRecorder;
let audioChunks = [];

document.addEventListener("DOMContentLoaded", () => {
  console.log("[voice_form] JS loaded, DOM ready");

  const recordBtn = document.getElementById("record-btn");
  const statusText = document.getElementById("record-status");

  if (!recordBtn) {
    console.error("[voice_form] No element with id 'record-btn' found");
    return;
  }

  recordBtn.addEventListener("click", async () => {
    console.log("[voice_form] record button clicked");

    if (!mediaRecorder || mediaRecorder.state === "inactive") {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        audioChunks = [];
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          console.log("[voice_form] recording stopped, sending audio...");
          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          await sendAudioToBackend(audioBlob, statusText);
        };

        mediaRecorder.start();
        if (statusText) statusText.textContent = "Recording... (click again to stop)";
        recordBtn.textContent = "⏹️ Stop";

        // Auto-stop after 60s
        setTimeout(() => {
          if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            if (statusText) statusText.textContent = "Recording stopped (60s limit)";
            recordBtn.textContent = "🎙️ Describe your situation";
          }
        }, 60000);
      } catch (err) {
        console.error("[voice_form] getUserMedia error", err);
        alert("Cannot access microphone (check browser permissions).");
      }
    } else if (mediaRecorder.state === "recording") {
      // Manual stop
      mediaRecorder.stop();
      if (statusText) statusText.textContent = "Recording stopped";
      recordBtn.textContent = "🎙️ Describe your situation";
    }
  });
});

async function sendAudioToBackend(audioBlob, statusText) {
  if (statusText) statusText.textContent = "Transcribing and extracting fields...";

  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");

  try {
    const response = await fetch(`${BACKEND_BASE_URL}/voice-form`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const text = await response.text();
      console.error("[voice_form] HTTP error", response.status, text);

      if (statusText) {
        if (response.status === 503) {
          statusText.textContent =
            "The voice model is temporarily overloaded. Please try again in a few seconds.";
        } else {
          statusText.textContent = "Error while processing voice";
        }
      }
      return;
    }

    const data = await response.json();
    console.log("[voice_form] Received data:", data);

    fillFormFromJson(data);
    if (statusText) statusText.textContent = "Form filled from voice ✅";
  } catch (err) {
    console.error("[voice_form] fetch error", err);
    if (statusText) statusText.textContent = "Error calling backend";
  }
}

// Tries by name first, then by id
function setValueIfPresent(nameOrId, value) {
  if (value === undefined || value === null) return;

  const byName = document.getElementsByName(nameOrId)[0];
  const el = byName || document.getElementById(nameOrId);

  if (!el) {
    console.warn(`[voice_form] No element found for "${nameOrId}"`);
    return;
  }

  el.value = value;
}

function fillFormFromJson(data) {
  // FULL NAME – this is the important new line
  setValueIfPresent("name_surname", data.name_surname);

  // Financial info
  setValueIfPresent("annual_income", data.annual_income);
  setValueIfPresent("loan_amount", data.loan_amount);

  // Categorical
  setValueIfPresent("gender", data.gender);
  setValueIfPresent("marital_status", data.marital_status);
  setValueIfPresent("education_level", data.education_level);
  setValueIfPresent("employment_status", data.employment_status);
  setValueIfPresent("loan_purpose", data.loan_purpose);
  setValueIfPresent("grade_subgrade", data.grade_subgrade);

  // Sliders + visible labels
  if (data.interest_rate !== undefined && data.interest_rate !== null) {
    setValueIfPresent("interest_rate", data.interest_rate);
    const span = document.getElementById("interest_rate_value");
    if (span) span.innerText = `${data.interest_rate}%`;
  }

  if (data.debt_to_income_ratio !== undefined && data.debt_to_income_ratio !== null) {
    setValueIfPresent("debt_to_income_ratio", data.debt_to_income_ratio);
    const span = document.getElementById("debt_to_income_ratio_value");
    if (span) span.innerText = data.debt_to_income_ratio;
  }

  if (data.credit_score !== undefined && data.credit_score !== null) {
    setValueIfPresent("credit_score", data.credit_score);
    const span = document.getElementById("credit_score_value");
    if (span) span.innerText = data.credit_score;
  }
}
