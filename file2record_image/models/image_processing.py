from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageStat


def transform_image(original_img, size_ratio=1.0, crop_box=None, crop_size=1.0,
                    blur=0, threshold=0, median_filter=False, contrast=1.0,
                    invert=False, revert_resize=False,
                    adaptive_sharpening=True, sharpening_radius=0, sharpening_percent=0, sharpening_threshold=0,
                    save_steps=False, output_dir=''):
    """
    Transform an image for Optical Character Recognition (OCR).
    """

    # Convert to grayscale and resize in one step
    img = original_img.convert('L')
    width, height = img.size
    if size_ratio != 1:
        size = (int(width * size_ratio), int(height * size_ratio))
        img = img.resize(size)
    if save_steps:
        img.save(f'{output_dir}/grayscale_resize.png')

    # Crop the image if a crop box is provided
    if crop_box:
        width, height = img.size
        crop_areas = {
            'top': (0, 0, width, height // 2),
            'bottom': (0, height // 2, width, height),
            'left': (0, 0, width // 2, height),
            'right': (width // 2, 0, width, height),
            'center': ((width - width * crop_size) // 2, (height - height * crop_size) // 2,
                       (width + width * crop_size) // 2, (height + height * crop_size) // 2)
        }
        img = img.crop(crop_areas.get(crop_box, img.getbbox()))
        if save_steps:
            img.save(f'{output_dir}/crop.png')

    if contrast != 1:
        img = ImageEnhance.Contrast(img).enhance(contrast)
        if save_steps:
            img.save(f'{output_dir}/contrast_enhance.png')


    if adaptive_sharpening:
        sharpening_radius, sharpening_percent, sharpening_threshold = adjust_sharpening_params(img)
    elif sharpening_radius == 0 and sharpening_percent == 0 and sharpening_threshold == 0:
        sharpening_radius, sharpening_percent, sharpening_threshold = 10, 1000, 30

    if sharpening_radius and sharpening_percent and sharpening_threshold:
        img = img.filter(ImageFilter.UnsharpMask(radius=sharpening_radius,
                                                 percent=sharpening_percent,
                                                 threshold=sharpening_threshold))
    if save_steps:
        img.save(f'{output_dir}/sharpen.png')

    if median_filter:
        img = img.filter(ImageFilter.MedianFilter(size=7))
        if save_steps:
            img.save(f'{output_dir}/median_filter.png')

    if blur:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
        if save_steps:
            img.save(f'{output_dir}/gaussian_blur.png')

    if not threshold:
        threshold = otsu_threshold(img)
    img = img.point(lambda x: 0 if x < threshold else 255)
    if save_steps:
        img.save(f'{output_dir}/threshold.png')

    if revert_resize and size_ratio != 1:
        size = original_img.size
        img = img.resize(size)

    if save_steps:
        img.save(f'{output_dir}/result.png')

    if invert:
        img = ImageOps.invert(img)
        if save_steps:
            img.save(f'{output_dir}/invert.png')

    return img


def otsu_threshold(img):
    """
    Calculate the optimal threshold using Otsu's method.
    """
    hist = img.histogram()
    total = sum(hist)
    sum_b, sum1_b, max_variance, threshold = 0, 0, 0, 0

    for i in range(256):
        sum_b += hist[i]
        sum1_b += i * hist[i]
        if sum_b == 0:
            continue
        sum_f = total - sum_b
        if sum_f == 0:
            break
        mean_b = sum1_b / sum_b
        mean_f = (sum(hist[i+1:]) - sum1_b) / sum_f if sum_f > 0 else 0
        variance_between = sum_b * sum_f * (mean_b - mean_f) ** 2
        if variance_between > max_variance:
            max_variance = variance_between
            threshold = i

    return 255 - threshold


def adjust_sharpening_params(img):
    """
    Dynamically adjust Unsharp Mask parameters based on image sharpness.
    """
    stat = ImageStat.Stat(img)
    contrast = stat.stddev[0]  # Measure standard deviation of pixel values

    if contrast < 20:
        return 10, 500, 10  # More aggressive sharpening for blurry images
    elif contrast < 50:
        return 15, 1000, 15  # Moderate sharpening
    elif contrast < 80:
        return 20, 1500, 20  # Minimal sharpening
    else:
        return 30, 2000, 30  # Very minimal sharpening for high-contrast images


if __name__ == '__main__':
    image_path = ''
    image = Image.open(image_path)
    transformed_image = transform_image(image,
                                        size_ratio=2,
                                        adaptive_sharpening=True,
                                        median_filter=True,
                                        contrast=1.5,
                                        blur=False,
                                        save_steps=True, output_dir='')