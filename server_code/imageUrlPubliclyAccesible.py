import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.http_endpoint('/images/:id')
def get_image(id):
    print(f"Request was made for image with id {id}")
    imageRow = app_tables.questions.get_by_id(id)
    image = imageRow['image']
    return image

@anvil.server.callable()
def get_image_url_from_id(id):
    return f"{anvil.server.get_api_origin()}/images/{id}"