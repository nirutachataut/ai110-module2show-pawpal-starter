# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Implementation Summary

`Owner` stores the owner's information, availability, preferences, and pets. `Pet` stores its name, species, and care tasks. `Task` represents a care activity with a duration, priority, frequency, and completion status. `Scheduler` creates a daily plan from the owner's tasks.

`Owner.get_all_tasks()` gathers tasks from every pet so the Scheduler can consider them together. The Scheduler sorts tasks by priority and adds tasks that fit within the owner's available time. `main.py` demonstrates this by creating pets and tasks, generating a daily plan, and printing the schedule and explanation.

## Features

- **Owner and pet management:** Enter owner information and add pets in the
  Streamlit interface. `Owner.add_pet()` stores each `Pet`.
- **Pet care task management:** Add tasks with a title, duration, priority,
  due date, scheduled time, and recurrence frequency. Tasks are stored on the
  selected `Pet` with `Pet.add_task()` and remain available in session state.
- **Chronological sorting:** `Scheduler.sort_by_time()` sorts valid scheduled
  times from earliest to latest. Tasks without a valid time appear last.
- **Task filtering:** `Owner.filter_tasks()` filters by pet name, completed
  state, or both; the Streamlit task table updates to match the selected
  filters.
- **Daily recurrence:** `Pet.complete_task()` creates the next daily task
  occurrence one day after its due date.
- **Weekly recurrence:** `Pet.complete_task()` creates the next weekly
  occurrence seven days after its due date.
- **Conflict detection:** `Scheduler.detect_conflicts()` detects overlapping
  pending tasks on the same date. The Streamlit app displays warnings without
  preventing task entry.
- **Streamlit task management:** Add pets and tasks, review filtered tasks,
  mark pending tasks complete, and generate a daily plan with an explanation.
- **Automated testing:** `tests/test_pawpal.py` covers core object behavior
  and scheduling algorithms.

## Final UML Class Diagram

The final Mermaid diagram reflects the implemented classes and relationships:
[diagrams/uml_final.mmd](diagrams/uml_final.mmd).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Run the Application

Install the declared dependencies using the setup commands above, then start
the terminal demo or Streamlit interface:

```bash
python main.py
streamlit run app.py
```

Run the automated tests with:

```bash
python -m pytest
```

## 🖥️ Sample Output

The following is the terminal output from running `python main.py`:

```
Recurring Tasks
---------------
Completed 'Feeding Buddy'; next due: 2025-01-02
Completing it again creates another task: False
Completed 'Grooming Luna'; next due: 2025-01-08
Tasks Sorted by Scheduled Time
-------------------------------
07:00 (No due date) - Walking Buddy
08:30 (2025-01-01) - Feeding Buddy
08:30 (2025-01-02) - Feeding Buddy
09:00 (2025-01-02) - Walk Buddy
09:00 (2025-01-02) - Give Buddy Medicine
09:15 (2025-01-01) - Grooming Luna
09:15 (2025-01-02) - Feed Luna
09:15 (2025-01-08) - Grooming Luna
09:30 (2025-01-02) - Brush Luna

Tasks Filtered by Pet Name (Buddy)
-----------------------------------
Feeding Buddy
Walking Buddy
Walk Buddy
Give Buddy Medicine
Feeding Buddy

Tasks Filtered by Pet Name (Luna)
----------------------------------
Grooming Luna
Feed Luna
Brush Luna
Grooming Luna

Completed Tasks
---------------
Feeding Buddy
Grooming Luna

Pending Tasks
-------------
Walking Buddy
Walk Buddy
Give Buddy Medicine
Feeding Buddy
Feed Luna
Brush Luna
Grooming Luna
Today's Schedule
----------------
Walking Buddy - 30 minutes (priority 3)
Walk Buddy - 30 minutes (priority 3)

Total scheduled time: 60 minutes
Owner's available time: 60 minutes

Plan explanation:
Skipped 'Feeding Buddy': it is already completed.
Selected 'Walking Buddy' (priority 3): it fits in the remaining time.
Selected 'Walk Buddy' (priority 3): it fits in the remaining time.
Skipped 'Feeding Buddy' (priority 3): not enough available time.
Skipped 'Give Buddy Medicine' (priority 2): not enough available time.
Skipped 'Grooming Luna': it is already completed.
Skipped 'Feed Luna' (priority 2): not enough available time.
Skipped 'Grooming Luna' (priority 2): not enough available time.
Skipped 'Brush Luna' (priority 1): not enough available time.

Scheduling Conflict Warnings
----------------------------
Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with Give Buddy Medicine (09:00-09:05).
Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with Feed Luna (09:15-09:25).
```

## Testing PawPal+

### How to Run Tests

From the project root, run the full automated test suite with:

```bash
python -m pytest
```

### Test Coverage

The tests in `tests/test_pawpal.py` cover:

- Owner pet addition, Pet task addition, task completion state, and empty owners
  or pets.
- Chronological sorting, out-of-order and equal times, missing or invalid
  times, empty lists, and preserving the input list.
- Filtering by pet and completion status, combined filters, no filters,
  duplicate references, and no matching tasks.
- Daily and weekly recurring tasks, due-date calculations, preserved task
  details, non-recurring tasks, and repeated completion.
- Conflict warnings for same-time and overlapping tasks, including different
  pets; back-to-back tasks, different dates, completed tasks, invalid or
  missing scheduling information, empty owners, and duplicate references.

### Successful Test Results

