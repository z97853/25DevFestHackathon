const API_URL = "http://127.0.0.1:5000"; // Python Backend URL

// ✅ Save Task (Automatically schedules focus lock)
document.getElementById("saveTask").addEventListener("click", async () => {
    const title = document.getElementById("taskTitle").value;
    const category = document.getElementById("taskCategory").value;
    const time = document.getElementById("taskTime").value;
    const url = document.getElementById("taskURL").value;

    if (!title || !category || !time || !url) {
        alert("Please fill in all fields!");
        return;
    }

    const response = await fetch(`${API_URL}/save-task`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, category, time, url })
    });

    const result = await response.json();
    alert(`Task Saved & Focus Lock Scheduled! ID: ${result.task_id}`);

    loadTasks(); // ✅ Refresh To-Do List
    document.getElementById("taskTitle").value = "";
    document.getElementById("taskCategory").value = "";
    document.getElementById("taskTime").value = "";
    document.getElementById("taskURL").value = "";
});

// ✅ Load To-Do List
async function loadTasks() {
    const response = await fetch(`${API_URL}/get-tasks`);
    const tasks = await response.json();

    const taskListElement = document.getElementById("taskList");
    taskListElement.innerHTML = ""; // Clear previous tasks

    tasks.forEach(task => {
        const listItem = document.createElement("li");
        listItem.className = "task-item";
        listItem.innerHTML = `
            <span>${task.title} (${task.time})</span>
            <button onclick="startFocusMode('${task.url}')">Start</button>
        `;
        taskListElement.appendChild(listItem);
    });
}

// ✅ Start Focus Mode
async function startFocusMode(url) {
    await fetch(`${API_URL}/focus-lock`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    });

    alert("Focus mode started for 5 minutes!");
    showCountdown();
}

// ✅ Countdown Timer
function showCountdown() {
    let countdown = 300; // 5 minutes in seconds
    const timerElement = document.getElementById("countdownTimer");

    const timerInterval = setInterval(() => {
        let minutes = Math.floor(countdown / 60);
        let seconds = countdown % 60;
        timerElement.innerText = `Time Left: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        if (countdown === 0) {
            clearInterval(timerInterval);
            setTimeout(() => {
                if (confirm("Do you really want to exit?")) {
                    setTimeout(() => window.close(), 10000);
                }
            }, 1000);
        } else if (countdown <= 60) {
            alert("Keep going! Stay focused.");
        }

        countdown--;
    }, 1000);
}
