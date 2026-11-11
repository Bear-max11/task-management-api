import sqlite3

DATABASE_URL = "tasks.db"

conn = sqlite3.connect(DATABASE_URL)

try:
    # 暂时关闭外键检查，方便重建旧表
    conn.execute("PRAGMA foreign_keys = OFF")

    conn.execute("BEGIN")

    # 1. 创建 users 表
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            hashed_password VARCHAR(255) NOT NULL
        )
    """)

    # 2. 创建一个用于接收旧任务的初始用户
    # 密码字段使用不可登录的占位值，之后不会作为真实密码使用
    conn.execute("""
        INSERT OR IGNORE INTO users
        (id, username, email, hashed_password)
        VALUES (1, 'legacy_user', 'legacy@example.invalid',
                '!DISABLED_LEGACY_ACCOUNT!')
    """)

    # 3. 检查 tasks 表是否已经有 user_id
    columns = conn.execute(
        "PRAGMA table_info(tasks)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "user_id" not in column_names:
        # 4. 创建新结构的任务表
        conn.execute("""
            CREATE TABLE tasks_new (
                id INTEGER PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description VARCHAR(500),
                completed BOOLEAN NOT NULL DEFAULT 0,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # 5. 保留旧任务，并将它们归属给初始用户
        conn.execute("""
            INSERT INTO tasks_new
            (id, title, description, completed, user_id)
            SELECT id, title, description, completed, 1
            FROM tasks
        """)

        # 6. 用新表替换旧表
        conn.execute("DROP TABLE tasks")
        conn.execute("ALTER TABLE tasks_new RENAME TO tasks")

        # 恢复原来 id 字段的索引
        conn.execute("""
            CREATE INDEX IF NOT EXISTS ix_tasks_id
            ON tasks(id)
        """)

    conn.commit()
    print("数据库迁移成功！")

except Exception:
    conn.rollback()
    raise

finally:
    conn.execute("PRAGMA foreign_keys = ON")
    conn.close()
