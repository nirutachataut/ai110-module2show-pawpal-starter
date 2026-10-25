from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task(title="Walk Buddy", duration_minutes=30, priority=3)

    assert task.completed is False

    task.mark_completed()

    assert task.completed is True


def test_task_addition():
    pet = Pet(name="Buddy", species="dog")

    initial_task_count = len(pet.get_tasks())
    task = Task(title="Feed Buddy", duration_minutes=10, priority=3)

    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_task_count + 1


def test_sort_by_time_places_untimed_tasks_last():
    owner = Owner(name="Alex", available_time=60, preferences=[])
    scheduler = Scheduler(owner)
    late_task = Task("Late", 10, 3, scheduled_time="18:00")
    untimed_task = Task("Untimed", 10, 1)
    early_task = Task("Early", 10, 1, scheduled_time="07:30")

    sorted_tasks = scheduler.sort_by_time([late_task, untimed_task, early_task])

    assert sorted_tasks == [early_task, late_task, untimed_task]
    assert scheduler.sort_tasks([early_task, late_task]) == [late_task, early_task]


def test_filter_tasks_by_pet_and_completion_status():
    owner = Owner(name="Alex", available_time=60, preferences=[])
    buddy = Pet(name="Buddy", species="dog")
    luna = Pet(name="Luna", species="cat")
    completed_task = Task("Walk Buddy", 30, 3)
    pending_task = Task("Feed Buddy", 10, 2)
    luna_task = Task("Groom Luna", 20, 1)
    completed_task.mark_completed()
    buddy.add_task(completed_task)
    buddy.add_task(pending_task)
    luna.add_task(luna_task)
    owner.add_pet(buddy)
    owner.add_pet(luna)

    original_tasks = owner.get_all_tasks()

    assert owner.filter_tasks(pet_name="Buddy") == [completed_task, pending_task]
    assert owner.filter_tasks(completed=True) == [completed_task]
    assert owner.filter_tasks(completed=False) == [pending_task, luna_task]
    assert owner.filter_tasks(pet_name="Buddy", completed=False) == [pending_task]
    assert owner.get_all_tasks() == original_tasks


def test_filter_tasks_returns_empty_list_when_no_tasks_match():
    owner = Owner(name="Alex", available_time=60, preferences=[])
    buddy = Pet(name="Buddy", species="dog")
    buddy.add_task(Task("Walk Buddy", 30, 3))
    owner.add_pet(buddy)

    assert owner.filter_tasks(pet_name="Luna") == []
    assert owner.filter_tasks(completed=True) == []


def test_filter_tasks_returns_empty_list_when_owner_has_no_pets():
    owner = Owner(name="Alex", available_time=60, preferences=[])

    assert owner.filter_tasks() == []


def test_daily_task_completion_creates_next_day_occurrence():
    pet = Pet(name="Buddy", species="dog")
    task = Task(
        "Feed Buddy",
        10,
        3,
        frequency="daily",
        scheduled_time="08:30",
        due_date=date(2025, 1, 1),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2025, 1, 2)
    assert next_task.completed is False
    assert next_task.title == task.title
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority
    assert next_task.scheduled_time == task.scheduled_time
    assert next_task.frequency == task.frequency
    assert pet.get_tasks() == [task, next_task]


