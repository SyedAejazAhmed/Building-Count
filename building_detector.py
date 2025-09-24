import cv2
import numpy as np
import os
import pandas as pd
import random
from pathlib import Path
import matplotlib.pyplot as plt

def detect_buildings_in_folder(input_folder_path, output_folder="output"):
    """
    Detect buildings in all images within a folder using distance transform method.
    
    Parameters:
    - input_folder_path: Path to folder containing images
    - output_folder: Name of output folder to create
    
    Returns:
    - DataFrame with results
    """
    
    # Create output directory structure
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    images_output_path = output_path / "images"
    images_output_path.mkdir(exist_ok=True)
    
    # Initialize results list
    results = []
    
    # Supported image extensions
    image_extensions = {'.tif', '.tiff', '.jpg', '.jpeg', '.png', '.bmp'}
    
    # Get all image files in the input folder
    input_path = Path(input_folder_path)
    image_files = [f for f in input_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"No image files found in {input_folder_path}")
        return pd.DataFrame()
    
    print(f"Found {len(image_files)} image files to process...")
    
    for image_file in image_files:
        print(f"\nProcessing: {image_file.name}")
        
        try:
            # Process single image
            result = process_single_image(image_file, images_output_path)
            if result:
                results.append(result)
                print(f"✓ Completed: {result['building_count']} buildings detected")
            else:
                print(f"✗ Failed to process: {image_file.name}")
                
        except Exception as e:
            print(f"✗ Error processing {image_file.name}: {str(e)}")
            continue
    
    # Create CSV with results
    if results:
        df = pd.DataFrame(results)
        csv_path = output_path / "building_detection_results.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n✓ Results saved to: {csv_path}")
        print(f"✓ Processed images saved to: {images_output_path}")
        print(f"✓ Individual building CSV files created for each image")
        
        # Print summary
        print(f"\n=== SUMMARY ===")
        print(f"Total images processed: {len(results)}")
        print(f"Total buildings detected: {df['building_count'].sum()}")
        print(f"Average buildings per image: {df['building_count'].mean():.2f}")
        print(f"Total building area (pixels): {df['total_building_area_pixels'].sum()}")
        print(f"Individual CSV files: {len([r for r in results if r.get('individual_csv')])}")
        
        return df
    else:
        print("No images were successfully processed.")
        return pd.DataFrame()

