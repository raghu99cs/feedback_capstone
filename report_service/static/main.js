const FEEDBACK_URL = "http://127.0.0.1:5000/feedback";
const ANALYTICS_URL = "http://127.0.0.1:5001/analyse";

let sentimentChart, keywordsChart, trendsChart;

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("feedback-form");
  const statusEl = document.getElementById("submit-status");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusEl.textContent = "Submitting...";
    const payload = {
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      text: document.getElementById("text").value.trim()
    };
    try {
      const res = await fetch(FEEDBACK_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `HTTP ${res.status}`);
      }
      statusEl.textContent = "Thanks, your feedback was submitted.";
      form.reset();
      await refreshAnalytics();
    } catch (err) {
      statusEl.textContent = `Error: ${err.message}`;
    }
  });

  refreshAnalytics();
});

async function refreshAnalytics() {
  const summaryEl = document.getElementById("summary");
  summaryEl.textContent = "Loading analytics...";
  try {
    const res = await fetch(ANALYTICS_URL);
    const data = await res.json();
    summaryEl.textContent = `Total feedback: ${data.total_feedback}`;

    renderSentiment(data.sentiment_distribution);
    renderKeywords(data.keywords);
    renderTrends(data.trends);
  } catch (err) {
    summaryEl.textContent = `Failed to load analytics: ${err.message}`;
  }
}

function renderSentiment(dist) {
  const ctx = document.getElementById("sentimentChart").getContext("2d");
  const labels = ["positive", "negative", "neutral"];
  const values = labels.map(l => dist[l] || 0);

  if (sentimentChart) sentimentChart.destroy();
  sentimentChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: ["#4CAF50", "#F44336", "#FFC107"]
      }]
    },
    options: { responsive: true }
  });
}

function renderKeywords(keywords) {
  const ctx = document.getElementById("keywordsChart").getContext("2d");
  const labels = keywords.map(k => k.word);
  const values = keywords.map(k => k.count);

  if (keywordsChart) keywordsChart.destroy();
  keywordsChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "frequency",
        data: values,
        backgroundColor: "#2196F3"
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true, precision: 0 } }
    }
  });
}

function renderTrends(trends) {
  const ctx = document.getElementById("trendsChart").getContext("2d");
  const labels = trends.map(t => t.date);
  const values = trends.map(t => t.count);

  if (trendsChart) trendsChart.destroy();
  trendsChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "feedback count",
        data: values,
        borderColor: "#9C27B0",
        backgroundColor: "rgba(156, 39, 176, 0.1)"
      }]
    },
    options: { responsive: true }
  });
}

