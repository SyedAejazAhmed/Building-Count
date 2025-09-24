#!/usr/bin/env python3
"""
Test script for building detection system
Run this to verify everything is working correctly
"""

import os
import sys
from pathlib import Path

def test_installation():
    """Test if all required packages are installed"""
    print("Testing installation...")
    
    try:
        import cv2
        print("✓ OpenCV installed")
    except ImportError:
        print("✗ OpenCV not installed. Run: pip install opencv-python")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy installed")
    except ImportError:
        print("✗ NumPy not installed. Run: pip install numpy")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas installed")
    except ImportError:
        print("✗ Pandas not installed. Run: pip install pandas")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ Matplotlib installed")
    except ImportError:
        print("✗ Matplotlib not installed. Run: pip install matplotlib")
        return False
    
    return True

def test_folder_structure():
    """Test if input folder exists"""
    print("\nTesting folder structure...")
    
    input_folder = "Massachusetts labels"
    if os.path.exists(input_folder):
        print(f"✓ Input folder '{input_folder}' found")
        
        # Count image files
        image_extensions = {'.tif', '.tiff', '.jpg', '.jpeg', '.png', '.bmp'}
        image_files = [f for f in Path(input_folder).iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]
        
        print(f"✓ Found {len(image_files)} image files")
        
        if image_files:
            print("  Sample files:")
            for i, file in enumerate(image_files[:3]):
                print(f"    - {file.name}")
            if len(image_files) > 3:
                print(f"    ... and {len(image_files) - 3} more")
        
        return True
    else:
        print(f"✗ Input folder '{input_folder}' not found")
        print("  Please ensure you have images in the 'Massachusetts labels' folder")
        return False

def test_building_detector():
    """Test if building_detector.py can be imported"""
    print("\nTesting building detector module...")
    
    try:
        from building_detector import detect_buildings_in_folder, process_single_image
        print("✓ Building detector module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Could not import building detector: {e}")
        return False

def run_sample_test():
    """Run a quick test on one image if available"""
    print("\nRunning sample test...")
    
    try:
        from building_detector import process_single_image
        import tempfile
        
        # Find first image file
        input_folder = Path("Massachusetts labels")
        if not input_folder.exists():
            print("✗ No input folder found for testing")
            return False
        
        image_extensions = {'.tif', '.tiff', '.jpg', '.jpeg', '.png', '.bmp'}
        image_files = [f for f in input_folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]
        
        if not image_files:
            print("✗ No image files found for testing")
            return False
        
        # Test with first image
        test_image = image_files[0]
        print(f"Testing with: {test_image.name}")
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_single_image(test_image, Path(temp_dir))
            
            if result:
                print(f"✓ Test successful!")
                print(f"  Buildings detected: {result['building_count']}")
                print(f"  Building area: {result['total_building_area_pixels']} pixels")
                print(f"  Output image: {result['output_image']}")
                return True
            else:
                print("✗ Test failed - no result returned")
                return False
                
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("BUILDING DETECTION SYSTEM - TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_installation,
        test_folder_structure,
        test_building_detector,
        run_sample_test
    ]
    
    passed = 0
    total = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"\n[{i}/{total}] Running {test.__name__.replace('_', ' ')}...")
        if test():
            passed += 1
        else:
            print(f"Test {i} failed!")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo run the building detection:")
        print("1. python building_detector.py")
        print("2. Or use: from building_detector import detect_buildings_in_folder")
        print("3. Or run GUI: python building_detector_gui.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        
        if passed == 0:
            print("\nQuick fix - install requirements:")
            print("pip install -r requirements.txt")
    
    print("=" * 50)

if __name__ == "__main__":
    main()