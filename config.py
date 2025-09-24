# Configuration file for building detection system

# Input/Output Settings
DEFAULT_INPUT_FOLDER = "Massachusetts labels"
DEFAULT_OUTPUT_FOLDER = "output"

# Image Processing Parameters
ADAPTIVE_THRESH_BLOCK_SIZE = 15
ADAPTIVE_THRESH_C = 10

# Morphological Operations
MORPH_KERNEL_SIZE = (3, 3)
MORPH_ITERATIONS = 2

# Distance Transform Parameters
DISTANCE_TRANSFORM_TYPE = "cv2.DIST_L2"
DISTANCE_MASK_SIZE = 5

# Peak Detection Parameters
ELLIPSE_KERNEL_SIZE = (7, 7)
PEAK_THRESHOLD_RATIO = 0.3  # Threshold = ratio * max_value

# Visualization Parameters
TEXT_FONT = "cv2.FONT_HERSHEY_SIMPLEX"
TEXT_SCALE = 0.6
TEXT_COLOR = (255, 255, 255)  # White
OUTLINE_COLOR = (0, 0, 0)     # Black
TEXT_THICKNESS = 2
OUTLINE_THICKNESS = 3
CIRCLE_RADIUS = 3
CIRCLE_COLOR = (0, 255, 0)    # Green

# Image Quality Settings
OUTPUT_DPI = 300
FIGURE_SIZE = (25, 25)

# File Settings
SUPPORTED_EXTENSIONS = ['.tif', '.tiff', '.jpg', '.jpeg', '.png', '.bmp']
OUTPUT_IMAGE_FORMAT = '.png'

# CSV Output Columns
CSV_COLUMNS = [
    'image_filename',
    'building_count', 
    'total_building_area_pixels',
    'building_centers_area_pixels',
    'coverage_percentage',
    'output_image',
    'individual_csv',
    'image_width',
    'image_height'
]

# Individual Building CSV Columns
INDIVIDUAL_CSV_COLUMNS = [
    'building_number',
    'center_x',
    'center_y', 
    'area_pixels',
    'label_id'
]