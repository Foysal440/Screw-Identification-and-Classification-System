[app]

# (str) Title of your application
title = Screw Detection App

# (str) Package name
package.name = screwdetection

# (str) Package domain (needed for android/ios packaging)
package.domain = org.screw.detection

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Include necessary libraries for your program
requirements = python3,kivy,pillow,opencv-python,numpy

# (str) Presplash of the application
# Add a presplash screen for branding (optional)
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# Add your custom app icon (recommended)
icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
# Set the orientation to portrait for this app
orientation = portrait

# (list) Permissions
# Permissions for accessing external storage and camera (if needed)
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE, android.permission.INTERNET

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Supported architectures
# Supporting both ARM architectures for broader compatibility
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Gradle dependencies
# Necessary dependencies for your app (if any additional are required)
android.gradle_dependencies =

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Adaptive icon of the application
# Optional: Use adaptive icons for Android API 26+ (recommended)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
