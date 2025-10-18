import cv2
import os
import numpy as np
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse

# Fixed names for the images
INPUT_IMAGE_NAME = 'uploaded_image.png'
OUTPUT_IMAGE_NAME = 'filtered_image.png'

def apply_mean_filter(image, kernel_size=9):
    """Applies mean (average) filtering using convolution."""
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    return cv2.filter2D(image, -1, kernel)

def apply_gaussian_filter(image, kernel_size=9, sigma=3):
    """Applies Gaussian filtering using OpenCV's built-in function."""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

def apply_median_filter(image, kernel_size=9):
    """Applies median filtering using OpenCV's built-in function."""
    return cv2.medianBlur(image, kernel_size)

def apply_filter(image_path, filter_type):
    # Read the image
    image = cv2.imread(image_path)

    if filter_type == 'grayscale':
        filtered_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'negative':
        filtered_image = 255 - image
    elif filter_type == 'mean_blur':
        filtered_image = apply_mean_filter(image)
    elif filter_type == 'gaussian_blur':
        filtered_image = apply_gaussian_filter(image)
    elif filter_type == 'median_blur':
        filtered_image = apply_median_filter(image)
    elif filter_type == 'laplacian':
        filtered_image = cv2.Laplacian(image, cv2.CV_64F)
        filtered_image = np.uint8(np.absolute(filtered_image))
    elif filter_type == 'high_pass':
        high_pass_kernel = np.array([[-1, -1, -1],
                                      [-1,  8, -1],
                                      [-1, -1, -1]])
        filtered_image = cv2.filter2D(image, -1, high_pass_kernel)
    elif filter_type == 'edges_sobel':
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        filtered_image = cv2.bitwise_or(sobel_x, sobel_y)
    elif filter_type == 'edges_prewitt':
        prewitt_x = cv2.filter2D(image, -1, np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]))
        prewitt_y = cv2.filter2D(image, -1, np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]))
        filtered_image = cv2.bitwise_or(prewitt_x, prewitt_y)
    elif filter_type == 'edges_canny':
        filtered_image = cv2.Canny(image, 100, 200)
    elif filter_type == 'threshold_binary':
        _, filtered_image = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    elif filter_type == 'threshold_otsu':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, filtered_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        filtered_image = image  # No filter

    # Save the filtered image
    output_path = os.path.join(settings.MEDIA_ROOT, OUTPUT_IMAGE_NAME)
    cv2.imwrite(output_path, filtered_image)
    return output_path


def cleanup_files():
    """Remove the uploaded and filtered images."""
    input_image_path = os.path.join(settings.MEDIA_ROOT, INPUT_IMAGE_NAME)
    output_image_path = os.path.join(settings.MEDIA_ROOT, OUTPUT_IMAGE_NAME)

    if os.path.exists(input_image_path):
        os.remove(input_image_path)
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

def upload_image(request):
    cleanup_files()
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        filter_type = request.POST.get('filter_type')

        fs = FileSystemStorage()
        fs.save(INPUT_IMAGE_NAME, image_file)  # Save with fixed name
        uploaded_file_url = fs.url(INPUT_IMAGE_NAME)

        # Apply the selected filter
        image_path = os.path.join(settings.MEDIA_ROOT, INPUT_IMAGE_NAME)
        filtered_image_path = apply_filter(image_path, filter_type)

        return render(request, 'filterlab/result.html', {
            'uploaded_file_url': uploaded_file_url,
            'filtered_image_url': settings.MEDIA_URL + OUTPUT_IMAGE_NAME
        })

    return render(request, 'filterlab/upload.html')

def cleanup_filtered_image(request):
    """Cleanup the uploaded and filtered images when the user navigates away."""
    cleanup_files()
    return redirect('/fxlab' + reverse('upload_image'))  # Redirect to the upload page
