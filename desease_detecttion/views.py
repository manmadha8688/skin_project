from django.shortcuts import render

from django.core.files.uploadedfile import InMemoryUploadedFile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image, UnidentifiedImageError

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
model = load_model("skin_cnn.h5")

import cv2

disease_info = {
    
    "Melanocytic Nevi": {
        "symptoms": "Small, pigmented, round or oval skin growths, commonly called moles.",
        "causes": "Accumulation of melanocytes (pigment cells) due to genetic factors or sun exposure.",
        "treatment": "Usually benign; removal via excision or laser therapy if changes in shape, color, or size occur.",
        "severity": "Mild"
    },
    "Actinic Keratosis": {
        "symptoms": "Rough, scaly, or crusty patches on sun-exposed areas, such as the face, ears, hands, and scalp.",
        "causes": "Chronic UV radiation exposure, particularly in fair-skinned individuals.",
        "treatment": "Topical chemotherapy (5-fluorouracil), cryotherapy, photodynamic therapy, or surgical excision if necessary.",
        "severity": "Moderate"
    },
    "Squamous Cell Carcinoma": {
        "symptoms": "Firm, red nodules or scaly, crusted sores that may bleed or ulcerate.",
        "causes": "Prolonged UV exposure, weakened immune system, history of precancerous skin lesions.",
        "treatment": "Surgical excision, Mohs surgery, radiation therapy, or targeted immunotherapy in advanced cases.",
        "severity": "Severe"
    },
    "Seborrheic Keratosis": {
        "symptoms": "Waxy, raised, wart-like brown, black, or tan growths on the skin surface.",
        "causes": "Unclear, but linked to aging and genetic factors.",
        "treatment": "Harmless; treatment options include cryotherapy, laser therapy, or curettage if symptomatic or cosmetically undesired.",
        "severity": "Mild"
    },
    "Dermatofibroma": {
        "symptoms": "Small, firm, reddish-brown or purple nodules, often found on the legs or arms.",
        "causes": "Fibrous overgrowth due to minor skin trauma (insect bites, scratches).",
        "treatment": "Generally requires no treatment; surgical excision if painful or bothersome.",
        "severity": "Mild"
    },
    "Melanoma": {
        "symptoms": "Asymmetrical, irregularly bordered, multi-colored moles that change in size, shape, or texture.",
        "causes": "Intense UV exposure, fair skin, genetic predisposition, history of sunburns.",
        "treatment": "Early-stage excision, lymph node biopsy, chemotherapy, immunotherapy, or targeted therapy for advanced cases.",
        "severity": "Severe"
    },
    "Vascular Lesions": {
        "symptoms": "Red, purple, or blue skin discoloration due to abnormal blood vessels or increased blood supply.",
        "causes": "Congenital conditions (birthmarks), aging, or underlying vascular disorders.",
        "treatment": "Laser therapy, sclerotherapy, or surgical removal if symptomatic or cosmetically concerning.",
        "severity": "Moderate"
    },
    "Basal Cell Carcinoma": {
        "symptoms": "Shiny, pearly, flesh-colored or pink bumps that may ulcerate or bleed over time.",
        "causes": "Cumulative UV exposure, fair skin, exposure to radiation or carcinogens.",
        "treatment": "Mohs surgery, topical chemotherapy, radiation therapy, or targeted therapy for inoperable cases.",
        "severity": "Moderate"
    }
}

CLASS_NAMES= {
    0: 'Actinic Keratosis',
    1: 'Basal Cell Carcinoma',
    2: 'Seborrheic Keratosis',
    3: 'Dermatofibroma',
    4: 'Melanoma',
    5: 'Melanocytic Nevi',
    6: 'Squamous Cell Carcinoma',
    7: 'Vascular Lesions'
}

def preprocess_uploaded_image(uploaded_file):
    # Read image bytes from the uploaded file
    file_bytes = uploaded_file.read()
    np_array = np.frombuffer(file_bytes, np.uint8)
    
    # Decode the numpy array as an image
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    if img is None:
        print("Error: Could not decode image")
        return None

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (28,28))
    img = img.astype('float32') / 255.0  # Normalized
    img = img.reshape(-1, 28, 28, 3)

    return img

# Create your views here.
def home(request):
    return render(request,'disease-detection/upload.html')
