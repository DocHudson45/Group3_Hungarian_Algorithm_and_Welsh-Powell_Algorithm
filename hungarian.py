import numpy as np
from typing import List, Tuple, Dict, Set

class HungarianAlgorithm:
    def __init__(self, cost_matrix: np.ndarray):
        self.original_matrix = cost_matrix.copy()
        self.matrix = cost_matrix.astype(float).copy()
        self.n = len(cost_matrix)
    
    def subtract_row_minimums(self):
        for i in range(self.n):
            row_min = np.min(self.matrix[i, :])
            self.matrix[i, :] -= row_min
    
    def subtract_column_minimums(self):
        for j in range(self.n):
            col_min = np.min(self.matrix[:, j])
            self.matrix[:, j] -= col_min

    def find_maximum_matching(self) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
        zero_positions = list(zip(*np.where(self.matrix == 0)))
        adj = [[] for _ in range(self.n)]
        for i, j in zero_positions:
            adj[i].append(j)
        match_row = [-1] * self.n
        match_col = [-1] * self.n
        def dfs(row: int, visited: Set[int]) -> bool:
            for col in adj[row]:
                if col in visited:
                    continue
                visited.add(col)
                if match_col[col] == -1 or dfs(match_col[col], visited):
                    match_row[row] = col
                    match_col[col] = row
                    return True
            return False
        for i in range(self.n):
            visited = set()
            dfs(i, visited)
        matching = [(i, match_row[i]) for i in range(self.n) if match_row[i] != -1]
        return matching, match_row, match_col
    
    def find_minimum_vertex_cover(self, match_row: List[int], match_col: List[int]) -> Tuple[Set[int], Set[int]]:
        zero_positions = list(zip(*np.where(self.matrix == 0)))
        adj = [[] for _ in range(self.n)]
        for i, j in zero_positions:
            adj[i].append(j)
        unmatched_rows = {i for i in range(self.n) if match_row[i] == -1}
        visited_rows = set()
        visited_cols = set()
        queue = list(unmatched_rows)
        while queue:
            row = queue.pop(0)
            if row in visited_rows:
                continue
            visited_rows.add(row)
            for col in adj[row]:
                if col not in visited_cols:
                    visited_cols.add(col)
                    if match_col[col] != -1:
                        queue.append(match_col[col])
        cover_rows = {i for i in range(self.n) if i not in visited_rows}
        cover_cols = visited_cols
        return cover_rows, cover_cols
    
    def adjust_matrix(self, cover_rows: Set[int], cover_cols: Set[int]) -> bool:
        min_val = float('inf')
        for i in range(self.n):
            for j in range(self.n):
                if i not in cover_rows and j not in cover_cols:
                    min_val = min(min_val, self.matrix[i, j])
        if min_val == float('inf') or min_val == 0:
            return False
        for i in range(self.n):
            for j in range(self.n):
                if i not in cover_rows and j not in cover_cols:
                    self.matrix[i, j] -= min_val
                elif i in cover_rows and j in cover_cols:
                    self.matrix[i, j] += min_val
        return True
    
    def solve(self, verbose=False) -> Tuple[List[Tuple[int, int]], float]:
        if verbose:
            print("HUNGARIAN ALGORITHM SOLUTION STEPS")
            print("\nOriginal Cost Matrix:")
            print(self.original_matrix)
            print()
        self.subtract_row_minimums()
        if verbose:
            print("Row Reduction:")
            print(self.matrix)
            print()
        self.subtract_column_minimums()
        if verbose:
            print("Column Reduction:")
            print(self.matrix)
            print()
        iteration = 0
        max_iterations = 100
        while iteration < max_iterations:
            iteration += 1
            matching, match_row, match_col = self.find_maximum_matching()
            if verbose:
                print(f"Iteration {iteration}: Matching size {len(matching)}/{self.n}")
            if len(matching) == self.n:
                if verbose:
                    print("Perfect matching found!\n")
                    print()
                break
            cover_rows, cover_cols = self.find_minimum_vertex_cover(match_row, match_col)
            num_lines = len(cover_rows) + len(cover_cols)
            if verbose:
                print(f"Cover size: {num_lines} lines")
                print(f"Covered Rows: {sorted(cover_rows)}")
                print(f"Covered Cols: {sorted(cover_cols)}")
            adjusted = self.adjust_matrix(cover_rows, cover_cols)
            if verbose:
                if adjusted:
                    print("\nAfter adjustment:")
                    print(self.matrix)
                else:
                    print("\nNo adjustment made")
                print()
            if not adjusted:
                print("Cannot make progress")
                break
        matching, match_row, match_col = self.find_maximum_matching()
        if len(matching) < self.n:
            print(f"\nOnly found {len(matching)}/{self.n} assignments.")
        total_cost = sum(self.original_matrix[i, j] for i, j in matching)
        return matching, total_cost

