#Project Name: OtterFodder
#Team Members: Lead - Jose Cabrera, support: Kevin Olasava, Bohnny Vohnan
#Class: CST205 - Multimedia design and programming
#Date: 11-14-22 thru 12-14-22

#To run program:
- pip install Flask-Migrate
- pip install Flask-Reuploaded
- pip install flask-uploads
- pip install flask-bcrypt
- pip install flask-login
- pip install flask-sqlalchem
- pip install Flask-WTF
- pip install bootstrap-flask
- make sure the virtual environment is activated, run the command "flask --app app --debug run"
- head to the link provided on the terminal

#Project Description
This class project was inspired by the various dating apps/sites available like Tinder, Hinge,etc, but oriented towards students at our school, hence the first part of the name reflecting our mascot @CSUMB. At the start you'll see the homepage, as you scroll down you can see our "About Us" section, followed by our very reputable reviews. On the top of the page there are options, you should begin with creating a profile "sign up".The page allows the user to create an account, provide a name, password, username, bio, height, gender, weight, and major. Upon clicking register after entering your information, you should see your profile with a default pic from one of the founders. By clicking Otters in the sea you will be navigated toards the "swiping" page where you can see various API generated profiles where you can "like" and "dislike". This was our go-to options since we did not want to scrape real prifiles. In the home page there was also a contact us section with our contact info.

Project link - https://github.com/novicecodersnail/CS205.git

#Future Project Ventures
- We would like to explore the upload picture functionality which is something the team toyed around with, but couldn't get it to stay associated with the registered user.
- Store the liked users into a list and be able to display them in a "liked" page with all their information. Due to the duration of the project, we couldn't explore this option since we'd need to learn how to store each liked user and its associated details and picture.
- "Delete" disliked users so there are no repeats
- Implement a chat function 
- Implement matching system that is similar to tinder, but to our specific criteria(weight, heiht, gender, etc.)
- Being able to see/match with other registered users
- Implementing an Edit feature to edit profile details and preferences
