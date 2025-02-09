const API_URL = "http://127.0.0.1:5000"; // Python Backend URL

// ✅ Save Task
document.getElementById("saveTask").addEventListener("click", async () => {
    const title = document.getElementById("taskTitle").value;
    const category = document.getElementById("taskCategory").value;
    const time = document.getElementById("taskTime").value;
    const url = document.getElementById("taskURL").value;

    const response = await fetch(`${API_URL}/save-task`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, category, time, url })
    });

    const result = await response.json();
    alert(`Task Saved! ID: ${result.task_id}`);
});

// ✅ Load Tasks
document.getElementById("getTasks").addEventListener("click", async () => {
    const response = await fetch(`${API_URL}/get-tasks`);
    const tasks = await response.json();

    const taskListElement = document.getElementById("taskList");
    taskListElement.innerHTML = "";

    tasks.forEach(task => {
        const listItem = document.createElement("li");
        listItem.className = "task-item";
        listItem.innerHTML = `
            <span>ID: ${task.id} - ${task.title} (${task.time})</span>
            <button onclick="copyTaskId('${task.id}')">Copy ID</button>
        `;
        taskListElement.appendChild(listItem);
    });
});

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
