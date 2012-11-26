# -*- encoding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


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

class GoalHandler(webapp.RequestHandler):

    def get(self):
        html_title = 'Create a new goal'
        goal_author = 'default_author'
        goal_name = self.request.get('goalName')

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

            template_values = {
                'html_title': html_title,
                'goal': goal
            }

            self.response.out.write(template.render('newGoalPage.html', template_values))
        else:
            template_values = {
            'html_title': html_title
            }

            self.response.out.write(template.render('newGoalPage.html', template_values))

class GoalViewerHandler(webapp.RequestHandler):

    def get(self):
        html_title = 'View your goals'

        goal_author = 'default_author'

        action = self.request.get('action')

        if action == 'Remove':
            goal_to_remove = self.request.get('goalName')
            q = db.GqlQuery("SELECT __key__ FROM Goal WHERE name = :1", goal_to_remove)
            results = q.get()
            db.delete(results)

        if action == 'Check':
            goal_to_finish = self.request.get('goalName')
            goal_to_remove = self.request.get('goalName')
            q = db.GqlQuery("SELECT * FROM Goal WHERE name = :1", goal_to_finish)
            result = q.get()
            result.finished = True
            db.put(result)

        goals = Goal.all()
        goals.ancestor(goal_key(goal_author))
        goals.filter("finished = ", False)

        finishedGoals = Goal.all()
        finishedGoals.ancestor(goal_key(goal_author))
        finishedGoals.filter("finished = ", True)

        template_values = {
            'html_title': html_title,
            'goals' : goals,
            'finishedGoals' : finishedGoals,
            'goalsNumber' : goals.count(),
            'fGoalsNumber' : finishedGoals.count()
        }

        self.response.out.write(template.render('listAllGoalsPage.html', template_values))

class MainHandler(webapp.RequestHandler):

    def get(self):
        html_title = 'Improve!'
        template_values = {
            'html_title': html_title
        }
        self.response.out.write(template.render('index.html', template_values))

    def post(self):
        html_title = 'Improve!'
        template_values = {
            'html_title': html_title,
        }
        self.response.out.write(template.render('index.html', template_values))

def main():
    application = webapp.WSGIApplication(
                                         [('/', MainHandler),
                                         ('/newGoal', GoalHandler),
                                         ('/goalViewer', GoalViewerHandler)],
                                         debug=True)
    run_wsgi_app(application)
if __name__ is '__main__':
    main()