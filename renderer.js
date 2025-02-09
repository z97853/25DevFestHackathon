const API_URL = "http://127.0.0.1:5000"; // Python Backend URL

document.addEventListener("DOMContentLoaded", () => {
    updateTime(); // Run on load
    setInterval(updateTime, 1000); // Update every second
});

// ✅ Save Task (Automatically schedules PUSH in the backend and updates the task list)
document.getElementById("saveTask").addEventListener("click", async () => {
    const title = document.getElementById("taskTitle").value;
    const category = document.getElementById("taskCategory").value;
    const time = document.getElementById("taskTime").value;
    const url = document.getElementById("taskURL").value;

    // ✅ Prevent saving if any field is empty
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
    alert(`Task Saved & Scheduled! ID: ${result.task_id}`);

    // ✅ Automatically refresh the task list after saving
    loadTasks();

    // ✅ Clear input fields
    document.getElementById("taskTitle").value = "";
    document.getElementById("taskCategory").value = "";
    document.getElementById("taskTime").value = "";
    document.getElementById("taskURL").value = "";
});


// ✅ Function to Load Tasks Automatically
async function loadTasks() {
    const response = await fetch(`${API_URL}/get-tasks`);
    const tasks = await response.json();

    const taskListElement = document.getElementById("taskList");
    taskListElement.innerHTML = ""; // Clear previous tasks

    tasks.forEach(task => {
        const listItem = document.createElement("li");
        listItem.className = "task-item";
        listItem.innerHTML = `
            <span> Task:${task.title} ID: ${task.id} Time:(${task.time})</span>
            <button onclick="copyTaskId('${task.id}')">Copy ID</button>
        `;
        taskListElement.appendChild(listItem);
    });
}

// ✅ Copy Task ID to Clipboard
function copyTaskId(taskId) {
    navigator.clipboard.writeText(taskId).then(() => {
        alert("Task ID copied!");
    });
}

// ✅ Delete Task
document.getElementById("deleteTask").addEventListener("click", async () => {
    const taskId = document.getElementById("taskId").value;
    const response = await fetch(`${API_URL}/delete-task/${taskId}`, { method: "DELETE" });

    const result = await response.json();
    alert(result.message);
});

// ✅ Show Current Time
function updateTime() {
    const now = new Date();
    const formattedTime = now.toLocaleString();
    document.getElementById("currentTime").innerText = `⏳ ${formattedTime}`;
}
setInterval(updateTime, 1000); // Update every second
updateTime(); // Initial call
