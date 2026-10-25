"""Core classes and scheduling logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta


class Owner:
    """Represent a pet owner, their availability, preferences, and pets."""

    def __init__(
        self,
        name: str,
        available_time: int,
        preferences: list[str],
    ) -> None:
        """Create an owner with basic details and scheduling preferences."""
        self.name = name
        self.available_time = available_time
        self.preferences = preferences
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the care tasks for all of this owner's pets."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Filter this owner's tasks by pet and completion state.

        Args:
            pet_name: Optional exact pet name to include.
            completed: Optional completion state; True means completed and
                False means pending.

        Returns:
            A new list of matching Task objects.
        """
        matching_tasks: list[Task] = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            matching_tasks.extend(
                task
                for task in pet.get_tasks()
                if completed is None or task.completed is completed
            )
        return matching_tasks

    def set_available_time(self, available_time: int) -> None:
        """Set the amount of time the owner has available."""
        self.available_time = available_time

    def update_preferences(self, preferences: list[str]) -> None:
        """Update the owner's care preferences."""
        self.preferences = preferences


@dataclass
class Pet:
    """Represent a pet and the care tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        return list(self.tasks)

    def complete_task(
        self,
        task: Task,
        completed_on: date | None = None,
    ) -> Task | None:
        """Complete a task and add its next daily or weekly occurrence.

        Args:
            task: A task belonging to this pet.
            completed_on: Optional date used when the task has no due date.

        Returns:
            The new pending occurrence, or None for a repeated or non-recurring
            task.
        """
        if not any(existing_task is task for existing_task in self.tasks):
            raise ValueError("The task does not belong to this pet.")
        if task.completed:
            return None

        task.mark_completed()
        recurrence = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
        }.get(task.frequency.lower())
        if recurrence is None:
            return None

        base_date = task.due_date or completed_on or date.today()
        next_task = Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            scheduled_time=task.scheduled_time,
            due_date=base_date + recurrence,
        )
        self.add_task(next_task)
        return next_task


@dataclass
class Task:
    """Represent one care task and its scheduling details."""

    title: str
    duration_minutes: int
    priority: int
    frequency: str = "daily"
    completed: bool = False
    scheduled_time: str | None = None
    due_date: date | None = None

    def update_task(
        self,
        title: str,
        duration_minutes: int,
        priority: int,
        frequency: str | None = None,
    ) -> None:
        """Update the task's details."""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        if frequency is not None:
            self.frequency = frequency

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    """Create a daily care plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner."""
        self.owner = owner
        self.daily_plan: list[Task] = []
        self.plan_explanation: list[str] = []

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority, highest first.

        Args:
            tasks: Tasks to sort.

        Returns:
            A new list ordered by descending priority.
        """
        return sorted(tasks, key=lambda task: task.priority, reverse=True)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by HH:MM scheduled time, placing untimed tasks last.

        Args:
            tasks: Tasks to sort.

        Returns:
            A new list ordered from earliest to latest scheduled time.
        """
        return sorted(
            tasks,
            key=lambda task: (
                task.scheduled_time is None,
                task.scheduled_time or "",
            ),
        )

    def detect_conflicts(self) -> list[str]:
        """Find overlapping task intervals for the same date.

        Checks pending tasks owned by all pets. Tasks without a valid date,
        HH:MM time, or positive duration are ignored.

        Returns:
            One readable warning per overlapping pair, or an empty list.
        """
        scheduled_tasks: list[tuple[Task, datetime, datetime]] = []
        for task in self.owner.get_all_tasks():
            if (
                task.completed
                or not isinstance(task.due_date, date)
                or task.scheduled_time is None
                or not isinstance(task.scheduled_time, str)
                or not isinstance(task.duration_minutes, int)
                or task.duration_minutes <= 0
            ):
                continue
            try:
                start_time = datetime.strptime(task.scheduled_time, "%H:%M").time()
            except ValueError:
                continue
            if start_time.strftime("%H:%M") != task.scheduled_time:
                continue

            try:
                start = datetime.combine(task.due_date, start_time)
                end = start + timedelta(minutes=task.duration_minutes)
            except (OverflowError, TypeError, ValueError):
                continue
            scheduled_tasks.append((task, start, end))

        warnings: list[str] = []
        warned_pairs: set[tuple[int, int]] = set()
        for first_index, (first_task, first_start, first_end) in enumerate(
            scheduled_tasks
        ):
            for second_index in range(first_index + 1, len(scheduled_tasks)):
                second_task, second_start, second_end = scheduled_tasks[second_index]
                pair = tuple(sorted((id(first_task), id(second_task))))
                if pair in warned_pairs or first_task is second_task:
                    continue
                if first_start.date() != second_start.date():
                    continue
                if first_start < second_end and second_start < first_end:
                    warnings.append(
                        f"Scheduling conflict: {first_task.title} "
                        f"({first_start:%H:%M}-{first_end:%H:%M}) overlaps with "
                        f"{second_task.title} "
                        f"({second_start:%H:%M}-{second_end:%H:%M})."
                    )
                    warned_pairs.add(pair)
        return warnings

    def generate_plan(self) -> list[Task]:
        """Select pending tasks that fit within the owner's available time."""
        self.daily_plan = []
        self.plan_explanation = []
        available_time = self.owner.available_time
        remaining_time = max(available_time, 0)
        tasks = self.owner.get_all_tasks()

        if not tasks:
            self.plan_explanation.append("No care tasks are available.")
            return self.daily_plan

        for task in self.sort_tasks(tasks):
            if task.completed:
                self.plan_explanation.append(
                    f"Skipped '{task.title}': it is already completed."
                )
            elif task.duration_minutes <= 0:
                self.plan_explanation.append(
                    f"Skipped '{task.title}': its duration must be positive."
                )
            elif task.duration_minutes <= remaining_time:
                self.daily_plan.append(task)
                remaining_time -= task.duration_minutes
                self.plan_explanation.append(
                    f"Selected '{task.title}' (priority {task.priority}): "
                    "it fits in the remaining time."
                )
            else:
                self.plan_explanation.append(
                    f"Skipped '{task.title}' (priority {task.priority}): "
                    "not enough available time."
                )

        if not self.daily_plan and any(
            not task.completed and task.duration_minutes > 0 for task in tasks
        ):
            self.plan_explanation.append(
                f"No tasks fit within {available_time} minutes of available time."
            )
        return list(self.daily_plan)

    def explain_plan(self) -> str:
        """Return the reasons tasks were selected or skipped."""
        return "\n".join(self.plan_explanation)