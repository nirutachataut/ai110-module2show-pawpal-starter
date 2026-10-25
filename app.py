from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_time=60,
        preferences=[],
    )

owner = st.session_state.owner

st.session_state.setdefault("daily_plan", [])
st.session_state.setdefault("plan_explanation", "")
st.session_state.setdefault("conflict_warnings", [])
st.session_state.setdefault("completion_message", "")
st.session_state.setdefault("owner_name", owner.name)
st.session_state.setdefault("available_time", owner.available_time)
st.session_state.setdefault("owner_preferences", owner.preferences)

st.markdown(
    """
Welcome to PawPal+. Enter owner and pet information, add care tasks, and generate a daily plan.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pet Information")
owner.name = st.text_input("Owner name", key="owner_name")
owner.set_available_time(
    st.number_input(
        "Available time (minutes)",
        min_value=0,
        key="available_time",
    )
)
owner.update_preferences(
    st.multiselect(
        "Preferences",
        ["daily care", "walks", "feeding", "grooming", "medication", "play"],
        key="owner_preferences",
    )
)

pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
if st.button("Add pet"):
    if pet_name.strip():
        pet = Pet(name=pet_name.strip(), species=species)
        owner.add_pet(pet)
        st.success(f"Added {pet.name} to your pets.")
        st.session_state.daily_plan = []
        st.session_state.plan_explanation = ""
        st.session_state.conflict_warnings = []
    else:
        st.warning("Enter a pet name before adding a pet.")

if owner.pets:
    st.write("Your pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("Add a pet before adding care tasks.")

st.markdown("### Tasks")
st.caption("Add care tasks to one of your pets.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input(
        "Task title", value="Morning walk", key="task_title"
    )
with col2:
    duration = st.number_input(
        "Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration"
    )
with col3:
    priority = st.selectbox(
        "Priority", ["low", "medium", "high"], index=2, key="task_priority"
    )

with st.expander("Task schedule and recurrence"):
    due_date = st.date_input("Due date", value=date.today(), key="task_due_date")
    scheduled_time = st.time_input(
        "Scheduled time", value=time(9, 0), key="task_scheduled_time"
    )
    frequency = st.selectbox(
        "Frequency",
        ["once", "daily", "weekly"],
        index=1,
        key="task_frequency",
    )

selected_pet = None
if owner.pets:
    selected_pet = st.selectbox(
        "Task belongs to",
        options=range(len(owner.pets)),
        format_func=lambda pet_index: (
            f"{owner.pets[pet_index].name} ({owner.pets[pet_index].species})"
        ),
        key="selected_pet",
    )

if st.button("Add task", disabled=selected_pet is None):
    priority_values = {"low": 1, "medium": 2, "high": 3}
    task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority_values[priority],
        frequency=frequency,
        scheduled_time=scheduled_time.strftime("%H:%M"),
        due_date=due_date,
    )
    owner.pets[selected_pet].add_task(task)
    task_conflicts = Scheduler(owner).detect_conflicts()
    if task_conflicts:
        st.info(
            f"Added '{task.title}' to {owner.pets[selected_pet].name}'s tasks. "
            "Review the scheduling conflict warning below."
        )
    else:
        st.success(
            f"Added '{task.title}' to {owner.pets[selected_pet].name}'s tasks. "
            "No scheduling conflicts found."
        )
    st.session_state.daily_plan = []
    st.session_state.plan_explanation = ""
    st.session_state.conflict_warnings = []

all_tasks = owner.get_all_tasks()
if st.session_state.completion_message:
    st.success(st.session_state.completion_message)
    st.session_state.completion_message = ""

if all_tasks:
    st.write("Current tasks, sorted by scheduled time:")
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        pet_filter_options = ["All pets"] + list(
            dict.fromkeys(pet.name for pet in owner.pets)
        )
        pet_filter = st.selectbox("Filter by pet", pet_filter_options)
    with filter_col2:
        status_filter = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed"]
        )

    filtered_tasks = owner.filter_tasks(
        pet_name=None if pet_filter == "All pets" else pet_filter,
        completed={
            "All": None,
            "Pending": False,
            "Completed": True,
        }[status_filter],
    )
    task_pet_lookup = {}
    for pet in owner.pets:
        if pet_filter != "All pets" and pet.name != pet_filter:
            continue
        for task in pet.get_tasks():
            task_pet_lookup.setdefault(id(task), pet)

    sorted_tasks = Scheduler(owner).sort_by_time(filtered_tasks)
    task_rows = [
        {
            "Pet": task_pet_lookup[id(task)].name,
            "Task": task.title,
            "Due date": task.due_date.isoformat() if task.due_date else "Not set",
            "Scheduled time": task.scheduled_time or "Not set",
            "Duration (minutes)": task.duration_minutes,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Status": "Completed" if task.completed else "Pending",
        }
        for task in sorted_tasks
    ]
    if task_rows:
        st.dataframe(task_rows, hide_index=True, width="stretch")
    else:
        st.info("No tasks match the selected filters.")

    pending_tasks = [task for task in sorted_tasks if not task.completed]
    if pending_tasks:
        st.caption("Complete a pending task to mark it done or create its next occurrence.")
        task_index = st.selectbox(
            "Task to complete",
            options=range(len(pending_tasks)),
            format_func=lambda index: (
                f"{task_pet_lookup[id(pending_tasks[index])].name}: "
                f"{pending_tasks[index].title}"
            ),
            key="task_to_complete",
        )
        if st.button("Complete selected task"):
            task = pending_tasks[task_index]
            pet = task_pet_lookup[id(task)]
            next_task = pet.complete_task(task)
            if next_task is None:
                st.session_state.completion_message = (
                    f"Marked '{task.title}' complete."
                )
            else:
                st.session_state.completion_message = (
                    f"Marked '{task.title}' complete. "
                    f"Next occurrence is due {next_task.due_date}."
                )
            st.session_state.daily_plan = []
            st.session_state.plan_explanation = ""
            st.session_state.conflict_warnings = []
            st.rerun()
    else:
        st.info("No pending tasks match the selected filters.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a plan using your pets' tasks, priorities, and available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    st.session_state.daily_plan = scheduler.generate_plan()
    st.session_state.plan_explanation = scheduler.explain_plan()
    st.session_state.conflict_warnings = scheduler.detect_conflicts()

current_conflicts = list(dict.fromkeys(Scheduler(owner).detect_conflicts()))
if current_conflicts:
    st.write("Scheduling conflict warnings")
    for warning in current_conflicts:
        conflicting_pet_names = []
        for pet in owner.pets:
            for task in pet.get_tasks():
                if (
                    task.scheduled_time
                    and f"{task.title} ({task.scheduled_time}-" in warning
                    and pet.name not in conflicting_pet_names
                ):
                    conflicting_pet_names.append(pet.name)
        pet_note = (
            f" Pets involved: {', '.join(conflicting_pet_names)}."
            if conflicting_pet_names
            else ""
        )
        st.warning(f"{warning}{pet_note}")
elif all_tasks:
    st.info("No scheduling conflicts found.")
else:
    st.info("Add scheduled tasks to check for conflicts.")

if st.session_state.daily_plan:
    st.write("Today's Schedule")
    for task in st.session_state.daily_plan:
        st.write(
            f"- {task.title} - {task.duration_minutes} minutes "
            f"(priority {task.priority})"
        )

if st.session_state.plan_explanation:
    st.write("Plan explanation")
    st.write(st.session_state.plan_explanation)
