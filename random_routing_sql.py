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

Chunk.objects.filter(file__submission__milestone=review_milestone.submit_milestone)
Chunk.objects.raw('''
	SELECT * FROM `chunks` 
	INNER JOIN `files` ON (`chunks`.`file_id` = `files`.`id`) 
	INNER JOIN `submissions` ON (`files`.`submission_id` = `submissions`.`id`) 
	WHERE `submissions`.`milestone_id` = %s''',[review_milestone.submit_milestone])


Chunk.objects.raw('''SELECT * FROM `chunks` join files on chunks.file_id=files.id ''')





.raw('''
SELECT files.submission_id, `chunks`.`id`, `chunks`.`file_id`, `chunks`.`name`, `chunks`.`start`, `chunks`.`end`, `chunks`.`cluster_id`, `chunks`.`created`, `chunks`.`modified`, `chunks`.`class_type`, `chunks`.`staff_portion`, `chunks`.`student_lines`, `chunks`.`chunk_info`
FROM `chunks` 
join files on chunks.file_id=files.id
join submissions on files.submission_id=submissions.id
join submissions_authors on submissions.id=submissions_authors.submission_id
where submissions.milestone_id=%s and not(user_id=%s)
            ''', [submit_milestone.id, django_user.id])