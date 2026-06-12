import aiosqlite

DB_NAME = "users.sql"
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            age INTEGER
            )
        """)
        await db.commit()
    
async def add_user(full_name: str, age: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO users (full_name, age) VALUES (?, ?)",
            (full_name, age)
        )
        await db.commit()
    
async def get_user(full_name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE full_name = ?",
            (full_name,)
        )
        return await cursor.fetchone()
    
    
async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users"
        )
        return await cursor.fetchall()