def result(request):
    if request.method == "POST":
        try:
            uploaded_image = request.FILES.get("image")

            # ✅ Check if an image was uploaded
            if not uploaded_image:
                return render(request, 'disease-detection/upload.html', {
                    "error": "No image uploaded. Please upload a valid image."
                })

            # ✅ Check if uploaded file is an image
            if not isinstance(uploaded_image, InMemoryUploadedFile) or not uploaded_image.content_type.startswith("image"):
                return render(request, 'disease-detection/upload.html', {
                    "error": "Invalid file format. Please upload an image."
                })

            # ✅ Open and process the image
            try:
                
                img = preprocess_uploaded_image(uploaded_image)  # Resize
                
            except UnidentifiedImageError:
                return render(request, 'disease-detection/upload.html', {
                    "error": "Uploaded file is not a valid image."
                })

            # ✅ Predict using the model
            if model is None:
                return render(request, 'disease-detection/upload.html', {
                    "error": "Model is not loaded. Please try again later."
                })

            prediction = model.predict(img)
            predicted_index = np.argmax(prediction)  # Get index of highest probability
            predicted_class = CLASS_NAMES[predicted_index]  # Get full name
            confidence= np.max(prediction) * 100  # Get confidence score in percentage
            
            img = Image.open(uploaded_image)
            img = img.resize((100,75))  # Resize
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0
            # ✅ Convert image to base64 for rendering
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_data_url = f"data:image/jpeg;base64,{img_base64}"

            request.session["uploaded_image"] = img_base64
            request.session["predicted_class"] = predicted_class
            request.session["confidence"] = float(confidence)
            request.session["severity"] = disease_info[predicted_class]["severity"]
            request.session["symptoms"] = disease_info[predicted_class]["symptoms"]
            request.session["causes"] = disease_info[predicted_class]["causes"]
            request.session["treatment"] = disease_info[predicted_class]["treatment"]


            return render(request, 'disease-detection/result.html', {
            
            "image": img_data_url,

           'class':predicted_class,
           "confidence":confidence,
           'severity':disease_info[predicted_class]["severity"],

           'symptoms':disease_info[predicted_class]["symptoms"],
           'causes':disease_info[predicted_class]["causes"],
           'treatment':disease_info[predicted_class]["treatment"],
    
            })

        except Exception as e:
            return render(request, 'disease-detection/upload.html', {
                "error": f"An unexpected error occurred: {str(e)} "
            })
        

        
    return render(request, 'disease-detection/upload.html', {
                "error": "An unexpected error occurred..!\n Please try again...!"
            })


def download_report(request):
    # Ensure the image is available in the session
    img_base64 = request.session.get("uploaded_image")
    predicted_class = request.session.get("predicted_class", "Unknown")
    confidence = request.session.get("confidence", 0)
    severity = request.session.get("severity", "Unknown")
    symptoms = request.session.get("symptoms", "N/A")
    causes = request.session.get("causes", "N/A")
    treatment = request.session.get("treatment", "N/A")

    # Set up the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Dermatology_Report.pdf"'

    # Create canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Standard A4 size page

    # Centering calculations
    center_x = width / 2

    # Report Title (Centered)
    p.setFont("Helvetica-Bold", 18)
    title_text = "Dermatology Diagnosis Report"
    title_width = p.stringWidth(title_text, "Helvetica-Bold", 18)
    p.drawString(center_x - (title_width / 2), height - 50, title_text)

    # Draw a separator line below title
    p.setLineWidth(1)
    p.line(50, height - 65, width - 50, height - 65)

    # Place Image (Centered)
    if img_base64:
        image_data = base64.b64decode(img_base64)
        img = ImageReader(BytesIO(image_data))
        image_width = 200
        image_height = 200
        p.drawImage(img, center_x - (image_width / 2), height - 300, width=image_width, height=image_height)

    # Diagnosis Details (Below Image, Centered Text)
    p.setFont("Helvetica", 12)
    start_y = height - 320  # Position below the image
    line_spacing = 20

    details = [
        f"Diagnosis: {predicted_class}",
        f"Confidence Level: {confidence}%",
        f"Severity: {severity}",
        f"Symptoms: {symptoms}",
        f"Causes: {causes}",
        f"Treatment: {treatment}",
    ]

    for i, text in enumerate(details):
        text_width = p.stringWidth(text, "Helvetica", 12)
        p.drawString(center_x - (text_width / 2), start_y - (i * line_spacing), text)

    # Save the PDF
    p.showPage()
    p.save()

    return response