Actual output from `python -m pytest`:

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/nirutachataut/ai110-module2show-pawpal-starter
configfile: pytest.ini
plugins: anyio-4.15.1
collected 22 items

tests/test_pawpal.py ......................                              [100%]

============================== 22 passed in 0.02s ==============================
```

### Confidence Level

Confidence Level: 4/5 stars

All 22 backend tests pass and cover the main scheduling behaviors and listed
edge cases. A Streamlit `AppTest` smoke check also confirmed the app renders
and initializes the Owner in session state. This is not a full interactive
browser test, and the tests do not cover every real-world scheduling case
(including conflicts that cross midnight), so the result is not rated 5/5.

## Smarter Scheduling

The scheduling features are implemented in `pawpal_system.py` and demonstrated
by `main.py`.

### 1. Sorting by Time

`Scheduler.sort_by_time(tasks)` returns a new list in chronological order.
Valid zero-padded 24-hour times (`HH:MM`) come first; missing or invalid times
are placed at the end. The original list is not changed. The existing
`Scheduler.sort_tasks(tasks)` method continues to order tasks by priority.

```python
sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
```

### 2. Filtering Tasks

`Owner.filter_tasks(pet_name=None, completed=None)` returns matching task
objects without changing the owner's tasks. Use `completed=True` for completed
tasks, `completed=False` for pending tasks, or provide both filters together.
With no filters, it returns all tasks once, even if a task reference appears
more than once in the owner's pets.

```python
buddy_pending = owner.filter_tasks(pet_name="Buddy", completed=False)
completed_tasks = owner.filter_tasks(completed=True)
```

### 3. Recurring Tasks

`Pet.complete_task(task, completed_on=None)` marks the task complete and keeps
it in that pet's history. A daily task produces a new pending task due one day
after its due date; a weekly task produces one due seven days later. The new
task keeps the title, duration, priority, scheduled time, and frequency.
Non-recurring tasks do not repeat, and completing an already-completed task
does not create a duplicate. `completed_on` supplies the reference date only
when the original task has no due date.

```python
next_occurrence = buddy.complete_task(task)
```

### 4. Conflict Detection

`Scheduler.detect_conflicts()` checks pending tasks belonging to all of the
owner's pets. It returns a warning for each pair whose scheduled intervals
overlap on the same due date. Tasks with missing or invalid dates or times,
and tasks with non-positive durations, are ignored. Back-to-back tasks are not
conflicts, and warnings do not change task times or the generated plan.

```python
warnings = scheduler.detect_conflicts()
for warning in warnings:
    print(warning)
```

### Run the Project

Run the terminal demonstration:

```bash
python main.py
```

Launch the Streamlit interface:

```bash
streamlit run app.py
```

Run the automated tests:

```bash
python -m pytest
```

The terminal demo shows the sorted tasks, Buddy and Luna filters, daily and
weekly recurrence, the generated schedule, and conflict warnings. Example
output excerpts from `python main.py`:

```text
Recurring Tasks
---------------
Completed 'Feeding Buddy'; next due: 2025-01-02
Completing it again creates another task: False
Completed 'Grooming Luna'; next due: 2025-01-08
```

```text
Tasks Filtered by Pet Name (Luna)
----------------------------------
Grooming Luna
Feed Luna
Brush Luna
Grooming Luna
```

```text
Scheduling Conflict Warnings
----------------------------
Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with Give Buddy Medicine (09:00-09:05).
Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with Feed Luna (09:15-09:25).
```

## Demo Walkthrough

1. Start the interface from the project folder with `streamlit run app.py`.
2. Enter the owner's name, available time, and preferences in the owner
   information fields.
3. Enter `Buddy` as the pet name, choose `dog`, and select **Add pet**.
4. Enter `Luna` as the pet name, choose `cat`, and select **Add pet**.
5. Add a `Feeding Buddy` task, choose Buddy, and set its duration, priority,
   due date, and scheduled time.
6. Add a `Walking Luna` task and choose Luna. Set a time that overlaps the
   feeding task to see conflict detection in the task/schedule view.
7. Review the saved task table, which is sorted chronologically; each row
   includes pet, due date, time, duration, priority, frequency, and status.
8. Use **Filter by pet** and **Filter by status** to show all tasks, one pet's
   tasks, pending tasks, completed tasks, or a combination.
9. Select a pending daily or weekly task and click **Complete selected task**.
   Its next occurrence is shown in the table with the next due date.
10. Add another task at an overlapping time, then review the `st.warning()`
    conflict message. Task entry remains enabled.
11. Select **Generate schedule** to see the tasks selected within the owner's
    available time and the Scheduler's explanation.

The terminal demo can be run separately with `python main.py`. These excerpts
are from its actual output:

```text
Completed 'Feeding Buddy'; next due: 2025-01-02
Completing it again creates another task: False
Completed 'Grooming Luna'; next due: 2025-01-08

Tasks Sorted by Scheduled Time
-------------------------------
07:00 (No due date) - Walking Buddy
08:30 (2025-01-01) - Feeding Buddy
08:30 (2025-01-02) - Feeding Buddy
09:00 (2025-01-02) - Walk Buddy

Tasks Filtered by Pet Name (Luna)
----------------------------------
Grooming Luna
Feed Luna
Brush Luna
Grooming Luna

Scheduling Conflict Warnings
----------------------------
Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with Give Buddy Medicine (09:00-09:05).
Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with Feed Luna (09:15-09:25).
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
