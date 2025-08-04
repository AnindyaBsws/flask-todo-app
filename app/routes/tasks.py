from flask import Flask, Blueprint, session, redirect, render_template, url_for, request,flash
from app import db
from app.models import Task
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

task_bp = Blueprint('task', __name__)

@task_bp.route('/view_task')
def view_task():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    tasks = Task.query.all()
    return render_template("tasks.html", tasks = tasks)



@task_bp.route('/add_task', methods=["POST", "GET"])
def add_task():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    task_title = request.form.get('html_task_title')
    deadline_str = request.form.get('deadline')
    deadline = None
    if deadline_str:
        # Converting the browser’s input to a datetime object
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        deadline = deadline.replace(tzinfo=ZoneInfo("Asia/Kolkata")).astimezone(timezone.utc)



    if task_title:
        new_task_title = Task(db_task_title=task_title, status="Pending", deadline=deadline)
        db.session.add(new_task_title)
        db.session.commit()
        flash('Task added succesfully', 'seccess')

    return redirect(url_for("task.view_task"))




@task_bp.route('/toggle_status/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    
    task = Task.query.get(task_id)
    
    # Debug: Check if task exists
    if not task:
        print(f"ERROR: Task with ID {task_id} not found in database!")
        flash(f"Task with ID {task_id} not found in database!")
        return redirect(url_for('task.view_task'))
    
    # print(f"Found task: ID={task.id}, Title={task.db_task_title}, Current Status={task.status}")
    # flash(f"Status toggled for task ID: {task_id}")
    
    
    # Toggle the status
    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Completed'
    elif task.status == 'Completed':
        flash("Once the task is completed, you can not edit it anymore")
    

    completed_time_str = request.form.get('clicked_time')
    if completed_time_str:
        completed_by = datetime.fromisoformat(completed_time_str.replace('Z', '+00:00'))
    else:
        completed_by = datetime.now(timezone.utc)

    # Ensure both times are timezone-aware UTC
    if completed_by.tzinfo is None:
        completed_by = completed_by.replace(tzinfo=timezone.utc)

    if task.deadline:
        if task.deadline.tzinfo is None:
            task.deadline = task.deadline.replace(tzinfo=timezone.utc)

        time_diff = task.deadline - completed_by
        seconds = int(time_diff.total_seconds())
        abs_seconds = abs(seconds)
        minutes = abs_seconds // 60
        hours = minutes // 60
        days = hours // 24

        remaining = f"{days}d {hours%24}h {minutes%60}m left before deadline."


        if task.status == 'Completed':  
            if seconds > 0:
                task.deadline_status = 'Completed by Time'
            elif seconds < 0:
                task.deadline_status = 'Completed Late'
            elif seconds == 0:
                task.deadline_status = 'Completed on Time'

        elif task.status == 'Pending':
            flash(f"Remainings days {remaining}!")
            
        elif task.status == 'Working':
            flash(f"Remainings days {remaining}!")
                
            
                
    elif not task.deadline:
        if task.status == 'Completed':  
            task.deadline_status = 'Completed by any Time'
        elif task.status == 'Working': 
            flash("No Deadlines are added ")
            task.deadline_status = 'No Deadlines Added'
        elif task.status == 'Pending':
                flash("No Deadlines are added ")
                task.deadline_status = 'No Deadlines Added'
    
    try:
        db.session.commit()
        print("Database commit successful")
        # flash(f"task_id is = {task_id} and task.id is {task.id} task status is {task.status}")
    except Exception as e:
        print(f"Database commit failed: {e}")
        flash(f"Error updating task: {e}")
        db.session.rollback()

    return redirect(url_for('task.view_task'))


@task_bp.route('/clear_tasks', methods=["POST"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash("All tasks are cleared!", 'info')
    return redirect(url_for('task.view_task'))


@task_bp.route('/delete_task', methods=["GET", "POST"])
def delete_task():
    ids = request.form.getlist("task_ids[]")
    for t in ids:
        select_task = Task.query.get(t)
        if select_task:
            db.session.delete(select_task)
    db.session.commit()
    return redirect(url_for("task.view_task"))