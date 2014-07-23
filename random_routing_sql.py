chunks = (Chunk.objects
			.filter(file__submission__milestone=review_milestone.submit_milestone)
	    	# remove chunks that have too few student-generated lines
			.exclude(student_lines__lt=review_milestone.min_student_lines)
			# remove chunks that aren't selected for review
	    	.exclude(name__in=list_chunks_to_exclude(review_milestone))
	    	# .values('id', 'name', 'cluster_id', 'file__submission', 'class_type', 'student_lines')\
	    	.select_related('id','file__submission__id','file__submission__authors'))

	if not simulate:
		# remove chunks already assigned to reviewer
	    chunks = (chunks.exclude(tasks__reviewer=r)
						# remove chunks that already have enough reviewers
    					.annotate(num_tasks=Count('tasks')).exclude(num_tasks__gte=num_tasks_for_user(review_milestone, r)))

	if simulate:
		# remove chunks that already have enough reviewers
		chunks = chunks.annotate(num_tasks=len(chunk_id_task_map['id'])).exclude(num_tasks__gte=num_tasks_for_user(review_milestone, r))
	# remove chunks that the reviewer authored
	chunks_to_choose_from = [c for c in chunks if r not in c.file.submission.authors.filter()]




#######################################################################################
# paste this into a terminal to test SQL
# cd Desktop/caesar-web
# vagrant ssh
# cd /var/django/caesar/
# ./manage.py shell
from __future__ import division
from collections import namedtuple, defaultdict
import itertools
from django.db.models import Count
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models.query import prefetch_related_objects
from tasks.models import Task, app_settings
from chunks.models import Chunk, ReviewMilestone
from accounts.models import Member
import random
import sys
import logging
from random import shuffle

def list_chunks_to_exclude(review_milestone):
 to_exclude = review_milestone.chunks_to_exclude
 if to_exclude == None:
  return []
 return to_exclude.split(",")

def num_tasks_for_user(review_milestone, user):
 member = Member.objects.get(user=user, semester=review_milestone.assignment.semester)
 if member.role == Member.STUDENT:
  return review_milestone.student_count
 elif member.role == Member.TEACHER:
  return review_milestone.staff_count
 elif member.role == Member.VOLUNTEER:
  return review_milestone.alum_count
 else:
  return 0

review_milestone = ReviewMilestone.objects.get(id=3)

# call str(QuerySet.query) to get the SQL equivalent

# django ORM call
c = (Chunk.objects.filter(file__submission__milestone=review_milestone.submit_milestone)
.exclude(student_lines__lt=review_milestone.min_student_lines)
.exclude(name__in=list_chunks_to_exclude(review_milestone))
.select_related('id','file__submission__id','file__submission__authors'))
# raw SQL equivalent
Chunk.objects.raw('''
	SELECT * FROM "chunks"
	INNER JOIN "files" ON ("chunks"."file_id" = "files"."id")
	INNER JOIN "submissions" ON ("files"."submission_id" = "submissions"."id")
	WHERE ("submissions"."milestone_id" = 1  AND NOT ("chunks"."student_lines" < 30 ))''')

# django ORM call
Chunk.objects.filter(file__submission__milestone=review_milestone.submit_milestone)
# raw SQL equivalent
Chunk.objects.raw('''
	SELECT * FROM `chunks` 
	INNER JOIN `files` ON (`chunks`.`file_id` = `files`.`id`) 
	INNER JOIN `submissions` ON (`files`.`submission_id` = `submissions`.`id`) 
	WHERE `submissions`.`milestone_id` = %s''',[review_milestone.submit_milestone])





chunks_to_choose_from = [c for c in chunks if r not in c.file.submission.authors.filter()]
# SQL equivalent
Chunk.objects.raw('''
	SELECT DISTINCT * FROM `chunks` 
	JOIN files on chunks.file_id=files.id
	JOIN submissions on files.submission_id=submissions.id
	JOIN submissions_authors on submissions.id=submissions_authors.submission_id
	WHERE submissions.milestone_id=%s AND NOT (user_id=%s)
	''', [submit_milestone.id, django_user.id])
# extra() equivalent
Chunk.objects.extra(select={"DISTINCT *":"chunks"}, where=["submissions.milestone_id=%s", "user_id!=%s"], params=[str(submit_milestone.id), str(django_user.id)], tables=['chunks_files as files','chunks_files_submissions as submissions','chunks_files_submissions_authors as submissions_authors'], order_by=None, select_params=None)


# what if I preform a query on File (f) and then exclude all c.files that are/aren't in f?
f = File.objects.filter(submission__milestone=review_milestone.submit_milestone,submission__authors__contains=r)
c.objects.exclude(file__in=f)





