from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(
    name="Alex",
    available_time=60,
    preferences=["daily care", "walks"],
)

buddy = Pet(name="Buddy", species="dog")
luna = Pet(name="Luna", species="cat")
owner.add_pet(buddy)
owner.add_pet(luna)

buddy.add_task(Task(title="Walking Buddy", duration_minutes=30, priority=3))
buddy.add_task(Task(title="Feeding Buddy", duration_minutes=10, priority=3))
luna.add_task(Task(title="Grooming Luna", duration_minutes=20, priority=2))

scheduler = Scheduler(owner)
daily_plan = scheduler.generate_plan()

print("Today's Schedule")
print("----------------")

for task in daily_plan:
    print(
        f"{task.title} - {task.duration_minutes} minutes "
        f"(priority {task.priority})"
    )

total_scheduled_time = sum(task.duration_minutes for task in daily_plan)
print(f"\nTotal scheduled time: {total_scheduled_time} minutes")
print(f"Owner's available time: {owner.available_time} minutes")

print("\nPlan explanation:")
print(scheduler.explain_plan())