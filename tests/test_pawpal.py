from pawpal_system import Pet, Task


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
