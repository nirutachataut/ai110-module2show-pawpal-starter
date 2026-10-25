from datetime import date

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

feeding = Task(
    title="Feeding Buddy",
    duration_minutes=10,
    priority=3,
    due_date=date(2025, 1, 1),
    scheduled_time="08:30",
)
walking = Task(
    title="Walking Buddy",
    duration_minutes=30,
    priority=3,
    scheduled_time="07:00",
)
grooming = Task(
    title="Grooming Luna",
    duration_minutes=20,
    priority=2,
    frequency="weekly",
    due_date=date(2025, 1, 1),
    scheduled_time="09:15",
)
buddy_walk = Task(
    title="Walk Buddy",
    duration_minutes=30,
    priority=3,
    due_date=date(2025, 1, 2),
    scheduled_time="09:00",
)
luna_feeding = Task(
    title="Feed Luna",
    duration_minutes=10,
    priority=2,
    due_date=date(2025, 1, 2),
    scheduled_time="09:15",
)
buddy.add_task(feeding)
buddy.add_task(walking)
buddy.add_task(buddy_walk)
luna.add_task(grooming)
luna.add_task(luna_feeding)

print("Recurring Tasks")
print("---------------")
tomorrow_feeding = buddy.complete_task(feeding)
print(f"Completed '{feeding.title}'; next due: {tomorrow_feeding.due_date}")
duplicate_feeding = buddy.complete_task(feeding)
print(f"Completing it again creates another task: {duplicate_feeding is not None}")

next_week_grooming = luna.complete_task(grooming)
print(f"Completed '{grooming.title}'; next due: {next_week_grooming.due_date}")

scheduler = Scheduler(owner)
daily_plan = scheduler.generate_plan()

print("Tasks Sorted by Scheduled Time")
print("-------------------------------")
for task in scheduler.sort_by_time(owner.get_all_tasks()):
    scheduled_time = task.scheduled_time or "Not scheduled"
    due_date = task.due_date.isoformat() if task.due_date else "No due date"
    print(f"{scheduled_time} ({due_date}) - {task.title}")

print("\nTasks Filtered by Pet Name (Buddy)")
print("-----------------------------------")
for task in owner.filter_tasks(pet_name="Buddy"):
    print(task.title)

print("\nCompleted Tasks")
print("---------------")
for task in owner.filter_tasks(completed=True):
    print(task.title)

print("\nPending Tasks")
print("-------------")
for task in owner.filter_tasks(completed=False):
    print(task.title)

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

print("\nScheduling Conflict Warnings")
print("----------------------------")
conflict_warnings = scheduler.detect_conflicts()
if conflict_warnings:
    for warning in conflict_warnings:
        print(warning)
else:
    print("No scheduling conflicts found.")