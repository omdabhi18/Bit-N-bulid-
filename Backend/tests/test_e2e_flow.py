import pytest
import asyncio

@pytest.mark.asyncio
async def test_end_to_end_autonomous_advisory_and_execution_flow(client):
    """
    Complete end-to-end demonstration workflow:
    1. Check initial Dashboard state (Field A moisture ~31%)
    2. Multi-Agent Orchestrator triggers cooperative cycle
    3. Soil + Weather + Crop + Risk agents detect high water deficit
    4. Constrained Planner formulates Plan #1024 after verifying constraints
    5. Farmer approves action plan
    6. System dispatches task to Kanban execution board
    7. Valve is triggered via Execution Agent & Mock IoT
    8. Valve status is verified as RUNNING
    9. Audit activity log captures the full chronological sequence
    """
    # Step 1: Query initial Dashboard
    dash_res = await client.get("/api/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["soilMoisture"] <= 35.0 # Low moisture deficit confirmed
    assert dash_data["farmHealthScore"] == 82

    # Step 2: Trigger Multi-Agent Orchestrator Cycle
    cycle_res = await client.post("/api/agents/orchestrate", json={"farmId": "farm-greenvalley-01"})
    assert cycle_res.status_code == 200
    cycle_data = cycle_res.json()
    assert cycle_data["success"] is True
    assert cycle_data["detectedRisksCount"] >= 1

    # Step 3: Fetch Detected Risks
    risks_res = await client.get("/api/risks")
    assert risks_res.status_code == 200
    risks = risks_res.json()
    water_risk = next(r for r in risks if "Water Stress" in r["category"])
    assert water_risk["severity"] == "High"
    assert water_risk["field"] == "Field A (Cotton)"

    # Step 4: Verify Constrained Action Plan
    plans_res = await client.get("/api/action-plans")
    assert plans_res.status_code == 200
    plans = plans_res.json()
    irrigation_plan = next(p for p in plans if p["id"] == "PLAN-1024")
    assert irrigation_plan["estimatedCost"] <= 150.0 # Verified under budget cap
    assert "Safe" in irrigation_plan["constraints"]["weatherWindow"]

    # Step 5: Farmer Approves Plan
    approve_res = await client.post("/api/action-plans/PLAN-1024/approve")
    assert approve_res.status_code == 200
    assert approve_res.json()["success"] is True

    # Step 6: Verify Auto-Dispatched Task on Kanban Board
    tasks_res = await client.get("/api/tasks")
    assert tasks_res.status_code == 200
    tasks = tasks_res.json()
    assert any(t["field"] == "Field A" for t in tasks)

    # Step 7: Execution Agent Triggers Mock IoT Valve
    valve_res = await client.post("/api/sensors/valve/trigger", json={
        "fieldId": "field-a",
        "minutes": 35
    })
    assert valve_res.status_code == 200
    valve_data = valve_res.json()
    assert valve_data["status"] == "Running"
    assert valve_data["fieldId"] == "field-a"

    # Step 8: Verify Activity Audit Logs
    logs_res = await client.get("/api/notifications/activity-logs")
    assert logs_res.status_code == 200
    logs = logs_res.json()
    assert len(logs) >= 5
    # Check that valve open and approval are logged
    log_texts = [l["event"] for l in logs]
    assert any("Valve opened" in t for t in log_texts)
    assert any("approved" in t.lower() for t in log_texts)