def create_cost_matrix_from_edges(
    nodes1: List[str],
    nodes2: List[str],
    edges: List[Tuple[str, str, float]],
    default_cost: float = float('inf')
) -> Tuple[np.ndarray, Dict[int, str], Dict[int, str]]:
    n1, n2 = len(nodes1), len(nodes2)
    n = max(n1, n2)
    cost_matrix = np.full((n, n), default_cost)
    row_labels = {i: node for i, node in enumerate(nodes1)}
    col_labels = {j: node for j, node in enumerate(nodes2)}
    node1_to_idx = {node: i for i, node in enumerate(nodes1)}
    node2_to_idx = {node: j for j, node in enumerate(nodes2)}
    for node1, node2, cost in edges:
        if node1 in node1_to_idx and node2 in node2_to_idx:
            i, j = node1_to_idx[node1], node2_to_idx[node2]
            cost_matrix[i, j] = cost
    return cost_matrix, row_labels, col_labels

def print_menu():
    print("HUNGARIAN ALGORITHM")
    print("\nChoose an input method:")
    print("1. Enter cost matrix manually")
    print("2. Enter nodes and edges")
    print("3. Exit")

def input_cost_matrix():
    print("MANUAL COST MATRIX INPUT")
    while True:
        try:
            n = int(input("\nEnter the size of the matrix (n x n): "))
            if n <= 0:
                print("Size must be positive!")
                continue
            break
        except ValueError:
            print("Please enter a valid integer!")
    print(f"\nEnter the cost matrix ({n}x{n}):")
    print("Enter each row on a separate line, with values separated by spaces.")
    print("Example for 2x2: '10 20' then '30 40'\n")
    matrix = []
    for i in range(n):
        while True:
            try:
                row_input = input(f"Row {i+1}: ")
                row = [float(x) for x in row_input.split()]
                if len(row) != n:
                    print(f"Please enter exactly {n} values!")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Please enter valid numbers separated by spaces!")
    return np.array(matrix), None, None, None

def input_nodes_and_edges():
    print("BIPARTITE GRAPH INPUT")
    print("\nEnter nodes for SET 1 (comma-separated):")
    nodes1 = [n.strip() for n in input("Set 1: ").split(',') if n.strip()]
    if not nodes1:
        print("No nodes entered!")
        return None, None, None, None
    print("\nEnter nodes for SET 2 (comma-separated):")
    nodes2 = [n.strip() for n in input("Set 2: ").split(',') if n.strip()]
    if not nodes2:
        print("No nodes entered!")
        return None, None, None, None
    print("\nEnter edges (format: node1, node2, cost), type 'done' when finished:\n")
    edges = []
    while True:
        edge_input = input(f"Edge {len(edges)+1}: ").strip()
        if edge_input.lower() == 'done':
            break
        try:
            parts = edge_input.split()
            if len(parts) != 3:
                print("Format: node1 node2 cost")
                continue
            node1, node2, cost = parts[0], parts[1], float(parts[2])
            if node1 not in nodes1:
                print(f"'{node1}' not in SET 1!")
                continue
            if node2 not in nodes2:
                print(f"'{node2}' not in SET 2!")
                continue
            edges.append((node1, node2, cost))
            print(f"Added edge: {node1} → {node2} (cost: {cost})")
        except ValueError:
            print("Invalid input format!")
    if not edges:
        print("No edges entered!")
        return None, None, None, None
    cost_matrix, row_labels, col_labels = create_cost_matrix_from_edges(
        nodes1, nodes2, edges, default_cost=999999
    )
    return cost_matrix, row_labels, col_labels, edges

