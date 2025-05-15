from utils.Database.Database import Sqlite


db = Sqlite(db_name='database')


db.GenerateTable(
    "courses",
    isauto=False,
    name="TEXT NOT NULL",
    description="TEXT"
)


db.GenerateTable(
    "disciplines",
    isauto=False,
    course_id="INTEGER NOT NULL",
    name="TEXT NOT NULL",
    # FOREIGN_KEY="(course_id) REFERENCES courses(id)"
)


db.GenerateTable(
    "posts",
    isauto=False,
    discipline_id="INTEGER NOT NULL",
    title="TEXT NOT NULL",
    content="TEXT",
    author="TEXT",
    created_at="TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    # FOREIGN_KEY="(discipline_id) REFERENCES disciplines(id)"
)