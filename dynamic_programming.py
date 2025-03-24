from functools import lru_cache

# Adjacency matrix representing the graph (distances between cities)
graph = [
    [0, 12, 10, 0, 0, 0, 12],  # City 1
    [12, 0, 8, 11, 0, 0, 0],   # City 2
    [10, 8, 0, 8, 3, 0, 9],    # City 3
    [0, 11, 8, 0, 11, 10, 0],  # City 4
    [0, 0, 3, 11, 0, 6, 7],    # City 5
    [0, 0, 0, 10, 6, 0, 9],    # City 6
    [12, 0, 9, 0, 7, 9, 0]     # City 7
]

N = len(graph)  # Number of cities
START_CITY = 0  # City 1 (0-based index)

# Dictionary to store the optimal path choices
path_cache = {}

@lru_cache(None)
def tsp(mask, pos):
    """
    Recursively computes the shortest path visiting all cities using DP + Bitmasking.
    
    Args:
        mask (int): Bitmask representing visited cities.
        pos (int): Current city position.
    
    Returns:
        int: Minimum travel cost from current position covering all cities.
    """
    # Base case: If all cities are visited, return cost to return to start
    if mask == (1 << N) - 1:
        return graph[pos][START_CITY] if graph[pos][START_CITY] > 0 else float('inf')
    
    min_cost = float('inf')  # Stores the shortest distance found
    best_next = None  # Stores the best next city to visit

    # Try visiting all other cities
    for next_city in range(N):
        if (mask & (1 << next_city)) == 0 and graph[pos][next_city] > 0:
            # Mark city as visited by updating the mask
            new_mask = mask | (1 << next_city)
            
            # Compute the cost of visiting next_city
            cost = graph[pos][next_city] + tsp(new_mask, next_city)
            
            # Update minimum cost and best next city if this path is better
            if cost < min_cost:
                min_cost = cost
                best_next = next_city
    
    # Store the best next city for reconstructing the path later
    path_cache[(mask, pos)] = best_next
    return min_cost

def find_optimal_path():
    """
    Reconstructs the optimal path from the DP table.
    
    Returns:
        tuple: (Optimal path as a list, Minimum travel cost)
    """
    mask = 1 << START_CITY  # Mark City 1 as visited
    pos = START_CITY  # Start from City 1
    path = [START_CITY + 1]  # Store the path (1-based index)
    total_cost = tsp(mask, pos)  # Get the shortest travel cost

    # Reconstruct the path using the stored decisions
    while len(path) < N:
        next_city = path_cache.get((mask, pos))
        if next_city is None or graph[pos][next_city] == 0:
            break  # Stop if no valid move

        path.append(next_city + 1)  # Convert to 1-based index
        mask |= (1 << next_city)  # Mark city as visited
        pos = next_city  # Move to the next city

    # Ensure we return to the starting city if a valid path exists
    if graph[pos][START_CITY] > 0:
        path.append(START_CITY + 1)
    
    return path, total_cost

# Compute the optimal tour
optimal_path, shortest_distance = find_optimal_path()

# Output results
print("Optimal Tour Path:", " ".join(map(str, optimal_path)))
print("Optimal Tour Distance:", shortest_distance)