def display_results(assignment, total_cost, original_matrix, row_labels=None, col_labels=None, edges=None):
    print("RESULTS")
    print("\nOPTIMAL ASSIGNMENT:")
    for i, j in sorted(assignment):
        cost = original_matrix[i, j]
        if row_labels and col_labels:
            from_node = row_labels.get(i, f"Row{i}")
            to_node = col_labels.get(j, f"Col{j}")
            print(f"  {from_node:20s} → {to_node:20s}  |  Cost: {cost:8.2f}")
        else:
            print(f"  Row {i:2d} → Column {j:2d}  |  Cost: {cost:8.2f}")
    print(f"  {'TOTAL COST':42s}  |  {total_cost:8.2f}")
    if row_labels and col_labels:
        paired_rows = {i for i, _ in assignment}
        paired_cols = {j for _, j in assignment}
        print("\nNODE COLORS AND PAIRS:")
        print(f"{'Node':<20} | {'Color':<10} | {'Paired With':<20}")
        for i, name in sorted(row_labels.items()):
            if i in paired_rows:
                j = next(j for (ri, j) in assignment if ri == i)
                paired_with = col_labels.get(j, "N/A")
                print(f"{name:<20} | {'PAIRED':<10} | {paired_with:<20}")
            else:
                print(f"{name:<20} | {'UNPAIRED':<10} | {'None':<20}")
        for j, name in sorted(col_labels.items()):
            if j in paired_cols:
                i = next(i for (i, cj) in assignment if cj == j)
                paired_with = row_labels.get(i, "N/A")
                print(f"{name:<20} | {'PAIRED':<10} | {paired_with:<20}")
            else:
                print(f"{name:<20} | {'UNPAIRED':<10} | {'None':<20}")
        if edges:
            print("\nEDGE COLORS:")
            print(f"{'From':<15} | {'To':<15} | {'Cost':<8} | {'Color':<10}")
            used_pairs = {(row_labels[i], col_labels[j]) for i, j in assignment}
            for node1, node2, cost in edges:
                color = 'PAIRED' if (node1, node2) in used_pairs else 'UNPAIRED'
                print(f"{node1:<15} | {node2:<15} | {cost:<8.2f} | {color:<10}")

def main():
    while True:
        print_menu()
        choice = input("\nChoose one (1-3): ").strip()
        if choice == '3':
            print("\nExiting the program. Goodbye!")
            break
        cost_matrix, row_labels, col_labels, edges = None, None, None, None
        if choice == '1':
            result = input_cost_matrix()
            if result[0] is not None:
                cost_matrix, row_labels, col_labels, edges = result
        elif choice == '2':
            result = input_nodes_and_edges()
            if result[0] is not None:
                cost_matrix, row_labels, col_labels, edges = result
        else:
            print("Invalid choice! Please enter 1-3.")
            continue
        if cost_matrix is None:
            continue
        verbose_input = input("\nShow solution? (y/n): ").lower()
        verbose = verbose_input == 'y'
        hungarian = HungarianAlgorithm(cost_matrix)
        assignment, total_cost = hungarian.solve(verbose=verbose)
        display_results(assignment, total_cost, cost_matrix, row_labels, col_labels, edges)
        continue_input = input("\nSolve another problem? (y/n): ").lower()
        if continue_input != 'y':
            print("\nExiting the program. Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()