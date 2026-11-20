import numpy as np
from typing import Dict
from models import ProblemInstance
from evaluation import evaluate_chromosome

def run_greedy_algorithm(instance: ProblemInstance) -> Dict:
    """
    Przydziela lekcje po kolei do pierwszego wolnego slotu, instruktora i auta.
    Jeśli nie znajdzie bezkonfliktowego przydziału, wpisuje pierwszy dostępny slot kursanta (generując konflikt).
    """
    n = instance.total_lessons
    chromosome = np.zeros((n, 3), dtype=int)

    used_inst = set()   # (slot, inst_id)
    used_car = set()    # (slot, car_id)
    used_stud = set()   # (slot, stud_id)
    inst_hours = np.zeros(instance.num_instructors, dtype=int)

    for idx, stud_id in enumerate(instance.lesson_to_student):
        assigned = False
        valid_slots = np.where(instance.student_availability[stud_id])[0]

        for slot in valid_slots:
            if (slot, stud_id) in used_stud:
                continue
            
            # Szukamy wolnego auta
            free_car = None
            for c in range(instance.num_cars):
                if (slot, c) not in used_car:
                    free_car = c
                    break
            if free_car is None:
                continue

            # Szukamy wolnego instruktora z zapasem godzin
            free_inst = None
            for i in range(instance.num_instructors):
                if (instance.instructor_availability[i, slot] and
                        (slot, i) not in used_inst and
                        inst_hours[i] < instance.instructor_max_hours[i]):
                    free_inst = i
                    break
            if free_inst is None:
                continue

            # Sukces - rezerwujemy
            chromosome[idx] = [slot, free_inst, free_car]
            used_stud.add((slot, stud_id))
            used_inst.add((slot, free_inst))
            used_car.add((slot, free_car))
            inst_hours[free_inst] += 1
            assigned = True
            break

        if not assigned:
            # Fallback zachłanny: bierze pierwszy możliwy slot kursanta mimo braku zasobów
            fallback_slot = valid_slots[0] if len(valid_slots) > 0 else 0
            chromosome[idx] = [fallback_slot, 0, 0]

    cost, metrics = evaluate_chromosome(chromosome, instance)
    return {
        "best_chromosome": chromosome,
        "best_cost": cost,
        "metrics": metrics
    }