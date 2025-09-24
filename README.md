# Building Detection System

This Python system automatically detects buildings in satellite/aerial images using distance transform method and provides comprehensive analysis with numbered visualizations.

## Quick Start

1. **Run the setup script:**
   ```bash
   setup.bat
   ```

2. **Test the system (optional but recommended):**
   ```bash
   python test_system.py
   ```

3. **Process images and view results:**
   ```bash
   python result.py
   ```
   
   **Alternative:** You can also run the building detector directly:
   ```bash
   python building_detector.py
   ```

## Initial Setup

The system comes with sample TIFF images in the `Massachusetts labels/` folder:
- 22828930_15.tif
- 22828990_15.tif
- 22829050_15.tif
- 23429020_15.tif
- 23429080_15.tif
- 23578960_15.tif
- 23579005_15.tif
- 23729035_15.tif
- 23879080_15.tif
- 24179065_15.tif

## Adding Your Own Images

To process your own images:
1. Add TIFF files (.tif format) to the `Massachusetts labels/` folder
2. Run the system using the commands above
3. Results will be generated in the `output/` folder

## Features

- **Batch Processing**: Automatically processes all TIFF images in the Massachusetts labels folder
- **Building Detection**: Uses distance transform method for accurate building detection
- **Numbered Visualization**: Creates images with numbered buildings for easy identification
- **CSV Results**: Generates detailed CSV files with building counts and areas
- **Summary Statistics**: Provides comprehensive analysis and visualizations
- **GUI**: A simple graphical user interface is available by running `python building_detector_gui.py`.
- **System Tests**: A test script `test_system.py` is included to verify the installation and functionality.

## Testing the System

To ensure the system is set up correctly and all dependencies are installed, you can run the test script:

```bash
python test_system.py
```

This script will perform the following checks:
- Verify that all required Python packages (OpenCV, NumPy, Pandas, Matplotlib) are installed.
- Check if the `Massachusetts labels/` input folder exists and contains images.
- Ensure that the `building_detector.py` module can be imported correctly.
- Run a sample detection on a single image to confirm the processing pipeline is working.

## Output Structure

The system creates different output folders depending on which script you run:

### Running `python result.py`:
Results are saved in the `results/` folder:
```
results/
├── images/
│   ├── numbered_22828930_15.png
│   ├── numbered_22828990_15.png
│   └── ... (numbered images for each input)
├── building_detection_results.csv
└── individual CSV files for each image
```

### Running `python building_detector.py`:
Results are saved in the `output/` folder:
```
output/
├── images/
│   ├── numbered_22828930_15.png
│   ├── numbered_22828990_15.png
│   └── ... (numbered images for each input)
├── building_detection_results.csv
└── summary_visualization.png
```

## Requirements

The system requires Python packages that will be automatically installed during setup:
- opencv-python
- numpy
- pandas
- matplotlib

## System Requirements

- Python 3.7 or higher
- Windows operating system (for the .bat setup script)
- Sufficient disk space for output images and CSV files

## Supported Image Format

- **Primary Format**: TIFF (.tif) - recommended for satellite/aerial imagery
- The system is optimized for TIFF format which provides the best quality for building detection

## How It Works

1. **Setup**: Creates Python virtual environment and installs dependencies
2. **Detection**: Uses distance transform algorithm to identify building structures
3. **Visualization**: Numbers each detected building on output images
4. **Analysis**: Generates CSV files with building counts and statistical data
5. **Summary**: Creates visualization charts showing detection results

## Troubleshooting

**Setup Issues:**
- Ensure you have Python installed on your system
- Run PowerShell as Administrator if you encounter permission issues

**Detection Issues:**
- Make sure your TIFF files are in the `Massachusetts labels/` folder
- Verify image files are not corrupted
- Run `python test_system.py` to diagnose potential issues.
