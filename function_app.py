import logging
import tempfile
import os
import azure.functions as func # type: ignore
from pdf2image import convert_from_path
import pytesseract

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing PDF for OCR.')
    logging.info('Python HTTP trigger function processed a request.')

# ////////////////////////////////////////////////////
    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
    
# ////////////////////////////////////////

# Get PDF file from request
    # pdf_file = req.files['file']
    # images = convert_from_path(pdf_file)

    # # Extract text from images
    # text = ""
    # for image in images:
    #     text += pytesseract.image_to_string(image)

    # return func.HttpResponse(text, status_code=200)

# ///////////////////////////////////////////////

    temp_file_path = None  # Initialize variable for cleanup

    try:
        # Ensure 'file' exists in request files
        if 'file' not in req.files:
            return func.HttpResponse("File not found in request.", status_code=400)

        pdf_file = req.files['file']

        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_file.read())
            temp_file_path = temp_file.name
        
        # Convert PDF to images
        images = convert_from_path(temp_file_path)

        # Extract text from images
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)

        # Clean up the temporary file
        os.remove(temp_file_path)

        return func.HttpResponse(text, status_code=200)

    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return func.HttpResponse("An error occurred while processing the file.", status_code=500)

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)