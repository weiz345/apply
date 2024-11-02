# event_listeners.py

from sqlalchemy import event
import threading
from models import Resume, Posting
from processing import process_new_resume, process_new_posting

# Event listener for Resume after insert
@event.listens_for(Resume, 'after_insert')
def receive_after_insert_resume(mapper, connection, target):
    threading.Thread(target=process_new_resume, args=(target.id,)).start()

# Event listener for Posting after insert
@event.listens_for(Posting, 'after_insert')
def receive_after_insert_posting(mapper, connection, target):
    threading.Thread(target=process_new_posting, args=(target.id,)).start()
