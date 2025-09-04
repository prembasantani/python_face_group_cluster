There are several commands to run this python page.

# Python suited for this face cluster - 3.8.0

# Firstly Install python 3.8.0 from python.org

<!-- Create Virtual Environment -->

# cd python_face_group_cluster
# py -3.8 -m venv .venv
# .venv\Scripts\activate

- This above commands would activate the virtual environment for you

* Make sure latest pip version is installed. At the time of creation of this module when installing python 3.8.0, Automatic version of pip comes as 19.2.3

* We would require the latest version for the continuity

<!-- To update pip use the following command -->

# python -m pip install --upgrade pip

<!-- Install required libararies for running the cluster program -->

# pip install pillow
# pip install ImageHash
# pip install dlib-19.22.99-cp38-cp38-win_amd64.whl
# pip install face-recognition
# pip install scikit-learn
# pip install tqdm

<!-- One final thing before running your program now. Image folder with name 'Images' should be created inside the main root directory with images inside to find faces and re group in cluster folder in root directory -->

<!-- Your program is now ready to run -->