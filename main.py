import cv2
import imutils
import pytesseract

def plate_to_string(dev_mode, image_path, tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Original image
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=300)
    #cv2.imshow("original image", image)

    # Grey-scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("greyed image", gray_image)

    # Smoothing of the grey-scale image
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    #cv2.imshow("smoothened image", gray_image)

    # Black/white edged detection
    edged = cv2.Canny(gray_image, 30, 200)
    #cv2.imshow("edged image", edged)

    # Contour detection
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1 = image.copy()
    cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
    #cv2.imshow("contours", image1)

    # Pick top 30 contours
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    screenCnt = None
    image2 = image.copy()
    cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
    #cv2.imshow("Top 30 contours", image2)

    # For every contour, create a new image framing the specific contour in a rectangle
    # Save only the rectangle with approximately the shape of a license plate
    i = 1
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx

            x, y, w, h = cv2.boundingRect(c)
            new_img = image[y:y + h, x:x + w]
            cv2.imwrite('./output_img/' + str(i) + '.png', new_img)
            i += 1
            break

    # Add the selected contour to the original image
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    cv2.imshow("image with detected license plate", image)

    # Crop the image and extract the text in the image
    Cropped_loc = './output_img/1.png'
    cv2.imshow("cropped", cv2.imread(Cropped_loc))
    plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
    print("Number plate is:", plate)

    # To keep the images open for visual inspection - Set dev_mode = True
    if dev_mode:
        cv2.waitKey(0)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dev_mode = True # Change to false in production
    image_path = r'C:\Users\adm.andersj\PycharmProjects\Snakers_ALPR\test_img\test_plate.jpg'
    tesseract_path = r'C:\Users\adm.andersj\AppData\Local\Programs\Tesseract-OCR\\tesseract'
    plate_to_string(dev_mode, image_path, tesseract_path)


