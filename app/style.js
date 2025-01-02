let timerInterval;
let score = 0;

document.getElementById('startBtn').addEventListener('click', startTimer);
document.getElementById('pauseBtn').addEventListener('click', pauseTimer);
document.getElementById('resetBtn').addEventListener('click', resetApp);

function startTimer() {
    const timerElement = document.getElementById('timer');
    let seconds = 0;
    timerInterval = setInterval(() => {
        seconds++;
        const minutes = Math.floor(seconds / 60);
        const displaySeconds = seconds % 60;
        timerElement.textContent = `${minutes}:${displaySeconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
}

function resetApp() {
    clearInterval(timerInterval);
    document.getElementById('timer').textContent = '0:00';
    document.getElementById('score').textContent = '0';
    score = 0;
}

function updateScore(newScore) {
    score += newScore;
    document.getElementById('score').textContent = score;
}
