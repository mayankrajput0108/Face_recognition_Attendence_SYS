# Face Recognition Attendance System  

![Python](https://img.shields.io/badge/Python-3.x-blue)  
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)  

## Overview  

A Python-based attendance system using face recognition technology to track and manage attendance through facial detection.

## Features  

- 📷 **Face Registration** - Capture and store facial images  
- ✅ **Attendance Tracking** - Recognize faces and record timestamps  
- 🔒 **Password Protection** - Secure training functions  
- 📊 **Data Management** - CSV storage for student records  
- ⏱️ **Real-time Clock** - Current time display  
- 🖥️ **GUI Interface** - User-friendly Tkinter interface  

## Installation  

1. Clone repository:  
```bash
git clone https://github.com/PiyushJaiswall/face-recognition-attendance-system.git
cd face-recognition-attendance-system
```
2. Install required packages: 
```bash
pip install opencv-python pillow pandas numpy
```
3. Ensure these files are in your project root:
```bash
main.py

haarcascade_frontalface_default.xml

```
## File Structure
```bash
project/
├── main.py                    # Main application
├── haarcascade_frontalface_default.xml  # Face detection model
├── StudentDetails/            # Student records (auto-created)
├── TrainingImage/             # Captured face images (auto-created)  
├── TrainingImageLabel/        # Trained model data (auto-created)
└── Attendance/                # Attendance records (auto-created)
```
## First-Time Setup
1. Run the application:
```bash
python main.py
```
2. When prompted, set an admin password for the training functions.

## Usage
### New Registration
1. Enter ID and Name in right panel
2. Click "Take Images" (system will capture 100 facial samples)
3. Click "Save Profile" to train the model

### Taking Attendance
1. Click "Capture Attendance" in left panel
2. Position face in camera view
3. Click "Stop Attendance" when finished

## Dependencies
- Python 3.6+
- OpenCV (opencv-python)
- Pillow (pillow)
- Pandas (pandas)
- NumPy (numpy)

## Notes
- Folders are automatically created on first run
- Works best with consistent lighting conditions
- For accuracy, capture face images from multiple angles during registration

## Contact
For support: piyushooo@gmail.com
