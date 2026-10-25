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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/nirutachataut/ai110-module2show-pawpal-starter
configfile: pytest.ini
plugins: anyio-4.15.1
collected 18 items

tests/test_pawpal.py ..................                                  [100%]

============================== 18 passed in 0.01s ===============================
```

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
pytest
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

## 📸 Demo Walkthrough

1. Open a terminal in the project folder.
2. Activate the project environment if you are using one.
3. Run `python main.py`.
4. Read the sorted tasks, recurrence examples, daily plan, and any scheduling conflict warnings.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
