import numpy as np
from typing import Tuple, Dict
from models import ProblemInstance

# Wagi kar - zgodnie z planem awaryjnym w karcie tematu:
# Naruszenia twarde mają ogromną wagę, żeby algorytm najpierw usunął konflikty,
# a dopiero potem optymalizował okienka (ograniczenie miękkie).
PENALTY_HARD = 1000.0
PENALTY_SOFT_GAP = 10.0

def evaluate_chromosome(chromosome: np.ndarray, instance: ProblemInstance) -> Tuple[float, Dict]:
    """
    Oblicza całkowity koszt (im mniej, tym lepiej; 0 = brak konfliktów i brak okienek)
    oraz zwraca szczegółowy słownik metryk do walidacji.
    """
    slots = chromosome[:, 0]
    instructors = chromosome[:, 1]
    cars = chromosome[:, 2]
    students = instance.lesson_to_student

    # 1. Konflikty twarde (podwójne rezerwacje w tym samym slocie)
    instructor_conflicts = 0
    car_conflicts = 0
    student_conflicts = 0
    
    # Grupowanie po slotach
    for s in range(instance.total_slots):
        in_slot = np.where(slots == s)[0]
        if len(in_slot) > 1:
            # Jeśli w jednym slocie jest k lekcji, a unikalnych zasobów jest m, to mamy (k - m) kolizji
            inst_in_slot = instructors[in_slot]
            instructor_conflicts += len(inst_in_slot) - len(np.unique(inst_in_slot))
            
            cars_in_slot = cars[in_slot]
            car_conflicts += len(cars_in_slot) - len(np.unique(cars_in_slot))
            
            stud_in_slot = students[in_slot]
            student_conflicts += len(stud_in_slot) - len(np.unique(stud_in_slot))

    # 2. Dostępność kursantów i instruktorów
    student_unavail = np.sum(~instance.student_availability[students, slots])
    instructor_unavail = np.sum(~instance.instructor_availability[instructors, slots])

    # 3. Przekroczenie limitu godzin instruktora w tygodniu
    inst_hours = np.bincount(instructors, minlength=instance.num_instructors)
    max_hours = np.array(instance.instructor_max_hours)
    overtime_violations = int(np.sum(np.maximum(0, inst_hours - max_hours)))

    hard_violations = int(
        instructor_conflicts + car_conflicts + student_conflicts +
        student_unavail + instructor_unavail + overtime_violations
    )

    # 4. Ograniczenie miękkie: Okienka instruktorów (czas oczekiwania)
    total_gaps = 0
    active_instructor_days = 0

    for inst_id in range(instance.num_instructors):
        inst_slots = slots[instructors == inst_id]
        if len(inst_slots) == 0:
            continue
        for day in range(instance.num_days):
            day_start = day * instance.slots_per_day
            day_end = (day + 1) * instance.slots_per_day
            day_slots = np.sort(inst_slots[(inst_slots >= day_start) & (inst_slots < day_end)])
            
            if len(day_slots) > 0:
                active_instructor_days += 1
                if len(day_slots) > 1:
                    # Liczba slotów od pierwszej do ostatniej jazdy minus liczba faktycznych jazd
                    span = (day_slots[-1] - day_start) - (day_slots[0] - day_start) + 1
                    gaps = span - len(day_slots)
                    total_gaps += int(gaps)

    avg_daily_gap = (total_gaps / active_instructor_days) if active_instructor_days > 0 else 0.0

    # Całkowity koszt
    total_cost = (hard_violations * PENALTY_HARD) + (total_gaps * PENALTY_SOFT_GAP)

    metrics = {
        "total_cost": float(total_cost),
        "hard_violations": hard_violations,
        "instructor_conflicts": int(instructor_conflicts),
        "car_conflicts": int(car_conflicts),
        "student_conflicts": int(student_conflicts),
        "student_unavail": int(student_unavail),
        "instructor_unavail": int(instructor_unavail),
        "overtime_violations": overtime_violations,
        "total_gaps": int(total_gaps),
        "avg_daily_gap": round(float(avg_daily_gap), 2),
        # W tym kodowaniu wszystkie wymagane godziny są zawsze w chromosomie,
        # więc efektywne pokrycie liczymy jako odsetek lekcji bez naruszeń twardych
        "valid_coverage_pct": round(max(0.0, (1.0 - hard_violations / instance.total_lessons) * 100), 1)
    }

    return float(total_cost), metrics
