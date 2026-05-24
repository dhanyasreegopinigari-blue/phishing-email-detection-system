document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const exampleBtn = document.getElementById('exampleBtn');
    const emailInput = document.getElementById('emailInput');
    const spinner = document.getElementById('spinner');
    const resultCard = document.getElementById('resultCard');
    const resultText = document.getElementById('resultText');
    const resultIcon = document.getElementById('resultIcon');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceLabel = document.getElementById('confidenceLabel');
    const errorMsg = document.getElementById('errorMsg');

    analyzeBtn.addEventListener('click', async () => {
        const emailTextVal = emailInput.value.trim();
        errorMsg.textContent = '';

        if (!emailTextVal) {
            errorMsg.textContent = 'Please paste the email content first.';
            return;
        }

        spinner.classList.remove('hidden');
        analyzeBtn.disabled = true;
        resultCard.classList.add('hidden');

        try {
            const resp = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: emailTextVal })
            });

            const data = await resp.json();

            if (!resp.ok) {
                throw new Error(data.error || 'Server error');
            }

            // Show result
            resultCard.classList.remove('hidden');

            const conf = Number(data.confidence || 0);
            confidenceBar.style.width = Math.min(100, conf) + '%';
            confidenceLabel.textContent = conf + '%';

            if (String(data.prediction).toLowerCase() === 'phishing') {
                resultText.textContent = '⚠️ Phishing detected';
                resultIcon.textContent = '🚨';
                confidenceBar.style.background = 'linear-gradient(90deg,var(--danger), #f97316)';
            } else {
                resultText.textContent = '✅ Email appears safe';
                resultIcon.textContent = '✅';
                confidenceBar.style.background = 'linear-gradient(90deg,var(--success), #86efac)';
            }

        } catch (err) {
            errorMsg.textContent = err.message || String(err);
            resultCard.classList.remove('hidden');
            resultText.textContent = 'Error';
            resultIcon.textContent = '❗';
            confidenceBar.style.width = '0%';
            confidenceLabel.textContent = '—';
        } finally {
            spinner.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    exampleBtn.addEventListener('click', () => {
        emailInput.value = `Dear user,\nYou have an urgent message from your bank. Click this link to verify your account: https://malicious.example/login\nSincerely, Bank Support`;
    });
});