def test_weekly_task_completion_creates_next_week_occurrence():
    pet = Pet(name="Luna", species="cat")
    task = Task(
        "Groom Luna",
        20,
        2,
        frequency="weekly",
        due_date=date(2025, 1, 1),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == date(2025, 1, 8)
    assert next_task.completed is False


def test_non_recurring_task_completion_creates_no_new_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(
        "One-time visit",
        45,
        1,
        frequency="once",
        due_date=date(2025, 1, 1),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is None
    assert pet.get_tasks() == [task]


def test_completing_task_twice_does_not_create_duplicate_occurrences():
    pet = Pet(name="Buddy", species="dog")
    task = Task("Feed Buddy", 10, 3, due_date=date(2025, 1, 1))
    pet.add_task(task)

    first_next_task = pet.complete_task(task)
    second_next_task = pet.complete_task(task)

    assert first_next_task is not None
    assert second_next_task is None
    assert pet.get_tasks() == [task, first_next_task]


def test_detect_conflict_for_same_start_time():
    owner = Owner("Alex", 60, [])
    buddy = Pet("Buddy", "dog")
    first_task = Task(
        "Walk Buddy", 30, 3, scheduled_time="09:00", due_date=date(2025, 1, 1)
    )
    second_task = Task(
        "Feed Buddy", 10, 2, scheduled_time="09:00", due_date=date(2025, 1, 1)
    )
    buddy.add_task(first_task)
    buddy.add_task(second_task)
    owner.add_pet(buddy)

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "Walk Buddy (09:00-09:30)" in warnings[0]
    assert "Feed Buddy (09:00-09:10)" in warnings[0]


def test_detect_conflict_for_partial_overlap_across_pets():
    owner = Owner("Alex", 60, [])
    buddy = Pet("Buddy", "dog")
    luna = Pet("Luna", "cat")
    buddy.add_task(
        Task("Walk Buddy", 30, 3, scheduled_time="09:00", due_date=date(2025, 1, 1))
    )
    luna.add_task(
        Task("Feed Luna", 10, 2, scheduled_time="09:15", due_date=date(2025, 1, 1))
    )
    owner.add_pet(buddy)
    owner.add_pet(luna)

    warnings = Scheduler(owner).detect_conflicts()

    assert warnings == [
        "Scheduling conflict: Walk Buddy (09:00-09:30) overlaps with "
        "Feed Luna (09:15-09:25)."
    ]


def test_detect_conflicts_ignores_back_to_back_tasks():
    owner = Owner("Alex", 60, [])
    buddy = Pet("Buddy", "dog")
    buddy.add_task(
        Task("Walk Buddy", 30, 3, scheduled_time="09:00", due_date=date(2025, 1, 1))
    )
    buddy.add_task(
        Task("Feed Buddy", 10, 2, scheduled_time="09:30", due_date=date(2025, 1, 1))
    )
    owner.add_pet(buddy)

    assert Scheduler(owner).detect_conflicts() == []


def test_detect_conflicts_ignores_different_dates():
    owner = Owner("Alex", 60, [])
    buddy = Pet("Buddy", "dog")
    buddy.add_task(
        Task("Walk Buddy", 30, 3, scheduled_time="09:00", due_date=date(2025, 1, 1))
    )
    buddy.add_task(
        Task("Walk Buddy next day", 30, 3, scheduled_time="09:15", due_date=date(2025, 1, 2))
    )
    owner.add_pet(buddy)

    assert Scheduler(owner).detect_conflicts() == []


def test_detect_conflicts_ignores_completed_and_invalid_tasks():
    owner = Owner("Alex", 60, [])
    buddy = Pet("Buddy", "dog")
    completed_task = Task(
        "Done", 30, 3, scheduled_time="09:00", due_date=date(2025, 1, 1)
    )
    completed_task.mark_completed()
    buddy.add_task(completed_task)
    buddy.add_task(
        Task("Missing time", 30, 2, due_date=date(2025, 1, 1))
    )
    buddy.add_task(
        Task("Bad time", 30, 2, scheduled_time="25:00", due_date=date(2025, 1, 1))
    )
    buddy.add_task(
        Task("Zero length", 0, 2, scheduled_time="09:00", due_date=date(2025, 1, 1))
    )
    owner.add_pet(buddy)

    assert Scheduler(owner).detect_conflicts() == []


def test_detect_conflicts_returns_empty_for_no_tasks_and_deduplicates_pairs():
    owner = Owner("Alex", 60, [])
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []

    buddy = Pet("Buddy", "dog")
    first_task = Task(
        "Walk Buddy", 30, 3, scheduled_time="09:00", due_date=date(2025, 1, 1)
    )
    second_task = Task(
        "Feed Buddy", 10, 2, scheduled_time="09:15", due_date=date(2025, 1, 1)
    )
    buddy.add_task(first_task)
    buddy.add_task(second_task)
    owner.add_pet(buddy)
    owner.add_pet(buddy)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Walk Buddy" in warnings[0]
    assert "Feed Buddy" in warnings[0]
