import numpy as np
import pandas as pd

from dcp import celery, db

from dcp.models.data import CollectedData


@celery.task()
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
                                     "collection_instance", "order"])
    df.to_sql(name=CollectedData.__tablename__,
              con=db.engine, if_exists="append")

    # put message back onto the queue
    return "write successful"
