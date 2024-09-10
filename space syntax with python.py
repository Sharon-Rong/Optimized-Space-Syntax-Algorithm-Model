import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import networkx as nx
from collections import deque
import numpy as np


road_segments = gpd.read_file('D:/XXX.shp')


road_segments.crs = 'EPSG:32651'


gov_data = pd.read_csv('D:/XXX.csv')


road_segments = road_segments.merge(gov_data, on='FID_1', how='left')

road_segments['geometry'] = road_segments.apply(lambda row: LineString([(row['x1'], row['y1']), (row['x2'], row['y2'])]), axis=1)


buffer_distance = 0.0001
road_segments['buffered'] = road_segments['geometry'].buffer(buffer_distance)


def find_neighbors(row, road_segments):
    sindex = road_segments.sindex
    possible_matches_index = list(sindex.intersection(row['buffered'].bounds))
    possible_matches = road_segments.iloc[possible_matches_index]
    precise_matches = possible_matches[possible_matches.intersects(row['buffered'])]
    neighbors = precise_matches.index.tolist()
    neighbors.remove(row.name)
    return tuple(neighbors)

road_segments['neighbor_FID_1'] = road_segments.apply(lambda row: find_neighbors(row, road_segments), axis=1)


def bfs_max_steps(graph, start_node, max_steps):
    visited = set()
    queue = deque([(start_node, 0)])
    result = []

    while queue:
        node, steps = queue.popleft()
        visited.add(node)
        result.append((node, steps))

        if steps < max_steps:
            if node in graph:
                neighbors = graph[node]
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, steps + 1))
                        visited.add(neighbor)
    return result


def compute_counts(segment_id, steps_data, road_segments, alpha, alpha_after_5):
    total_counts = { 'Count_shop': 0, 'Count_pop': 0}
    for neighbor_id, distance in steps_data:
        for count_type in total_counts.keys():
            count = road_segments.loc[neighbor_id, count_type]
            if distance <= 5:
                total_counts[count_type] += (alpha ** distance) * count
            else:
                total_counts[count_type] += (alpha_after_5 ** (distance - 5)) * count
    return total_counts


def main(max_steps, alpha, alpha_after_5):

    graph = nx.Graph()
    for _, row in road_segments.iterrows():
        neighbors = row['neighbor_FID_1']
        for neighbor in neighbors:
            graph.add_edge(row['FID_1'], neighbor)


    total_counts = { 'Count_shop': {}, 'Count_pop': {}}
    for start_segment in road_segments['FID_1']:
        steps_data = bfs_max_steps(graph, start_segment, max_steps)
        counts = compute_counts(start_segment, steps_data, road_segments, alpha, alpha_after_5)
        for count_type in counts.keys():
            total_counts[count_type][start_segment] = counts[count_type]


    for count_type in total_counts.keys():
        road_segments['log_'+count_type] = np.log10(np.array(list(total_counts[count_type].values())) + 1)


    road_segments[['FID_1', 'log_Count_shop', 'log_Count_pop']].to_excel('fpop_qing60.xlsx', index=False)

if __name__ == "__main__":
    max_steps =60
    alpha = 1.0
    alpha_after_5 = 0.9
    main(max_steps, alpha, alpha_after_5)
