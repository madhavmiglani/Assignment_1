import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load and read the image
image_path = r'C:\Users\Madhav\Desktop\assignment.jpg'
image = mpimg.imread(image_path)

# Flatten the image array to a 2D array 
pixel_arr = image.reshape(-1, 3)

# Create a DataFrame for pixel data
df_pixels = pd.DataFrame(pixel_arr, columns=['R', 'G', 'B'])

#Euclidean distance between two points
def compute_distance(point_1, point_2):
    return np.sqrt(np.sum((point_1 - point_2)**2))

# Function to initialize centroids using K-means++ algorithm
def init_centr(pixel_arr, K):
    centroids = [pixel_arr[np.random.randint(pixel_arr.shape[0]), :]]
    for _ in range(K - 1):
        distances = np.array([min([compute_distance(pixel, centroid) for centroid in centroids]) for pixel in pixel_arr])
        next_centroid = pixel_arr[np.argmax(distances)]
        centroids.append(next_centroid)
    return np.array(centroids)

# Function to assign pixels to the nearest centroid
def assign_clusters(pixel_arr, centroids, K):
    clusters = {i: [] for i in range(K)}
    for pixel in pixel_arr:
        distances = [compute_distance(pixel, centroid) for centroid in centroids]
        closest_centroid = np.argmin(distances)
        clusters[closest_centroid].append(pixel)
    return clusters

# Function to recompute centroids as the mean of assigned points
def recompute_centroids(clusters, K):
    new_centroids = [np.mean(clusters[i], axis=0) for i in range(K)]
    return np.array(new_centroids)

# Function to assign each pixel to the nearest cluster's centroid
def assign_pixel_arr(pixel_arr, centroids, K):
    new_pixel_array = np.zeros(pixel_arr.shape)
    for idx, pixel in enumerate(pixel_arr):
        distances = [compute_distance(pixel, centroid) for centroid in centroids]
        closest_centroid = np.argmin(distances)
        new_pixel_array[idx] = centroids[closest_centroid]
    return new_pixel_array

# Main K-means clustering function
def kmeans_clust(pixel_arr, K, max_iterations=100):
    centroids = init_centr(pixel_arr, K)
    for _ in range(max_iterations):
        clusters = assign_clusters(pixel_arr, centroids, K)
        new_centroids = recompute_centroids(clusters, K)
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    return centroids, clusters

# Execute K-means++ clustering
K = 3
final_centroids, final_clusters = kmeans_clust(pixel_arr, K)

# Assign pixels to the closest centroid and reshape to the original image dimensions
clustered_pixel_arr = assign_pixel_arr(pixel_arr, final_centroids, K)
clustered_image = clustered_pixel_arr.reshape(image.shape)

# Display the clustered image
plt.imshow(clustered_image.astype(np.uint8))
plt.axis(False)
plt.show()
