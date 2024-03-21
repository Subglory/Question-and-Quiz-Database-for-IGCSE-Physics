from ._anvil_designer import EditingAndViewingQuizTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EditingAndViewingQuiz(EditingAndViewingQuizTemplate):
  def __init__(self, quizName, savedQuestions, quizID, **properties):
    self.init_components(**properties)
    self.quizID = quizID
    self.quizName = self.textBox_quizName.text = quizName

    #List of questions that are saved for the quiz
    self.savedQuestions = set(savedQuestions)
    
    self.topics = ["Motion, forces and energy", "Thermal physics", "Waves", "Electricity and magnetism","Nuclear physics","Space physics"]
    
    #Sets the items of the dropdown box to the list of topics
    self.drop_down_topicsList.items = ["All"] + self.topics
    self.repeating_panel_questionsList.items = self.savedQuestions

  def drop_down_topicsList_change(self, **event_args):
    if self.drop_down_topicsList.selected_value == "All":
      self.drop_down_subtopicsList.items = []  
    else:
      #Assigns a dictionary of the topic name as the key and a list of subtopics as the value
      self.subtopics = anvil.server.call('getSubtopics')
      #Sets the values of the dropdown boxes to contain the list of subtopics that will be filtered
      topicChosen = self.drop_down_topicsList.selected_value
      self.drop_down_subtopicsList.items = ["All"] + self.subtopics[topicChosen]

  def button_applyFilter_click(self, **event_args):
    topicChosen = self.drop_down_topicsList.selected_value
    subtopicChosen = self.drop_down_subtopicsList.selected_value
    if self.check_box_notBeenUsed.checked:
      if topicChosen == "All":
        self.repeating_panel_questionsList.items = app_tables.questions.search(isUsed=False)
      elif subtopicChosen == "All":
        self.repeating_panel_questionsList.items = app_tables.questions.search(isUsed=False, topic= topicChosen)
      else:
        self.repeating_panel_questionsList.items = app_tables.questions.search(isUsed=False, topic= topicChosen, subtopic= subtopicChosen)
    else:
      if topicChosen == "All":
        self.repeating_panel_questionsList.items = app_tables.questions.search()
      elif subtopicChosen == "All":
        self.repeating_panel_questionsList.items = app_tables.questions.search(topic= topicChosen)
      else:
        self.repeating_panel_questionsList.items = app_tables.questions.search(topic= topicChosen, subtopic= subtopicChosen)

    if len(self.repeating_panel_questionsList.items) == 0:
      self.label_noResults.visible = True
    else:
      self.label_noResults.visible = False

  def button_viewAll_click(self, **event_args):
    self.repeating_panel_questionsList.items = app_tables.questions.search()
    self.button_saveQuiz.visible = False
    self.card_filter.visible = True

  def button_viewSaved_click(self, **event_args):
    self.repeating_panel_questionsList.items = self.savedQuestions
    self.button_saveQuiz.visible = True
    self.card_filter.visible = False

  def button_saveQuiz_click(self, **event_args):
    if self.textBox_quizName.text == "":
      alert("You must put a name for this quiz")
    else:
      quizToEdit = app_tables.quizzes.get_by_id(self.quizID)
      quizToEdit['quizName'] = self.textBox_quizName.text
      quizToEdit['questionsIncluded'] = list(self.savedQuestions)
      alert("Quiz has successfully been saved")
      open_form("Homepage.Quizzes")

  def back_button_click(self, **event_args):
    open_form('Homepage.Quizzes')