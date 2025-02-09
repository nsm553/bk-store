from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Relative path
engine_relative = create_engine("sqlite:///./books.db")

# Absolute path (Unix/Mac)
engine_absolute_unix = create_engine("sqlite:///./books.db")

# Absolute path (Windows - escaped backslashes)
engine_absolute_windows_escaped = create_engine("sqlite:///./books.db")

# Absolute path (Windows - raw string)
engine_absolute_windows_raw = create_engine("sqlite:///./books.db")

# Example of executing a query
with Session(engine_relative) as session:
    result = session.execute(text("SELECT 1")).scalar()
    print(result) # Output: 1