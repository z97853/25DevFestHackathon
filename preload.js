const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("electron", {
    saveTask: (task) => fetch("http://127.0.0.1:5000/save-task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task)
    }).then(response => response.json()),

    getTasks: () => fetch("http://127.0.0.1:5000/get-tasks").then(response => response.json()),

    deleteTask: (taskId) => fetch(`http://127.0.0.1:5000/delete-task/${taskId}`, {
        method: "DELETE"
    }).then(response => response.json())
});
