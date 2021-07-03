from flask import current_app
import numpy as np
import pandas as pd

from dcp import celery, db

from dcp.models.data import CollectedData

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def store_stream_data(data: np.ndarray):
    """Celery task responsible for storing a chunk of
    streamed data to the database.

    Args:
        data (numpy.ndarray): OpenBCI data to store to the database.
    """
    df = pd.DataFrame(data, columns=["channel_1", "channel_2", "channel_3",
                                     "channel_4", "channel_5", "channel_6",
                                     "channel_7", "channel_8",
                                     "is_subject_anxious",
                                     "collection_instance_id", "order"])
    collected_data = [CollectedData(
        channel_1=row.channel_1,
        channel_2=row.channel_2,
        channel_3=row.channel_3,
        channel_4=row.channel_4,
        channel_5=row.channel_5,
        channel_6=row.channel_6,
        channel_7=row.channel_7,
        channel_8=row.channel_8,
        is_subject_anxious=row.is_subject_anxious,
        collection_instance_id=row.collection_instance_id,
        order=row.order,
    )
        for row in df.itertuples(index=False)
    ]
    logger.info(f"Collected data: {collected_data}")

    db.session.add_all(collected_data)
    db.session.commit()

    return "Successfully wrote {} samples.".format(len(collected_data))

# CELERY TEST TASK
# bind=True means the first argument to the task will always be the
# task instance (self)


@celery.task(bind=True)
def add(self, x, y):
    from celery.states import state, PENDING, SUCCESS
    self.update_state(state=state(PENDING), meta='Got Request - Starting work')
    import random
    import time
    num = random.randrange(5, 10)
    self.update_state(task_id=self.id,
                      state=state(PENDING),
                      meta='Starting to sleep {}s'.format(num))
    time.sleep(num)
    num = random.randrange(5, 10)
    self.update_state(task_id=self.id,
                      state=state(PENDING),
                      meta='Continuing to sleep {}s'.format(num))
    time.sleep(num)
    self.update_state(task_id=self.id, state=state(
        SUCCESS), meta="Work finished!")
    logger.info("hello")
    return x + y
