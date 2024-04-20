from ._anvil_designer import QuizzesListTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.http
import webbrowser
import anvil.media

class QuizzesList(QuizzesListTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_quizName.text = self.item['quizName']
    self.quizID = self.item.get_id()

  #Deletes the quiz
  def button_delete_click(self, **event_args):
    #Asks for a confirmation if the user wants to delete the quiz
    c = confirm("Are you sure you want to delete  '" + self.item['quizName'] +"' ?")
    if c:
      resultsID = self.item['results'].get_id()
      resultsRow = app_tables.results.get_by_id(resultsID)
      resultsRow.delete()
      self.item.delete()
      self.remove_from_parent()

  #Opens the form to edit or view an already made quiz
  def button_editAndView_click(self, **event_args):
    open_form('Homepage.Quizzes.QuizzesList.EditingAndViewingQuiz', quizName = self.item['quizName'], savedQuestions = self.item['questionsIncluded'], quizID = self.quizID)

  #Creates a google forms from the quiz using a Google API
  def button_createGForms_click(self, **event_args):
    #Asks for authorization from the user
    anvil.google.auth.login(["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/forms.body"])
    accessToken = anvil.google.auth.get_user_access_token()
    
    #Creates a google form
    createGFormResponse = anvil.http.request("https://forms.googleapis.com/v1/forms/", method = "POST", json = True,
                          data = 
                          {
                            "info": {
                              "title": self.item['quizName']
                            }
                          },
                          headers = {'Authorization': 'Bearer ' + accessToken})
    
    formID = createGFormResponse["formId"]
    
    #Stores the json data for the questions to be added into the google form and converting it to the quiz
    jsonDataUpdate = {"requests": []}
    
    #Index 0 stores the data to of the request's list value stores the data to convert the form to a quiz
    jsonDataUpdate["requests"].append(
                                {
                                  "updateSettings": {
                                    "settings": {
                                      "quizSettings": {
                                        "isQuiz": True
                                      }
                                    },
                                    "updateMask": "quizSettings.isQuiz"
                                  }
                                })
    
    #Iterates through each question
    for i in range(len(self.item['questionsIncluded'])):
      question = self.item['questionsIncluded'][i]
      correctAnsValue = question[question['correctAnswer']]
      print(question)
      imageUrl = None
      
      #Adds the question to the array of requests
      jsonDataUpdate["requests"].append(
                            {
                              "createItem": {
                                "item": {
                                  "title": question['text'],
                                  "questionItem": {
                                    "question": {
                                      "required": True,
                                      "grading": {
                                        "correctAnswers": {
                                          "answers": [
                                            {
                                              "value": correctAnsValue
                                            }
                                          ]
                                        },
                                        "pointValue": 1
                                      },
                                      "choiceQuestion": {
                                        "shuffle": True,
                                        "type": "RADIO",
                                        "options": [
                                          {
                                            "value": question["option1"]
                                          },
                                          {
                                            "value": question['option2']
                                          },
                                          {
                                            "value": question['option3']
                                          },
                                          {
                                            "value": question['option4']
                                          }
                                        ]
                                      }
                                    }
                                  }
                                },
                                "location": {
                                  "index": i
                                }
                              }
                            }
      )
      
      #If the question has an image, adds an additional element to the dictionary for the json data containing the image details
      if question['image'] != None:
        imageUrl = anvil.server.call('getImageUrl', question.get_id())
        jsonDataUpdate['requests'][i+1]['createItem']['item']['questionItem']["image"] = {"sourceUri": imageUrl, "properties": {"alignment": "CENTER"}}
        
    #Adds all the questions to the google quiz form
    anvil.http.request(f"https://forms.googleapis.com/v1/forms/{formID}:batchUpdate", method = "POST", json = True,
                        data = jsonDataUpdate,
                        headers = {'Authorization': 'Bearer ' + accessToken})
    
    #Redirects to the google form to make any final edits
    formURL = f"https://docs.google.com/forms/d/{formID}/edit"
    webbrowser.open(formURL)

    alert("Google Form for quiz has been created. If you have not been redirected, open google drive")

  #Goes to the form containing all the results of the selected quiz
  def button_results_click(self, **event_args):
    open_form("Homepage.Quizzes.QuizzesList.QuizResults", quizID = self.quizID)