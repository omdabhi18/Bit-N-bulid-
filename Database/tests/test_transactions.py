import pytest
from Database.models.action_plan import ActionPlan, ActionPlanStatus, ActionPriority
from Database.models.task import Task, TaskStatus
from Database.repositories.action_plan_repository import ActionPlanRepository



@pytest.mark.asyncio
async def test_action_plan_approval_and_task_dispatch_transaction(db_session):
    """
    Verify atomic operation:
    Approving an action plan sets status to APPROVED and creates a corresponding Task
    within the same transaction boundary.
    """
    repo = ActionPlanRepository(db_session)
    plan = await repo.create(
        id="act-tx-01",
        field_id="field-1",
        action="Run Fertigation with 19:19:19 NPK Solution",
        estimated_cost=420.0,
        priority=ActionPriority.HIGH,
        confidence=0.92,
        status=ActionPlanStatus.PENDING_APPROVAL,
    )

    # Approve and atomically dispatch task
    approved_plan, dispatched_task = await repo.approve_and_dispatch_task(
        action_plan_id=plan.id,
        user_id="usr-1",
    )

    assert approved_plan.status == ActionPlanStatus.APPROVED
    assert dispatched_task is not None
    assert dispatched_task.action_plan_id == "act-tx-01"
    assert dispatched_task.status == TaskStatus.PENDING
    assert "Fertigation" in dispatched_task.title


@pytest.mark.asyncio
async def test_action_plan_approval_invalid_id_rejection(db_session):
    """Verify that attempting to approve a non-existent plan raises an error cleanly without dirty state."""
    repo = ActionPlanRepository(db_session)
    with pytest.raises(ValueError, match="not found"):
        await repo.approve_and_dispatch_task(
            action_plan_id="non-existent-id",
            user_id="usr-1",
        )
