# FxLab

A Django web app for applying various filters to images

- Uses Python and Django for back-end
- Uses plain HTML, CSS, JS for front-end
- Uses OpenCV for server-side image processing
- Filters include: grayscale, negative, blurring and edge detection

## Getting Started

1. Clone repository

    ```sh 
    git clone https://github.com/vanbagaria/fxlab
    cd fxlab
    ```
1. Ensure Python 3.10 or greater is installed and create virtual environment

    ```sh
    python --version # Should output 3.10 or above
    python -m venv fxvenv
    source fxvenv/bin/activate
    ```
1. Install dependencies in virtual environment

    ```sh
    pip install -r requirements.txt
    ```
1. Test setup with "Debug = True" set in fxlab/settings.py

    ```sh
    python manage.py runserver
    ```
1. Open 127.0.0.1:8000 in a web browser to test that the development environment is working

## Uses

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [OpenCV](https://opencv.org/)