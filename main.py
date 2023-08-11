import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import rawpy


def calculate_light_loss(img1_path, img2_path):
    with rawpy.imread(img1_path) as raw:
        rgb = raw.postprocess(output_bps=16,
                              exp_shift=0.0,
                              gamma=(1, 1),
                              no_auto_bright=True,
                              use_camera_wb=True,
                              output_color=rawpy.ColorSpace.raw)

    img1 = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    with rawpy.imread(img2_path) as raw:
        rgb = raw.postprocess(output_bps=16,
                              exp_shift=0.0,
                              gamma=(1, 1),
                              no_auto_bright=True,
                              use_camera_wb=True,
                              output_color=rawpy.ColorSpace.raw)

    img2 = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    if img1 is None or img2 is None:
        raise ValueError("Image files not found. Please check the paths.")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    mean1 = np.mean(gray1)
    mean2 = np.mean(gray2)

    exposure_difference = np.log2(mean1 / mean2)

    return exposure_difference


def on_calculate_exposure():

    top = tk.Tk()
    top.geometry("300x150")
    top.title("Select Images")

    img1_path = None
    img2_path = None

    def on_select_cross_image():
        nonlocal img1_path
        img1_path = filedialog.askopenfilename(title="Select the cross-polarized image")
        if img1_path != "":
            select_cross_image_button.config(text=img1_path.split("/")[-1])

    def on_select_parallel_image():
        nonlocal img2_path
        img2_path = filedialog.askopenfilename(
            title="Select the parallel-polarized image"
        )

        if img2_path != "":
            select_parallel_image_button.config(text=img2_path.split("/")[-1])

    def on_start_calculation():
        nonlocal img1_path, img2_path
        if img1_path is None or img2_path is None or img1_path == "" or img2_path == "":
            result_label.config(text="Please select both images.")
        else:
            exposure_difference = calculate_light_loss(img1_path, img2_path)
            result_label.config(
                text=f"Exposure difference: {exposure_difference:.2f} stops"
            )

    select_cross_image_button = tk.Button(
        top, text="Select Cross Image", command=on_select_cross_image
    )
    select_cross_image_button.pack(pady=5)

    select_parallel_image_button = tk.Button(
        top, text="Select Parallel Image", command=on_select_parallel_image
    )
    select_parallel_image_button.pack(pady=5)

    start_calculation_button = tk.Button(
        top, text="Start Calculation", command=on_start_calculation
    )
    start_calculation_button.pack(pady=5)

    result_label = tk.Label(top, text="")
    result_label.pack(pady=5)

    top.mainloop()


if __name__ == "__main__":
    on_calculate_exposure()
