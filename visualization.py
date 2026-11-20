import os
import pandas as pd
import matplotlib.pyplot as plt
from models import ProblemInstance

DAYS_PL = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]

def plot_convergence(history_best, history_avg, greedy_cost, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.plot(history_best, label="GA - Najlepszy osobnik", color="#1f77b4", linewidth=2)
    plt.plot(history_avg, label="GA - Średnia populacji", color="#aec7e8", linestyle="--")
    plt.axhline(y=greedy_cost, color="#d62728", linestyle=":", linewidth=2, label=f"Algorytm zachłanny ({greedy_cost:.0f})")
    
    plt.title("Zbieżność algorytmu genetycznego vs algorytm zachłanny")
    plt.xlabel("Pokolenie")
    plt.ylabel("Funkcja kosztu (im mniej tym lepiej)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

def export_schedule_csv(chromosome, instance: ProblemInstance, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []
    for idx, (slot, inst_id, car_id) in enumerate(chromosome):
        stud_id = instance.lesson_to_student[idx]
        day_idx = slot // instance.slots_per_day
        hour_idx = (slot % instance.slots_per_day) + 8  # zakładamy start pracy szkoły o 8:00
        day_name = DAYS_PL[day_idx] if day_idx < len(DAYS_PL) else f"Dzień {day_idx+1}"
        
        rows.append({
            "Dzień": day_name,
            "Godzina": f"{hour_idx:02d}:00",
            "Slot_ID": slot,
            "Kursant": f"Kursant_{stud_id+1:02d}",
            "Instruktor": f"Instruktor_{inst_id+1:02d}",
            "Samochód": f"Auto_{car_id+1:02d}"
        })
    
    df = pd.DataFrame(rows).sort_values(by=["Slot_ID", "Instruktor"])
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
