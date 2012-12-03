# -*- encoding: utf-8 -*-

import facebook
import logging

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


FACEBOOK_APP_ID = "435215956532387"
FACEBOOK_APP_SECRET = "a6eddd2d723debb7dd59d4e0e7cb4eee"


class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    firstName = db.StringProperty(required=True)
    lastName = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    friends = db.StringListProperty()    

class Goal(db.Model):
    """Models an individual Goal"""
    name = db.StringProperty()
    category = db.StringProperty()
    description = db.StringProperty(multiline=True)
    dueDate = db.StringProperty()
    public = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    finished = db.BooleanProperty()

def goal_key(goal_author):
  """Constructs a Datastore key for a Goal entity with goal_author."""
  return db.Key.from_path('Goal', goal_author)


class BaseHandler(webapp.RequestHandler):

    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(
                self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                firstName=profile["first_name"],
                                lastName=profile["last_name"],
                                profile_url=profile["link"],
                                access_token=cookie["access_token"])
                    friendData = graph.get_connections("me", "friends")
                    user.friends = [friend["id"] for friend in friendData["data"]]
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        return self._current_user

class GoalViewerHandler(BaseHandler):

    def get(self):
        html_title = 'View your goals'

        if self.current_user:
            goal_author = self.current_user.id
        else:
            goal_author = 'none'

        action = self.request.get('action')

        if action == 'Remove':
            goal_to_remove = self.request.get('goalName')
            q = db.GqlQuery("SELECT __key__ FROM Goal WHERE name = :1", goal_to_remove)
            results = q.get()
            db.delete(results)

        if action == 'Accomplished!':
            goal_to_finish = self.request.get('goalName')
            goal_to_remove = self.request.get('goalName')
            q = db.GqlQuery("SELECT * FROM Goal WHERE name = :1", goal_to_finish)
            result = q.get()
            result.finished = True
            db.put(result)

        goals = Goal.all()
        goals.ancestor(goal_key(goal_author))
        goals.filter("finished = ", False)
        goals.order("-created")

        finishedGoals = Goal.all()
        finishedGoals.ancestor(goal_key(goal_author))
        finishedGoals.filter("finished = ", True)

        template_values = {
            'html_title': html_title,
            'goals' : goals,
            'finishedGoals' : finishedGoals,
            'goalsNumber' : goals.count(),
            'fGoalsNumber' : finishedGoals.count(),
            'current_user' : self.current_user
        }

        self.response.out.write(template.render('listAllGoalsPage.html', template_values))

class FriendsHandler(BaseHandler):

    def get(self):
        html_title = "Your friends' goals"

        friendGoals = {}
        if self.current_user:
            for friendID in self.current_user.friends:
                # checking if the friend is using our app
                user = User.get_by_key_name(friendID)
                if user:
                    goalList = []
                    goals = Goal.all()
                    goals.ancestor(goal_key(friendID))
                    # retrieving friend finished public goals
                    goals.filter("public = ", True).filter("finished = ", False)
                    for goal in goals.run(limit=2):
                        goalList.append(goal)
                    if len(goalList) > 0:
                        friendGoals[user] = goalList

        template_values = {
            'current_user' : self.current_user,
            'html_title': html_title,
            'friendGoals': friendGoals
        }
        self.response.out.write(template.render('friendGoals.html', template_values))


class AboutHandler(BaseHandler):

    def get(self):
        html_title = 'About us'

        template_values = {
            'current_user' : self.current_user,
            'html_title': html_title
        }
        self.response.out.write(template.render('about.html', template_values))

class CookieErrorHandler(BaseHandler):

    def get(self):
        html_title = 'Cookies disabled'

        template_values = {
            'html_title': html_title
        }
        self.response.out.write(template.render('cookiesDisabledPage.html', template_values)) 

class GoalHandler(BaseHandler):

    def get(self):
        self.post()

    def post(self):
        html_title = 'Create a new goal'
        goal_name = self.request.get('goalName')

        if self.current_user:
            goal_author = self.current_user.id
        else:
            goal_author = 'none'

        goal = None
        if goal_name:
            goal = Goal(parent=goal_key(goal_author))

            goal.name = goal_name
            goal.category = self.request.get('goalType')
            goal.description = self.request.get('goalDescription')
            dueDate = self.request.get('goalDueDate')
            if dueDate:
                goal.dueDate = dueDate
            isPublic = self.request.get('goalPublic')
            if isPublic == 'public':
                goal.public = True
            else:
                goal.public = False
            goal.finished = False
            ## save new goal in DB    
            goal.put()
            self.redirect("/goalViewer")
        else:
            friendGoals = {}
            if self.current_user:
                for friendID in self.current_user.friends:
                    # checking if the friend is using our app
                    user = User.get_by_key_name(friendID)
                    if user:
                        goalList = []
                        goals = Goal.all()
                        goals.ancestor(goal_key(friendID))
                        # retrieving friend finished public goals
                        goals.filter("public = ", True).filter("finished = ", False)
                        for goal in goals.run(limit=2):
                            goalList.append(goal)
                        if len(goalList) > 0:
                            friendGoals[user.name] = goalList

            template_values = {
                'html_title': html_title,
                'facebook_app_id' : FACEBOOK_APP_ID,
                'goal': goal,
                'current_user' : self.current_user,
                'friendGoals': friendGoals
            }

            self.response.out.write(template.render('newGoalPage.html', template_values))

def main():
    application = webapp.WSGIApplication(
                                         [('/', GoalHandler),
                                         ('/goalViewer', GoalViewerHandler),
                                         ('/friends', FriendsHandler),
                                         ('/about', AboutHandler),
                                         ('/cookiesDisabled', CookieErrorHandler)],
                                         debug=False)
    run_wsgi_app(application)
if __name__ == '__main__':
    main()