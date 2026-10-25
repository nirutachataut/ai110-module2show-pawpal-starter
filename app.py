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
    )
    owner.pets[selected_pet].add_task(task)
    st.success(f"Added '{task.title}' to {owner.pets[selected_pet].name}'s tasks.")
    st.session_state.daily_plan = []
    st.session_state.plan_explanation = ""

if owner.get_all_tasks():
    st.write("Current tasks:")
    for pet in owner.pets:
        for task in pet.get_tasks():
            st.write(
                f"- {pet.name} ({pet.species}): {task.title} - "
                f"{task.duration_minutes} minutes (priority {task.priority})"
            )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a plan using your pets' tasks, priorities, and available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    st.session_state.daily_plan = scheduler.generate_plan()
    st.session_state.plan_explanation = scheduler.explain_plan()

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
