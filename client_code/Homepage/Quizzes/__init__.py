from ._anvil_designer import QuizzesTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Quizzes(QuizzesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  #Goes back to the previous form
  def back_button_click(self, **event_args):
    open_form('Homepage')