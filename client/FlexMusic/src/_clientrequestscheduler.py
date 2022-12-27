class _ClientRequestScheduler(object):
    '''
    Request scheduler for FlexMusic client.\n
    For internal use only
    '''

    def __init__(self):
        self._job_queue = []
        self._finished_jobs = 0

    @property
    def latest_job_id(self) -> int:
        return len(self._job_queue)

    def queue_job(self) -> int:
        self._job_queue.append(job_id := int(len(self._job_queue)))
        return job_id

    def finish_job(self):
        self._finished_jobs += 1

    def ready(self, id) -> bool:
        if id == self._finished_jobs:
            return True
        else:
            False