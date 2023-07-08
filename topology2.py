import random
import subprocess
import heapq
import os

from mininet.topo import Topo


# from dijkstra import dijkstra

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


class MyTopo(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        h5 = self.addHost('h5', ip='10.0.0.5/24')
        h6 = self.addHost('h6', ip='10.0.0.6/24')
        h7 = self.addHost('h7', ip='10.0.0.7/24')
        h8 = self.addHost('h8', ip='10.0.0.8/24')

        # Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')

        # keys are the host/switch and values are list of tuples that first argument is the neighbor and second
        # argument is weight of the link. if 2 host/switch has no link to each other it means the weight is infinity
        graph = {
            h1: [], h2: [], h3: [], h4: [], h5: [], h6: [], h7: [], h8: [],
            s1: [], s2: [], s3: [], s4: [], s5: [], s6: [], s7: [], s8: []
        }

        ports = {
            h1: {}, h2: {}, h3: {}, h4: {}, h5: {}, h6: {}, h7: {}, h8: {},
            s1: {}, s2: {}, s3: {}, s4: {}, s5: {}, s6: {}, s7: {}, s8: {}
        }

        for i in ports.keys():
            ports[i]['port_num'] = 1

        # Links
        self.add_link(h1, s1, graph, ports)
        self.add_link(h2, s2, graph, ports)
        self.add_link(h3, s3, graph, ports)
        self.add_link(h4, s4, graph, ports)
        self.add_link(h5, s5, graph, ports)
        self.add_link(h6, s6, graph, ports)
        self.add_link(h7, s7, graph, ports)
        self.add_link(h8, s8, graph, ports)

        self.add_link(s1, s8, graph, ports)
        self.add_link(s3, s8, graph, ports)
        self.add_link(s6, s8, graph, ports)
        self.add_link(s7, s8, graph, ports)
        self.add_link(s1, s3, graph, ports)
        self.add_link(s6, s3, graph, ports)
        self.add_link(s4, s3, graph, ports)
        self.add_link(s6, s5, graph, ports)
        self.add_link(s2, s5, graph, ports)
        self.add_link(s4, s5, graph, ports)
        self.add_link(s7, s5, graph, ports)
        self.add_link(s2, s4, graph, ports)
        self.add_link(s7, s4, graph, ports)
        self.add_link(s2, s7, graph, ports)

        path = dijkstra(graph=graph, start='h1', end='h2')

        file = open('command.sh', 'w+')
        for i in range(1, len(path) - 1):
            flow_command = "in_port={},nw_src=10.0.0.7,nw_dst=10.0.0.8 actions=output:{}".format(
                ports[path[i]][path[i - 1]],
                ports[path[i]][path[i + 1]])
            command = 'sudo ovs-ofctl add-flow {} "{}"\n'.format(path[i], flow_command)
            file.write(command)
            subprocess.call(command, shell=True)
            reverse_flow_command = "in_port={}, nw_src=10.0.0.8,nw_dst=10.0.0.7 actions=output:{}".format(
                ports[path[i]][path[i + 1]],
                ports[path[i]][path[i - 1]])
            reverse_command = 'sudo ovs-ofctl add-flow {} "{}" \n'.format(path[i], reverse_flow_command)
            file.write(reverse_command)
            subprocess.call(command, shell=True)

        file.close()

    def add_link(self, host1, host2, graph, ports):
        wight = random.randint(1, 10)
        graph[host1].append((host2, wight))
        graph[host2].append((host1, wight))

        ports[host1][host2] = ports[host1]['port_num']
        ports[host1]['port_num'] += 1

        ports[host2][host1] = ports[host2]['port_num']
        ports[host2]['port_num'] += 1

        self.addLink(host1, host2)


topos = {'mytopo': (lambda: MyTopo())}
