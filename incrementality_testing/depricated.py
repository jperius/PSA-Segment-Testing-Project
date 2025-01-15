'''
import plotly.express as px
import pandas as pd
import json

with open('dma_boundaries.geojson', 'r') as f:
    escaped_json_str = f.read()

# Remove one level of string encoding
unescaped_json_str = json.loads(escaped_json_str)
dma_geojson = json.loads(unescaped_json_str)

names_and_groups_df['dma_code'] = names_and_groups_df['dma_code'].astype(str)
for feature in dma_geojson['features']:
    feature['properties']['dma'] = str(feature['properties']['dma'])

honolulu_geojson = [feature for feature in dma_geojson['features'] if feature['properties']['dma'] == '744']
anchorage_geojson = [feature for feature in dma_geojson['features'] if feature['properties']['dma'] == '743']
print("Honolulu in GeoJSON:", honolulu_geojson)
print("Anchorage in GeoJSON:", anchorage_geojson)

fig = px.choropleth_mapbox(
    names_and_groups_df,
    geojson=dma_geojson,
    locations='dma_code',
    color='group',
    featureidkey='properties.dma',
    color_discrete_map={
        'group_a': 'blue',
        'group_b': 'orange',
        'group_c': 'green'
    },
    mapbox_style="carto-positron",
    zoom=3,  # Adjust as needed
    center={"lat": 37.0902, "lon": -95.7129},
    hover_data={'dma_code': True, 'dma_description': True, 'group': True}
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
'''


'''
from sklearn.metrics import pairwise_distances

distances = pairwise_distances(final_df_pca['coords'].to_list(), metric='euclidean')
distances_df = pd.DataFrame(distances)
distances_df

group_a = set()
group_b = set()
group_c = set()
used_indices = set()

random_indices = np.random.permutation(distances_df.index)

for idx in random_indices:
    if idx in used_indices:
        continue

    row = distances_df.loc[idx]

    group_a.add(idx)
    used_indices.add(idx)

    closest_indices = np.argsort(row)[1:]

    assigned_b = False
    assigned_c = False

    for i in closest_indices:
        if not assigned_b and i not in used_indices:

            group_b.add(i)
            used_indices.add(i)
            assigned_b = True
            continue

        if not assigned_c and i not in used_indices:
      
            group_c.add(i)
            used_indices.add(i)
            assigned_c = True

        if assigned_b and assigned_c:
            break

    # Handle cases where not enough unassigned closest points are available
    if not assigned_b or not assigned_c:
        print(f"Not enough unassigned closest points for index {idx}")

group_a_dict = {idx: 'Group A' for idx in group_a}
group_b_dict = {idx: 'Group B' for idx in group_b}  
group_c_dict = {idx: 'Group C' for idx in group_c}

assignment_dict = {**group_a_dict, **group_b_dict, **group_c_dict}

print(assignment_dict)

print(len(group_a))
print(len(group_b))
print(len(group_c))




'''

'''
cluster_counts = final_df_with_cvr['cluster'].value_counts().to_dict()

# Create a list to store group assignments
group_assignments = []

# Loop over each cluster and assign groups proportionally
for cluster_id, count in cluster_counts.items():
    # Calculate the sizes for each group in this cluster
    group_size = count // 3
    remainder = count % 3  # To handle any uneven distribution

    # Assign group labels for this cluster
    group_labels = (['Group A'] * group_size + 
                    ['Group B'] * group_size + 
                    ['Group C'] * group_size)

    # Distribute the remainder items across groups
    for i in range(remainder):
        group_labels.append(f'Group {chr(65 + i)}')  # Assign extra items to Group A, B, or C as needed

    # Shuffle the labels to avoid any ordering bias
    np.random.shuffle(group_labels)

    # Append the labels for the current cluster
    group_assignments.extend(group_labels)

# Add the balanced group assignments to the DataFrame
#final_df_with_cvr = final_df_with_cvr.sort_values(by='cluster')
final_df_with_cvr['group'] = group_assignments

final_df_with_cvr

'''

'''
from scipy.spatial.distance import euclidean

centroids = final_df_with_cvr.groupby('cluster')[['x', 'y']].mean()

# Calculate the distance of each point to its own cluster's centroid
def calculate_distance(row):
    cluster_id = row['cluster']
    centroid = centroids.loc[cluster_id]
    return euclidean((row['x'], row['y']), centroid)

# Apply distance calculation
final_df_with_cvr['distance_to_centroid'] = final_df_with_cvr.apply(calculate_distance, axis=1)

# Initialize list for group assignments
group_assignments = []

# Sort each cluster by distance to centroid and assign groups in a balanced way
for cluster_id, group_df in final_df_with_cvr.groupby('cluster'):
    # Sort points within the cluster by distance to the centroid
    sorted_df = group_df.sort_values(by='distance_to_centroid')
    
    # Calculate group sizes
    count = len(sorted_df)
    group_size = count // 3
    remainder = count % 3
    
    # Assign groups based on distance ranking within each cluster
    group_labels = ['Group A'] * group_size + ['Group B'] * group_size + ['Group C'] * group_size

    # Handle any remainders
    for i in range(remainder):
        group_labels.append(f'Group {chr(65 + i)}')
    
    # Apply group labels in sorted order (no shuffle)
    sorted_df['group'] = group_labels
    
    # Append to group assignments list, maintaining order
    group_assignments.append(sorted_df)

# Concatenate all clusters back into the main DataFrame
final_df_with_cvr = pd.concat(group_assignments).sort_index()

final_df_with_cvr
'''