# realTimeChat-Django-Channels
Real time chat application

To run this application:
1. Create a virtual environment `virtualenv venv`
2. And activate it `source venv/bin/activate`(for ubuntu) `venv\Scripts\activate`(for windows)
3. Then install dependencies `pip install -r requirements.txt`
4. Migrate to database `python manage.py migrate`
5. Now run the server `python manage.py runserver`
   
APIs: 
1. api/ login 
2. api/ register
3. api/ users 
4. api/ online-users 
5. api/ chat/start/<int:pk> 
6. api/ suggested-friends/<int:user_id> 
7. ws://<host>/ws/users/<int:user_id> /
