import json
import os
import numpy as np
from models import ProblemInstance

def generate_instance(
    name: str,
    num_days: int,
    slots_per_day: int,
    num_instructors: int,
    num_cars: int,
    num_students: int,
    seed: int = 42
) -> ProblemInstance:
    np.random.seed(seed)
    total_slots = num_days * slots_per_day

    # Kursanci: każdy ma ok. 45% dostępnych slotów w tygodniu i 2-4 godziny jazdy
    student_avail = (np.random.rand(num_students, total_slots) < 0.45)
    # Gwarantujemy, że każdy kursant ma minimum 4 wolne sloty
    for s in range(num_students):
        if np.sum(student_avail[s]) < 4:
            free = np.random.choice(total_slots, size=4, replace=False)
            student_avail[s, free] = True

    req_hours = np.random.randint(2, 5, size=num_students).tolist()

    # Instruktorzy: dostępni przez ok. 75% czasu pracy szkoły, limit 15-25h tygodniowo
    inst_avail = (np.random.rand(num_instructors, total_slots) < 0.75)
    max_hours = np.random.randint(15, 26, size=num_instructors).tolist()

    # Budowa wektora mapującego każdą lekcję na ID kursanta
    lesson_to_student = []
    for s_id, hours in enumerate(req_hours):
        lesson_to_student.extend([s_id] * hours)

    return ProblemInstance(
        name=name,
        num_days=num_days,
        slots_per_day=slots_per_day,
        num_instructors=num_instructors,
        num_cars=num_cars,
        num_students=num_students,
        student_availability=student_avail,
        student_required_hours=req_hours,
        instructor_availability=inst_avail,
        instructor_max_hours=max_hours,
        lesson_to_student=np.array(lesson_to_student, dtype=int)
    )

def save_instance_to_json(instance: ProblemInstance, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    data = {
        "name": instance.name,
        "num_days": instance.num_days,
        "slots_per_day": instance.slots_per_day,
        "num_instructors": instance.num_instructors,
        "num_cars": instance.num_cars,
        "num_students": instance.num_students,
        "student_availability": instance.student_availability.astype(int).tolist(),
        "student_required_hours": instance.student_required_hours,
        "instructor_availability": instance.instructor_availability.astype(int).tolist(),
        "instructor_max_hours": instance.instructor_max_hours,
        "lesson_to_student": instance.lesson_to_student.tolist()
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_instance_from_json(filepath: str) -> ProblemInstance:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ProblemInstance(
        name=data["name"],
        num_days=data["num_days"],
        slots_per_day=data["slots_per_day"],
        num_instructors=data["num_instructors"],
        num_cars=data["num_cars"],
        num_students=data["num_students"],
        student_availability=np.array(data["student_availability"], dtype=bool),
        student_required_hours=data["student_required_hours"],
        instructor_availability=np.array(data["instructor_availability"], dtype=bool),
        instructor_max_hours=data["instructor_max_hours"],
        lesson_to_student=np.array(data["lesson_to_student"], dtype=int)
    )