def process_single_image(image_path, output_dir):
    """
    Process a single image to detect buildings using distance transform method.
    
    Parameters:
    - image_path: Path to the image file
    - output_dir: Directory to save the processed image
    
    Returns:
    - Dictionary with detection results
    """
    
    try:
        # Load image
        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if image is None:
            print(f"Could not load image: {image_path}")
            return None
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Adaptive thresholding
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY_INV, 15, 10)
        
        # Morphological cleanup
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Distance transform method for building detection
        dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
        
        # Find local maxima
        kernel_max = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        local_maxima = cv2.morphologyEx(dist_transform, cv2.MORPH_TOPHAT, kernel_max)
        
        # Threshold to get peaks
        _, peaks = cv2.threshold(local_maxima, 0.3 * local_maxima.max(), 255, cv2.THRESH_BINARY)
        peaks = peaks.astype(np.uint8)
        
        # Find connected components of peaks
        num_peaks, peak_labels = cv2.connectedComponents(peaks)
        
        # Number of buildings detected (subtract 1 for background)
        buildings_detected = num_peaks - 1
        
        # Create numbered visualization
        numbered_viz = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        building_centers = []
        building_count = 0
        total_building_area = 0
        
        # Process each building (skip background label 0)
        for label in range(1, num_peaks):
            # Find all pixels belonging to this building center
            mask = (peak_labels == label)
            
            if np.any(mask):
                # Get coordinates of this building center
                coords = np.where(mask)
                
                if len(coords[0]) > 0:
                    # Calculate centroid of the building center
                    cY = int(np.mean(coords[0]))
                    cX = int(np.mean(coords[1]))
                    
                    building_centers.append((cX, cY, label))
                    building_count += 1
                    
                    # Calculate building area (approximate using connected component area)
                    building_area = np.sum(mask)
                    total_building_area += building_area
                    
                    # Add number to the visualization with high contrast
                    text_color = (255, 255, 255)  # White
                    outline_color = (0, 0, 0)     # Black
                    
                    # Add thick black outline for visibility
                    cv2.putText(numbered_viz, f'{building_count}', (cX-20, cY+8),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, outline_color, 3)
                    cv2.putText(numbered_viz, f'{building_count}', (cX-20, cY+8),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
                    
                    # Draw a circle at building center
                    cv2.circle(numbered_viz, (cX, cY), 3, (0, 255, 0), -1)
        
        # Save the numbered image
        output_filename = f"numbered_{image_path.stem}.png"
        output_path = output_dir / output_filename
        cv2.imwrite(str(output_path), numbered_viz)
        
        # Create individual building data for CSV
        individual_buildings = []
        for i, (cX, cY, label) in enumerate(building_centers, 1):
            # Calculate individual building area (approximate using connected component)
            mask = (peak_labels == label)
            building_area = np.sum(mask)
            
            individual_buildings.append({
                'building_number': i,
                'center_x': cX,
                'center_y': cY,
                'area_pixels': building_area,
                'label_id': label
            })
        
        # Save individual CSV for this image
        if individual_buildings:
            csv_filename = f"{image_path.stem}_buildings.csv"
            csv_path = output_dir / csv_filename
            buildings_df = pd.DataFrame(individual_buildings)
            buildings_df.to_csv(csv_path, index=False)
        
        # Calculate total white pixels (building area)
        total_white_pixels = np.sum(binary == 255)
        
        # Return results
        return {
            'image_filename': image_path.name,
            'building_count': building_count,
            'total_building_area_pixels': total_white_pixels,
            'building_centers_area_pixels': total_building_area,
            'coverage_percentage': (total_building_area / total_white_pixels * 100) if total_white_pixels > 0 else 0,
            'output_image': output_filename,
            'individual_csv': csv_filename if individual_buildings else None,
            'image_width': binary.shape[1],
            'image_height': binary.shape[0]
        }
        
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def create_summary_visualization(csv_path):
    """
    Create a summary visualization from the CSV results.
    
    Parameters:
    - csv_path: Path to the CSV file with results
    """
    
    try:
        df = pd.read_csv(csv_path)
        
        # Create summary plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Building count per image
        axes[0, 0].bar(range(len(df)), df['building_count'])
        axes[0, 0].set_title('Building Count per Image')
        axes[0, 0].set_xlabel('Image Index')
        axes[0, 0].set_ylabel('Number of Buildings')
        
        # Plot 2: Building area distribution
        axes[0, 1].hist(df['total_building_area_pixels'], bins=10, alpha=0.7)
        axes[0, 1].set_title('Building Area Distribution')
        axes[0, 1].set_xlabel('Total Building Area (pixels)')
        axes[0, 1].set_ylabel('Frequency')
        
        # Plot 3: Coverage percentage
        axes[1, 0].bar(range(len(df)), df['coverage_percentage'])
        axes[1, 0].set_title('Building Coverage Percentage')
        axes[1, 0].set_xlabel('Image Index')
        axes[1, 0].set_ylabel('Coverage %')
        
        # Plot 4: Building count vs area scatter
        axes[1, 1].scatter(df['building_count'], df['total_building_area_pixels'])
        axes[1, 1].set_title('Building Count vs Total Area')
        axes[1, 1].set_xlabel('Number of Buildings')
        axes[1, 1].set_ylabel('Total Building Area (pixels)')
        
        plt.tight_layout()
        
        # Save the summary plot
        summary_path = Path(csv_path).parent / "summary_visualization.png"
        plt.savefig(summary_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Summary visualization saved to: {summary_path}")
        
    except Exception as e:
        print(f"Error creating summary visualization: {str(e)}")

# Example usage function
def main():
    """
    Main function to demonstrate usage
    """
    
    # Example usage
    input_folder = "Massachusetts labels"  # Change this to your input folder
    output_folder = "output"
    
    print("=== BUILDING DETECTION BATCH PROCESSOR ===")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        print("Please provide a valid folder path containing images.")
        return
    
    # Process all images in the folder
    results_df = detect_buildings_in_folder(input_folder, output_folder)
    
    if not results_df.empty:
        # Create summary visualization
        csv_path = os.path.join(output_folder, "building_detection_results.csv")
        create_summary_visualization(csv_path)
        
        print(f"\n✓ All processing completed successfully!")
        print(f"✓ Check the '{output_folder}' folder for results")
        print(f"✓ Individual CSV files created for each image with building details")
    else:
        print("\n✗ No images were processed successfully.")

if __name__ == "__main__":
    main()