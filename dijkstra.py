import heapq


def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}  # Initialize distances with infinity
    distances[start] = 0  # Set the distance of the start node to 0
    previous = {node: None for node in graph}  # Store the previous node in the best path

    # Use a priority queue (heap) to keep track of the nodes to visit
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:  # Reached the end node, terminate the loop
            break

        if current_distance > distances[current_node]:
            continue  # Skip if a shorter path to the current node has already been found

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct the best path from start to end
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]

    path.reverse()  # Reverse the path to get it in the correct order
    return path

