from collections import defaultdict

def read_nodes():
    raw = input("Enter nodes: ").strip()
    if "," in raw:
        parts = [p.strip() for p in raw.split(",") if p.strip()]
    else:
        parts = [p.strip() for p in raw.split() if p.strip()]
    if not parts:
        raise ValueError("No nodes provided.")
    return parts

def read_edges(nodes):
    node_set = set(nodes)
    edges = []
    print("Enter edges as: u v cost")
    while True:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        if len(parts) != 3:
            print("  !! Please enter exactly three values: u v cost")
            continue
        u, v, cost = parts
        if u not in node_set or v not in node_set:
            print("  !! u and v must be existing nodes")
            continue
        try:
            cost_val = int(cost)
        except ValueError:
            try:
                cost_val = float(cost)
            except ValueError:
                print("  !! cost must be a number")
                continue
        edges.append((u, v, cost_val))
    return edges

def build_adj(nodes, edges):
    adj = {n: set() for n in nodes}
    for u, v, _c in edges:
        if u == v:  # ignore self-loops for coloring
            continue
        adj[u].add(v)
        adj[v].add(u)
    return adj

def welsh_powell(nodes, edges):
    """
    Welsh–Powell vertex coloring:
      1) compute degrees
      2) sort vertices by degree descending
      3) assign color 1 to the first vertex; then in the same pass, assign color 1
         to any remaining vertex not adjacent to any vertex already colored 1
      4) start a new color and repeat for uncolored vertices until all colored
    """
    adj = build_adj(nodes, edges)
    degrees = {v: len(adj[v]) for v in nodes}
    ordered = sorted(nodes, key=lambda v: (-degrees[v], str(v)))

    color_of = {v: 0 for v in nodes}
    current_color = 0

    uncolored = set(ordered)
    while uncolored:
        current_color += 1
        last_colored_this_round = []
        for v in ordered:
            if v in uncolored:
                if all((nbr not in last_colored_this_round) for nbr in adj[v]):
                    color_of[v] = current_color
                    last_colored_this_round.append(v)
        uncolored.difference_update(last_colored_this_round)

    return color_of, current_color

def main():
    nodes = read_nodes()
    edges = read_edges(nodes)
    color_of, num_colors = welsh_powell(nodes, edges)
    
    print(f"Colors used: {num_colors}")
    print("Node colors:")
    for v in sorted(nodes, key=str):
        print(f"  {v}: color {color_of[v]}")

    print("\nEdges (u, v, cost):")
    for (u, v, c) in edges:
        print(f"  ({u}, {v}, {c})")

if __name__ == "__main__":
    main()
