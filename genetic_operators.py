import numpy as np
from typing import Tuple, List, Dict
from models import ProblemInstance, create_random_chromosome
from evaluation import evaluate_chromosome

def tournament_selection(population: List[np.ndarray], fitnesses: np.ndarray, k: int = 3) -> np.ndarray:
    """Wybiera najlepszego osobnika spośród k losowo wybranych (minimalizacja kosztu)."""
    indices = np.random.choice(len(population), size=k, replace=False)
    best_idx = indices[np.argmin(fitnesses[indices])]
    return population[best_idx].copy()

def crossover(parent1: np.ndarray, parent2: np.ndarray, cx_prob: float = 0.8) -> Tuple[np.ndarray, np.ndarray]:
    """Krzyżowanie jednopunktowe na poziomie całych lekcji (wierszy macierzy)."""
    if np.random.rand() > cx_prob or len(parent1) < 2:
        return parent1.copy(), parent2.copy()
    
    point = np.random.randint(1, len(parent1))
    child1 = np.vstack((parent1[:point], parent2[point:]))
    child2 = np.vstack((parent2[:point], parent1[point:]))
    return child1, child2

def mutate(chromosome: np.ndarray, instance: ProblemInstance, mut_prob: float = 0.05) -> np.ndarray:
    """Mutacja genów: zmienia losowo slot, instruktora lub samochód dla wybranych lekcji."""
    mutant = chromosome.copy()
    for i in range(len(mutant)):
        if np.random.rand() < mut_prob:
            gene_to_mutate = np.random.randint(0, 3)
            if gene_to_mutate == 0:
                student_id = instance.lesson_to_student[i]
                valid_slots = np.where(instance.student_availability[student_id])[0]
                if len(valid_slots) > 0 and np.random.rand() < 0.8:
                    mutant[i, 0] = np.random.choice(valid_slots)
                else:
                    mutant[i, 0] = np.random.randint(0, instance.total_slots)
            elif gene_to_mutate == 1:
                mutant[i, 1] = np.random.randint(0, instance.num_instructors)
            else:
                mutant[i, 2] = np.random.randint(0, instance.num_cars)
    return mutant

def run_genetic_algorithm(
    instance: ProblemInstance,
    pop_size: int = 100,
    generations: int = 300,
    cx_prob: float = 0.8,
    mut_prob: float = 0.05,
    tournament_k: int = 3,
    elitism: int = 2
) -> Dict:
    """Główna pętla ewolucyjna z elitaryzmem."""
    population = [create_random_chromosome(instance) for _ in range(pop_size)]
    history_best = []
    history_avg = []

    for gen in range(generations):
        fitnesses = np.array([evaluate_chromosome(ind, instance)[0] for ind in population])
        
        best_idx = np.argmin(fitnesses)
        history_best.append(float(fitnesses[best_idx]))
        history_avg.append(float(np.mean(fitnesses)))

        # Elitaryzm - przenosimy najlepszych bez zmian
        sorted_indices = np.argsort(fitnesses)
        new_population = [population[idx].copy() for idx in sorted_indices[:elitism]]

        while len(new_population) < pop_size:
            p1 = tournament_selection(population, fitnesses, tournament_k)
            p2 = tournament_selection(population, fitnesses, tournament_k)
            c1, c2 = crossover(p1, p2, cx_prob)
            new_population.append(mutate(c1, instance, mut_prob))
            if len(new_population) < pop_size:
                new_population.append(mutate(c2, instance, mut_prob))

        population = new_population

    final_fitnesses = np.array([evaluate_chromosome(ind, instance)[0] for ind in population])
    best_idx = np.argmin(final_fitnesses)
    best_chromosome = population[best_idx]
    best_cost, metrics = evaluate_chromosome(best_chromosome, instance)

    return {
        "best_chromosome": best_chromosome,
        "best_cost": best_cost,
        "metrics": metrics,
        "history_best": history_best,
        "history_avg": history_avg
    }