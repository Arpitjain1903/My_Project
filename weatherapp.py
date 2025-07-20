import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QVBoxLayout,QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
class weatherApp(QWidget) :
    def __init__(self):
        super().__init__()
        self.setGeometry(700,350,600,600)
        #self.setWindowIcon(QIcon("))
        self.city_label=QLabel("Enter The City Name :-> ",self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Submit",self)
        self.city_temperature=QLabel(self)
        self.emoji=QLabel("🌤️",self)
        self.Description_label=QLabel(self)
        self.initUi()
    def initUi(self):
         self.setWindowTitle("WeatherApp")
         
         vbox=QVBoxLayout()
         vbox.addWidget(self.city_label)
         vbox.addWidget(self.city_input)
         vbox.addWidget(self.get_weather_button)
         vbox.addWidget(self.city_temperature)
         vbox.addWidget(self.emoji)
         vbox.addWidget(self.Description_label)
         self.setLayout(vbox)
         self.city_label.setAlignment(Qt.AlignCenter)
         self.city_input.setAlignment(Qt.AlignCenter)
         self.emoji.setAlignment(Qt.AlignCenter)
         self.city_temperature.setAlignment(Qt.AlignCenter)
         self.Description_label.setAlignment(Qt.AlignCenter)

         self.city_label.setObjectName("city_label")
         self.city_input.setObjectName("city_input")
         self.get_weather_button.setObjectName("get_weather_button")
         self.city_temperature.setObjectName("city_temperature")
         self.emoji.setObjectName("emoji")
         self.Description_label.setObjectName("Description_label")

         self.setStyleSheet("""
          QLabel, QPushButton{font-family:calibri;}
          QLabel#city_label{
                            font-size:40px;
                            font-style:italic;}
          QLineEdit#city_input{
                            font-size:40px;
                            }
          QPushButton#get_weather_button{
                            font-size:30px;
                            font-weight:bold;}
          QLabel#city_temperature{
                            font-size:45px;
                            font-weight: bold;
                            }
          QLabel#emoji{
                            font-size:100px;
                            font-family:'Segoe UI emoji';
                        }
          QLabel#Description_label{
                            font-size:50px;
                            font-weight:bold;}
                            """)
         self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather (self):
        api_key="89c39696c952110898a64c22339e1589"
        city=self.city_input.text()
        url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try :
             response=requests.get(url)
             response.raise_for_status()
             data=response.json()
             if data["cod"]==200:
                self.display_weather(data)
             else:
                print(data)
        except requests.exceptions.HTTPError as httperror :
              match response.status_code:
                  case 400:
                      self.display_error("Bad Request\n Please check the the input")
                  case 401:
                      self.display_error("Unthorised\n Invalid api key")
                  case 403:
                      self.display_error("Forbidden\n Access is denied")
                  case 404:
                      self.display_error("Not Found\n City not found")
                  case 500:
                      self.display_error("Internal Server Error\n Please try again later")
                  case 502:
                      self.display_error("Bad Gateway\n Invaild response from the server")
                  case 503:
                      self.display_error("Service Unavailable\n Server is down")
                  case 504:
                      self.display_error("Gateway Timeout\n No response from the server")
                  case _:
                      self.display_error(f"Http erro occured\n{httperror}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\n Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error :\n The request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\n Check your url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error :\n {req_error}")
    def display_weather(self,data):
        temp=data["main"]["temp"]
        weather_id=data["weather"][0]["id"]
        weather_discrition=data["weather"][0]["description"].capitalize()
        self.Description_label.setText(weather_discrition)
        self.city_temperature.setText(f"{temp:.1f}°C")
        self.emoji.setText(self.get_emoji(weather_id))
    def display_error(self,massage):
        self.city_temperature.setText(massage)
        self.emoji.clear()
        self.Description_label.clear()
    @staticmethod
    def get_emoji(weather_id):
        if 200<=weather_id<=232:
            return "⛈️"
        elif 300<=weather_id<=321:
            return "🌦️"
        elif 500<=weather_id<=531:
            return "☔"
        elif 600<=weather_id<=622:
            return "☃️"
        elif 700<=weather_id<=741:
            return "🌫️"
        elif weather_id==781 :
            return "🌪️"
        elif weather_id==800:
            return "🌞"
        elif 801<=weather_id<=804:
            return "⛅"
        else :
            return ""
if __name__=="__main__":
    App=QApplication(sys.argv)
    Weather_app=weatherApp()
    Weather_app.show()
    sys.exit(App.exec_()) 
          