import numpy as np
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ProblemInstance:
    name: str
    num_days: int
    slots_per_day: int
    num_instructors: int
    num_cars: int
    num_students: int
    # Dostępność kursantów: macierz bool [num_students, total_slots]
    student_availability: np.ndarray
    # Wymagana liczba godzin dla każdego kursanta: lista int [num_students]
    student_required_hours: List[int]
    # Dostępność instruktorów: macierz bool [num_instructors, total_slots]
    instructor_availability: np.ndarray
    # Maksymalna liczba godzin w tygodniu dla instruktora: lista int [num_instructors]
    instructor_max_hours: List[int]
    # Mapowanie indeksu genu (jazdy) na ID kursanta
    lesson_to_student: np.ndarray

    @property
    def total_slots(self) -> int:
        return self.num_days * self.slots_per_day

    @property
    def total_lessons(self) -> int:
        return len(self.lesson_to_student)


def create_random_chromosome(instance: ProblemInstance) -> np.ndarray:
    """
    Tworzy losowy chromosom o wymiarach (total_lessons, 3).
    Kolumna 0: slot czasowy (0 .. total_slots - 1)
    Kolumna 1: id instruktora (0 .. num_instructors - 1)
    Kolumna 2: id auta (0 .. num_cars - 1)
    """
    n = instance.total_lessons
    chromosome = np.zeros((n, 3), dtype=int)
    
    # Sprytna inicjalizacja: losujemy slot z dostępnych dla danego kursanta (jeśli ma dostępne)
    for idx, student_id in enumerate(instance.lesson_to_student):
        valid_slots = np.where(instance.student_availability[student_id])[0]
        if len(valid_slots) > 0:
            chromosome[idx, 0] = np.random.choice(valid_slots)
        else:
            chromosome[idx, 0] = np.random.randint(0, instance.total_slots)
            
    chromosome[:, 1] = np.random.randint(0, instance.num_instructors, size=n)
    chromosome[:, 2] = np.random.randint(0, instance.num_cars, size=n)
    return chromosome