from reportlab.pdfgen import canvas

def generate_certificate(user, course):
    file_name = f"certificate_{user.username}.pdf"
    c = canvas.Canvas(file_name)
    c.drawString(100, 750, "Certificate of Completion")
    c.drawString(100, 700, f"Name: {user.username}")
    c.drawString(100, 650, f"Course: {course.title}")
    c.save()
    return file_name
