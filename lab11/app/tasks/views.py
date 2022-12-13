from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import User, navs, footer_l_get
from app.tasks import todo_bp
from app.tasks.forms import TaskForm, CategoryForm, CommentForm, TaskDetailForm
from app.tasks.models import Task, Category, Comment


@todo_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False

    form = TaskForm()

    if request.method == 'GET':
        return render_template('createTask.html',
                               log_in=log_in,
                               form=form,
                               footer_l=footer_l_get(),
                               navs=navs)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data
        category = form.category.data
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         progress=progress,
                         category_id=category,
                         owner_id=current_user.get_id())
        task_info.users.append(current_user)
        db.session.add(task_info)
        db.session.commit()

        flash(f"Task successfully added", category='success')
        return redirect(url_for("task.create_task"))

    flash("Incorrect input data", category='warning')
    return redirect(url_for("task.create_task"))




@todo_bp.route('/<int:task_id>', methods=['GET'])
@login_required
def detail_task(task_id):
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False

    task = Task.query.filter_by(id=task_id).first()
    task_detail = {
        'Title': task.title,
        'Description': task.description,
        'Created': task.created,
        'Modified': task.modified,
        'Deadline': task.deadline.date(),
        'Priority': task.priority,
        'Progress': task.progress
    }
    form = TaskForm()
    form2 = TaskDetailForm()
    form_comment = CommentForm()
    comments = Comment.query.filter_by(task_id=task_id).all()

    data = {
        'form_comment': form_comment,
        'comments': comments,
        'User': User
    }
    return render_template('detailTask.html',
                           task_detail=task_detail,
                           log_in=log_in,
                           task_id=task.id,
                           form=form,
                           form2=form2,
                           assigned=task.users,
                           data=data,
                           footer_l=footer_l_get(),
                           navs=navs)


@todo_bp.route('/', methods=['GET'])
@login_required
def list_task():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False

    task_list = current_user.tasks
    task_list = task_list.order_by(Task.priority.desc())
    task_list = task_list.order_by(Task.deadline.asc())
    # task_list = Task.query.filter(Task.users.any(id=current_user.id)).all()
    # print(type(task_list[0].owner_id))
    return render_template('listTask.html',
                           task_list=task_list,
                           log_in=log_in,
                           footer_l=footer_l_get(),
                           navs=navs)


@todo_bp.route('/<int:task_id>/assign/user', methods=['POST'])
@login_required
def assign_user_task(task_id):

    form = TaskDetailForm()

    task = Task.query.filter_by(id=task_id).first()

    if task.owner_id != current_user.id:
        flash("You cannot assign users to this task", category='warning')
        return redirect(url_for("task.detail_task", task_id=task_id))
    if not request.form.get('email'):
        flash("Fill the email field", category='warning')
        return redirect(url_for("task.detail_task", task_id=task_id))
    user_id = form.email.data

    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("No user with such email", category='warning')
        return redirect(url_for("task.detail_task", task_id=task_id))
    task.users.append(user)
    db.session.add(task)
    db.session.commit()
    flash("Successfully assigned user", category='success')
    return redirect(url_for("task.detail_task", task_id=task_id))


@todo_bp.route('/<int:task_id>/discard/user', methods=['POST'])
@login_required
def discard_user_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.owner_id != current_user.id:
        flash("You cannot discard users from this task", category='warning')
        return redirect(url_for("task.detail_task", task_id=task_id))
    user = User.query.filter_by(id=request.form.get('user_id')).first()
    task.users.remove(user)
    db.session.add(task)
    db.session.commit()
    flash("Successfully discarded user", category='success')
    return redirect(url_for("task.detail_task", task_id=task_id))


@todo_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data

        task = Task.query.filter_by(id=task_id).first()
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        flash(f"Task successfully updated", category='success')
        return redirect(url_for("task.detail_task", task_id=task_id))
    print(form.errors, form.description.data)
    flash("Incorrect input data", category='warning')
    return redirect(url_for("task.detail_task", task_id=task_id))


@todo_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    flash("Successfully deleted!", category='success')
    return redirect(url_for("task.list_task"))


@todo_bp.route('/category/', methods=['GET'])
@login_required
def list_category():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False
    cat_list = Category.query.all()
    return render_template('listCategory.html',
                           cat_list=cat_list,
                           log_in=log_in,
                           footer_l=footer_l_get(),
                           navs=navs)


@todo_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def create_category():
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False

    form = CategoryForm()
    if request.method == 'GET':
        return render_template('createCategory.html',
                               log_in=log_in,
                               form=form,
                               footer_l=footer_l_get(),
                               navs=navs)

    if form.validate_on_submit():
        name = form.name.data
        cat_info = Category(name=name)
        db.session.add(cat_info)
        db.session.commit()

        flash(f"Category successfully added", category='success')
        return redirect(url_for("task.create_category"))

    flash("Incorrect input data", category='warning')
    return redirect(url_for("task.create_category"))


@todo_bp.route('/category/<int:cat_id>', methods=['GET'])
@login_required
def detail_category(cat_id):
    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=current_user.get_id()).first()
    else:
        log_in = False

    cat = Category.query.filter_by(id=cat_id).first()
    cat_detail = {
        'Category': cat.name,
    }
    form = CategoryForm()
    return render_template('detailCategory.html',
                           log_in=log_in,
                           cat_detail=cat_detail,
                           cat_id=cat.id,
                           form=form,
                           footer_l=footer_l_get(),
                           navs=navs)


@todo_bp.route('/category/<int:cat_id>/update', methods=['POST'])
@login_required
def update_category(cat_id):
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data

        cat = Category.query.filter_by(id=cat_id).first()
        cat.name = name
        db.session.add(cat)
        db.session.commit()

        flash(f"Category successfully updated", category='success')
        return redirect(url_for("task.detail_category", cat_id=cat_id))

    flash("Incorrect input data", category='warning')
    return redirect(url_for("task.detail_category", cat_id=cat_id))


@todo_bp.route('/category/<int:cat_id>/delete', methods=['POST'])
@login_required
def delete_category(cat_id):
    cat = Category.query.filter_by(id=cat_id).first()
    db.session.delete(cat)
    db.session.commit()
    flash("Successfully deleted!", category='success')
    return redirect(url_for("task.list_category"))


@todo_bp.route('/user/profile')
@login_required
def user_profile():
    user_id = current_user.get_id()

    if current_user.is_authenticated:
        log_in = User.query.filter_by(id=user_id).first()
        task_list = log_in.tasks
    else:
        log_in = False

    return render_template('user_account.html',
                           log_in=log_in,
                           navs=navs,
                           task_list=task_list)


@todo_bp.route('/add_comment/<int:task_id>', methods=['POST'])
@login_required
def add_comment(task_id):
    task = current_user.tasks.filter_by(id=task_id).first()
    if not task:
        flash("You cannot add comment to this task", category='warning')
        return redirect(url_for("task.detail_task", task_id=task_id))
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(text=text,
                          owner_id=current_user.id,
                          task_id=task_id)
        db.session.add(comment)
        db.session.commit()

        flash(f"Comment successfully added", category='success')
        return redirect(url_for("task.detail_task", task_id=task_id))

    flash("Incorrect input data", category='warning')
    return redirect(url_for("task.detail_task", task_id=task_id))
