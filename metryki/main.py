from data_generator import generate_instance, save_instance_to_json, load_instance_from_json
from greedy_solver import run_greedy_algorithm
from genetic_operators import run_genetic_algorithm
from visualization import plot_convergence, export_schedule_csv

def main():
    print("=== 1. Generowanie instancji danych ===")
    small_inst = generate_instance("mala_instancja", num_days=2, slots_per_day=8, num_instructors=3, num_cars=2, num_students=6, seed=10)
    large_inst = generate_instance("duza_instancja", num_days=7, slots_per_day=12, num_instructors=12, num_cars=8, num_students=35, seed=42)
    
    save_instance_to_json(small_inst, "data/small_instance.json")
    save_instance_to_json(large_inst, "data/large_instance.json")
    print(f"Zapisano instancje. Duża instancja ma {large_inst.total_lessons} jazd do zaplanowania.\n")

    # Wczytujemy dużą instancję (12 instruktorów, 8 aut, 35 kursantów)
    instance = load_instance_from_json("data/large_instance.json")

    print("=== 2. Uruchomienie algorytmu zachłannego (Baseline) ===")
    greedy_res = run_greedy_algorithm(instance)
    print("Wynik zachłanny:", greedy_res["metrics"], "\n")

    print("=== 3. Uruchomienie algorytmu genetycznego (GA) ===")
    ga_res = run_genetic_algorithm(
        instance,
        pop_size=120,
        generations=400,
        cx_prob=0.85,
        mut_prob=0.04,
        tournament_k=3
    )
    print("Wynik GA:", ga_res["metrics"], "\n")

    print("=== 4. Zapis wyników i wykresów ===")
    plot_convergence(
        ga_res["history_best"],
        ga_res["history_avg"],
        greedy_res["best_cost"],
        "results/convergence.png"
    )
    export_schedule_csv(ga_res["best_chromosome"], instance, "results/grafik_tygodniowy.csv")
    print("Gotowe! Wykres zapisano w results/convergence.png, a grafik w results/grafik_tygodniowy.csv")

if __name__ == "__main__":
    main()
