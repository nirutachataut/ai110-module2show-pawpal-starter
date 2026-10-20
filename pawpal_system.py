"""Core classes and scheduling logic."""

from __future__ import annotations

from dataclasses import dataclass, field


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


@dataclass
class Task:
    """Represent one care task and its scheduling details."""

    title: str
    duration_minutes: int
    priority: int
    frequency: str = "daily"
    completed: bool = False

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
        """Return tasks ordered from highest to lowest priority."""
        return sorted(tasks, key=lambda task: task.priority, reverse=True)

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