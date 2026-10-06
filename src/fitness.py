# src/fitness.py
from typing import List
from src.models import Booking # lub z miejsca, gdzie zdefiniujecie Booking

def calculate_fitness(chromosome: List[Booking], instance_data: dict) -> float:
    """
    Główna funkcja oceny (Patryk).
    Zwraca całkowitą wartość kary. Czym MNIEJ, tym LEPIEJ (0 = idealny grafik).
    """
    total_penalty = 0.0
    
    # 1. Obliczanie kar za ograniczenia twarde (Hard Constraints)
    hard_penalties = check_collisions(chromosome) + check_availabilities(chromosome, instance_data)
    
    # 2. Obliczanie kar za ograniczenia miękkie (Soft Constraints)
    soft_penalties = check_instructor_gaps(chromosome) + check_missing_hours(chromosome, instance_data)
    
    total_penalty = hard_penalties + soft_penalties
    return total_penalty


def check_collisions(chromosome: List[Booking]) -> float:
    penalty = 0.0
    # Słowniki do wykrywania dubli w danym slocie (dzien, godzina)
    instructor_slots = set()
    car_slots = set()
    
    for booking in chromosome:
        slot_key = (booking.day, booking.timeslot)
        
        # Kolizja instruktora
        if (booking.instructor_id, *slot_key) in instructor_slots:
            penalty += 10000  # Bardzo duża kara!
        else:
            instructor_slots.add((booking.instructor_id, *slot_key))
            
        # Kolizja auta
        if (booking.car_id, *slot_key) in car_slots:
            penalty += 10000
        else:
            car_slots.add((booking.car_id, *slot_key))
            
    return penalty


def check_availabilities(chromosome: List[Booking], instance_data: dict) -> float:
    # Tutaj sprawdzasz czy kursant jeździ wtedy kiedy ma czas
    return 0.0


def check_instructor_gaps(chromosome: List[Booking]) -> float:
    # Tutaj wyliczasz okienka u instruktorów
    return 0.0


def check_missing_hours(chromosome: List[Booking], instance_data: dict) -> float:
    # Sprawdzanie czy pokrycie zapotrzebowania wynosi >= 95%
    return 0.0
