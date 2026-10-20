"""Class skeletons for the PawPal+ pet care scheduling system."""

from __future__ import annotations

from dataclasses import dataclass, field


class Owner:
    """Represent a pet owner and their availability and preferences."""

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

    def set_available_time(self, available_time: int) -> None:
        """Set the amount of time the owner has available."""
        pass

    def update_preferences(self, preferences: list[str]) -> None:
        """Update the owner's care preferences."""
        pass


@dataclass
class Pet:
    """Represent a pet and the care tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass


@dataclass
class Task:
    """Represent one care task for a pet."""

    title: str
    duration_minutes: int
    priority: int

    def update_task(
        self,
        title: str,
        duration_minutes: int,
        priority: int,
    ) -> None:
        """Update the task's details."""
        pass


class Scheduler:
    """Represent a daily plan made from tasks and available time."""

    def __init__(self) -> None:
        """Create a scheduler with an empty daily plan."""
        self.daily_plan: list[Task] = []

    def sort_tasks(self, tasks: list[Task]) -> None:
        """Provide a place to define task ordering."""
        pass

    def generate_plan(self, owner: Owner, tasks: list[Task]) -> None:
        """Provide a place to create a plan using tasks and owner availability."""
        pass

    def explain_plan(self) -> None:
        """Provide a place to explain the daily plan."""
        pass