import cv2
import numpy as np

#https://blog.csdn.net/qq_38269799/article/details/80687830
#https://blog.csdn.net/qq_40716944/article/details/80098005

image = cv2.imread('./s.jpg')
image_blur = np.hstack(      # 结果图像的水平拼接
    [cv2.blur(image, (3, 3)),  # kernel_size为3×3
    cv2.blur(image, (5, 5)),
    cv2.blur(image, (7, 7))]  # 能够看到图像变得越来越模糊
)
cv2.imwrite('blur_of_diff_size.jpg', image_blur)

image_gaussian = np.hstack([
    cv2.GaussianBlur(image, (3, 3), 0),
    cv2.GaussianBlur(image, (5, 5), 0),
    cv2.GaussianBlur(image, (7, 7), 0)   # 可以看出效果没有均值滤波模糊的那么厉害
])
cv2.imwrite('blur_of_diff_gaussian_size.jpg', image_gaussian)

def make_sp_noise(image, ratio):
    """人为的为图像添加椒盐噪声，ratio规定了噪声点占全局像素的比例"""
    h, w = image.shape[:2]
    image_copy = image.copy()
    nums = int(h * w * ratio) # 椒盐噪声点占比
    for i in range(nums):
        row = np.random.randint(0, h)
        col = np.random.randint(0, w)
        if i % 2 == 0:
            image_copy[row, col] = 255
        else:
            image_copy[row, col] = 0
    return image_copy

image_with_sp = make_sp_noise(image, 0.7)
cv2.imwrite('image_with_sp.jpg', image_with_sp)
image_mid_blur = np.hstack([
    cv2.medianBlur(image_with_sp, 3),
    cv2.medianBlur(image_with_sp, 5),
    cv2.medianBlur(image_with_sp, 7)  # 邻域越大，过滤椒盐噪声效果越好，但是图像质量也会下降明显。除非非常密集椒盐噪声，否则不推荐Ksize=7这么大的卷积核
])
cv2.imwrite('image_remove_noise.jpg', image_mid_blur)
# 对比：高斯滤波对滤除椒盐噪声
image_gaussian_compare = np.hstack([
    cv2.GaussianBlur(image_with_sp, (3, 3), 0),
    cv2.GaussianBlur(image_with_sp, (5, 5), 0),
    cv2.GaussianBlur(image_with_sp, (7, 7), 0)
])
cv2.imwrite('image_remove_noise_compare.jpg', image_gaussian_compare)

image = cv2.imread('./beach.png')
image_bilater = np.hstack([
    cv2.bilateralFilter(image, 5, 21, 21),
    cv2.bilateralFilter(image, 7, 31, 31),
    cv2.bilateralFilter(image, 9, 41, 41)
])
cv2.imwrite('image_bilater.jpg', image_bilater)
