# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging

from flask import abort
from rq.job import Job

from api.api import Resource
from worker import conn


class AdversarialExamplesId(Resource):
    def get(self, id):
        try:
            job = Job.fetch(id, connection=conn)
        except:
            logging.log(logging.INFO, "GET /api/adversarial_samples/{}. Job ID not found".format(id))
            abort(404, "Job ID not found.")
            return
        if job.is_finished:
            # redirect to job output API
            return {"job-status": job.status}, 200, {'Location': "api/adversarial_samples/{}/output".format(id)}
        return {"job-status": job.status}, 200, None

    def delete(self, id):
        try:
            job = Job.fetch(id, connection=conn)
        except:
            logging.log(logging.INFO, "DELETE /api/adversarial_samples/{} - Job ID not found.".format(id))
            abort(404, "Job ID not found.")
            return

        job.delete(remove_from_queue=True)
        return None, 200, None