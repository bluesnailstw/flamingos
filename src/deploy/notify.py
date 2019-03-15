from functools import wraps
from django.utils import timezone
from tornado.websocket import WebSocketHandler
from django.conf import settings
from users.models import User
from django.contrib.sessions.models import Session
import json
from tornado.web import RequestHandler
from deploy.models import History, Task, TASK_STATUS
from tornado.escape import json_decode


def verify_user(func):
    @wraps(func)
    def with_verify_user(request, *args, **kwargs):
        session_key = request.get_cookie('sessionid')
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                if session and timezone.now() < session.expire_date:
                    user_id = session.get_decoded().get('_auth_user_id')
                    if user_id:
                        user = User.objects.get(id=user_id)
                        request.user = user
                        if user:
                            return func(request, *args, **kwargs)
            except Exception as e:
                print(e)
                pass
        try:
            request.close()
        except AttributeError:
            pass
        return None

    return with_verify_user


class NotifyHandler(WebSocketHandler):
    clients = set()

    def __init__(self, application, request, **kwargs):
        super(NotifyHandler, self).__init__(application, request, **kwargs)
        self.jobs = set()
        self.user: User = None

    @verify_user
    def open(self):
        NotifyHandler.clients.add(self)
        self.jobs = set((t.occupy for t in Task.objects.filter(status=TASK_STATUS[1][0], operator=self.user)))
        print('user %s opened websocket.' % self.user.name)

    def on_message(self, message):
        try:
            msg = json.loads(message)
            assert isinstance(msg, dict)
        except Exception as e:
            print(e)
            self.write_message(u"JSONDecodeError")
        else:
            action = msg.get('action')
            if action == 'add_job' and msg.get('job'):
                self.jobs.add(msg['job'])
            else:
                self.write_message(u'Unknown Action')

    def on_close(self):
        if self in NotifyHandler.clients:
            NotifyHandler.clients.remove(self)
            if self.user:
                print('user %s closed websocket.' % self.user.name)
            else:
                print('user nobody closed websocket.')
        else:
            print("WebSocket closed")

    @classmethod
    def send(cls, message,  user=None, job=None):
        for client in cls.clients:
            if client.user.name == user.name and job in client.jobs:
                client.write_message(message)

    @classmethod
    def broadcast(cls, message):
        for client in cls.clients:
            client.write_message(message)


def process_event(data: dict):
    job_id = data['jid']
    minion_id = data['id']
    task = Task.objects.filter(occupy=job_id, status=TASK_STATUS[1][0]).last()
    if task:
        task.barn.remove(minion_id)
        if not task.barn:
            task.status = TASK_STATUS[2][0]
        task.save()
        History.objects.create(job_id=job_id, minion_id=minion_id,
                               user=task.operator,
                               task=task, result=data)
        NotifyHandler.send(data, task.operator, job_id)
    else:
        print("indifference job [%s:%s]" % (job_id, minion_id))


class SaltEventHandler(RequestHandler):

    def post(self):
        data = json_decode(self.request.body)
        process_event(data)

        self.write("ok")
