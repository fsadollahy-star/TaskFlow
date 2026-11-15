
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Database configuration
DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Database model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String(20), default="medium")


# Create database tables
Base.metadata.create_all(bind=engine)


# Pydantic schemas
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    completed: bool = False
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None
    priority: str | None = Field(default=None, pattern="^(low|medium|high)$")


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    priority: str


# FastAPI application
app = FastAPI(
    title="TaskFlow API",
    description="Professional Task Management REST API",
    version="1.0.0"
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# CREATE
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**data.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# READ ALL
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.desc()).all()


# READ ONE
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# UPDATE
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
