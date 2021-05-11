# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

# new_row = Table(task='Nothing to do!', deadline=datetime.strptime('04-09-2021', '%m-%d-%Y').date())
# session.add(new_row)
# session.add(Table(task='Visit an orphanage', deadline=datetime.today()))
# session.add(Table(task='Analyze New product consumer-reception', deadline=datetime.today()))
# session.add(Table(task='Visit an Ethiopia', deadline=datetime.today() + timedelta(days=2)))
# session.commit()

rows = session.query(Table).all()
today = datetime.today()
for_today_rows = session.query(Table).filter(Table.deadline == today.date()).all()
ordered_rows = session.query(Table).order_by(Table.deadline).all()
tomorrow = datetime.today() + timedelta(days=1)
delete_today = session.query(Table).filter(Table.deadline == datetime.today().date()).delete()
specific_rows_past_task = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()


# print(first_row.task)

def weeks_task():
    dl = today.date()
    for n_day in range(7):
        tasks = session.query(Table).filter(Table.deadline == dl).all()
        # print(tasks)
        if not tasks:
            print(f"{dl.strftime('%A %#d %b')}:")
            print("Nothing to do!")
            print()
        else:
            print(f"{dl.strftime('%A %#d %b')}:")
            sn = 1
            for todo in tasks:
                task_to_do = todo.task
                print(f"{sn}. {task_to_do}")
                sn += 1
            print()

        dl += timedelta(days=1)


def all_task():
    everything_todo = session.query(Table).order_by(Table.deadline).all()
    sn = 0
    for i in everything_todo:
        sn += 1
        time_frame_day = i.deadline.day
        time_frame_month = i.deadline.strftime('%b')
        time_frame = str(f'{time_frame_day} {time_frame_month}')
        print(f'{sn}. {i}. {time_frame}')


def delete_task():
    rows_to_delete = session.query(Table).all()
    to_delete = session.query(Table).filter(Table.deadline).all()
    sn = 0
    if len(to_delete) > 0:
        for i in rows_to_delete:
            sn += 1
            print(f'{sn}. {i}.', i.deadline.strftime('%#d %b'))
        selected = int(input("> "))
        deleted = rows_to_delete[selected - 1]
        print(deleted)
        session.delete(deleted)
        session.commit()
        print("The task has been deleted!")
    else:
        print("Nothing to delete")
    session.commit()


def missed_task():
    session.commit()
    task_missed = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    sn = 0
    for i in task_missed:
        sn += 1
        i_day = i.deadline.day
        i_month = i.deadline.strftime('%b')
        print(f'{sn}. {i}. {i_day} {i_month}')


def selection():
    session.commit()
    today_task = for_today_rows
    menu = ["1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit"]
    for option in menu:
        print(f'{option}')
    selected = int(input("enter an option "))

    if selected == 6:
        session.commit()
        print("\n")
        print("Choose the number of the task your want to delete:\n")
        delete_task()
        session.commit()
        print("\n")
        selection()

    if selected == 5:
        print("\n")
        print("Enter task")
        new_row = Table(task=input("> "),
                        deadline=datetime.strptime(input('Enter deadline\n>'), '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added")
        print("\n")
        selection()

    if selected == 4:
        session.commit()
        print("\n")
        print("Missed task:")
        missed_task()
        print("\n")
        selection()

    if selected == 3:
        print("\n")
        print("All tasks:")
        all_task()
        print("\n")
        selection()

    if selected == 2:
        print('\n')
        weeks_task()
        selection()
        # print(all_task())

    if selected == 1 and len(rows) > 1:
        print("\n")

        time_frame_day = datetime.today().day
        time_frame_month = datetime.today().strftime('%b')
        today_date = str(f'Today {time_frame_day} {time_frame_month}:')
        print(today_date)
        for i in today_task:
            print(i)
        print("Nothing to do")
        # print(new_row.task)
        print("\n")
        selection()

    elif selected == 1 and len(today_task) <= 0:
        print("\n")
        print("Today:")
        print('Nothing to do!')
        print("\n")
        selection()

    else:
        print("\n")
        print("Bye!")
    session.commit()


selection()
