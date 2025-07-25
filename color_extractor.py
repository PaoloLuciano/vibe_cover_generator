import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import cv2

class ColorExtractor:
    def __init__(self, n_colors=5):
        self.n_colors = n_colors
    
    def extract_colors(self, image_path):
        """Extract dominant colors from an image using K-means clustering."""
        image = Image.open(image_path)
        image = image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Reshape to 2D array of pixels
        pixels = image_array.reshape(-1, 3)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the dominant colors
        colors = kmeans.cluster_centers_.astype(int)
        
        # Get the percentage of each color
        labels = kmeans.labels_
        label_counts = np.bincount(labels)
        percentages = (label_counts / len(labels)) * 100
        
        # Sort colors by dominance
        sorted_indices = np.argsort(percentages)[::-1]
        colors = colors[sorted_indices]
        percentages = percentages[sorted_indices]
        
        return colors, percentages
    
    def extract_colors_multiple(self, image_paths):
        """Extract colors from multiple images and combine them."""
        all_pixels = []
        
        for image_path in image_paths:
            image = Image.open(image_path)
            image = image.convert('RGB')
            image_array = np.array(image)
            pixels = image_array.reshape(-1, 3)
            all_pixels.extend(pixels)
        
        all_pixels = np.array(all_pixels)
        
        # Apply K-means to combined pixels
        kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
        kmeans.fit(all_pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        
        # Get percentages
        labels = kmeans.labels_
        label_counts = np.bincount(labels)
        percentages = (label_counts / len(labels)) * 100
        
        # Sort by dominance
        sorted_indices = np.argsort(percentages)[::-1]
        colors = colors[sorted_indices]
        percentages = percentages[sorted_indices]
        
        return colors, percentages
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color code."""
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
    
    def get_color_palette(self, image_paths):
        """Get a formatted color palette from image(s)."""
        if isinstance(image_paths, str):
            colors, percentages = self.extract_colors(image_paths)
        else:
            colors, percentages = self.extract_colors_multiple(image_paths)
        
        palette = []
        for i, (color, percentage) in enumerate(zip(colors, percentages)):
            palette.append({
                'rgb': tuple(int(c) for c in color),
                'hex': self.rgb_to_hex(color),
                'percentage': float(round(percentage, 1)),
                'rank': i + 1
            })
        
        return palette