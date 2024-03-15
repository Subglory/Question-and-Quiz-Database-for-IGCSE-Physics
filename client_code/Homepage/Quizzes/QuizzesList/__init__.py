from ._anvil_designer import QuizzesListTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class QuizzesList(QuizzesListTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_quizName.text = self.item['quizName']

