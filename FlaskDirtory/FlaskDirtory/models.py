from FlaskDirtory.main import models

db = models.session()


class BaseModel(models.Model):
    __abstract__ = True  # 抽象表为True，代表当前类为抽象类，不会被创建
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.add(self)
        db.commit()

    def delete_obj(self):
        db.delete(self)
        db.commit()


class User(BaseModel):
    """
        用户表
    """
    username = models.Column(models.String(32))
    password = models.Column(models.String(32))
    identity = models.Column(models.Integer)    # 0 学生 1 教师
    identity_id = models.Column(models.Integer, nullable=True)


class Student(BaseModel):
    """
        学员表
    """
    __tablename__ = "student"
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)  # 0 男 1 女


Stu_Cou = models.Table(
    "stu_cou",
    models.Column("id", models.Integer, primary_key=True, autoincrement=True),
    models.Column("course_id", models.Integer, models.ForeignKey("course.id")),
    models.Column("student_id", models.Integer, models.ForeignKey("student.id"))
)


class Course(BaseModel):
    """
        课程表
    """
    __tablename__ = "course"
    label = models.Column(models.String(32))
    description = models.Column(models.Text)
    to_teacher = models.relationship(
        'Teacher',  # 映射表
        backref='to_course_data'  # 反向映射字段，反向映射表通过该字段查询当前表内容
    )

    """
        总结：
        models.relationship 当前字段用于一对多或者多对多反向映射：
            第一个参数是   映射向的模型名称
                Secondary  参数 指向多对多的关系表
                backref    参数指向反向映射字段，反向映射表通过该字段查询当前表内容
                Lazy       select 访问该字段时候，加载所有的映射数据 joined  对关联的两个表students和stu_cou进行join查询 dynamic 不加载数据
    """
    to_student = models.relationship(
        "Student",
        secondary=Stu_Cou,
        backref=models.backref("to_course", lazy="dynamic"),
        lazy="dynamic"
        # select 访问该字段时候，加载所有的映射数据
        # joined  对关联的两个表students和stu_cou进行join查询
        # dynamic 不加载数据
    )


class Grade(BaseModel):
    """
        成绩表
        课程，学员关联此表
    """
    __tablename__ = "grade"
    grade = models.Column(models.Float)
    course_id = models.Column(models.Integer, models.ForeignKey("course.id"))
    student_id = models.Column(models.Integer, models.ForeignKey("student.id"))


class Attendance(BaseModel):
    """
        考勤表，记录是否请假
        学员
    """
    __tablename__ = "attendance"
    att_time = models.Column(models.DateTime)
    status = models.Column(models.Integer, default=1)  # 0 迟到 1 正常出勤 2 早退 3 请假 4 旷课
    student_id = models.Column(models.Integer, models.ForeignKey("student.id"))


class Teacher(BaseModel):
    """
        教师表
        老师与课程多对一关系
    """
    __tablename__ = "teacher"
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)
    course_id = models.Column(models.Integer, models.ForeignKey("course.id"))


