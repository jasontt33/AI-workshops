import PyPDF2

## write a python script to read a PDF file and then export all text to a text document
# Open the PDF file in read-binary mode
with open('Software Engineering Confluence Space.pdf', 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)

    # Create an empty string to store the extracted text
    extracted_text = ''

    # Iterate over each page in the PDF
    for page in pdf_reader.pages:
        # Extract the text from the page and append it to the extracted_text string
        extracted_text += page.extract_text()

# Open a text file in write mode and write the extracted text to it
with open('SE-confluence.txt', 'w') as file:
    file.write(extracted_text)
