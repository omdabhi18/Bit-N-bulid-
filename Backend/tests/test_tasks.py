import pytest

@pytest.mark.asyncio
async def test_tasks_flow(client):
    # 1. Get tasks
    res = await client.get("/api/tasks")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) >= 4

    # 2. Update task status to completed
    task_id = tasks[0]["id"]
    patch_res = await client.patch(f"/api/tasks/{task_id}/status", json={"status": "completed"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "completed"

    # 3. Create new task
    create_res = await client.post("/api/tasks", json={
        "title": "Check drip disc filter pressure",
        "field": "Field A",
        "priority": "High",
        "dueTime": "Tomorrow 08:00",
        "assignedTo": "Kishanbhai Patel"
    })
    assert create_res.status_code == 200
    assert "TSK-" in create_res.json()["id"]
