import os
import pandas as pd
from datetime import datetime, timedelta

class TodoManager:
    def __init__(self, csv_file="todos.csv"):
        self.csv_file = csv_file
        self.columns = ["id", "task", "description", "due_date", "due_time", "status", "created_at"]
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        """Create CSV file if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.csv_file, index=False)

    def load_todos(self):
        """Load todos from CSV file"""
        try:
            return pd.read_csv(self.csv_file)
        except Exception as e:
            print(f"Error loading todos: {e}")
            return pd.DataFrame(columns=self.columns)

    def save_todos(self, df) -> bool:
        """Save todos to CSV file"""
        try:
            df.to_csv(self.csv_file, index=False)
            return True
        except Exception as e:
            print(f"Error saving todos: {e}")
            return False

    def add_todo(self, task, description, due_date, due_time) -> int:
        """Add a new todo item"""
        df = self.load_todos()
        new_id = len(df) + 1 if len(df) > 0 else 1

        new_todo = {
            "id": new_id,
            "task": task,
            "description": description,
            "due_date": due_date,
            "due_time": due_time,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.concat([df, pd.DataFrame([new_todo])], ignore_index=True)
        if self.save_todos(df):
            return int(new_id)
        return -1

    def list_todos(self, status=None) -> str:
        """List todos, optionally filtered by status"""
        df = self.load_todos()
        if df.empty:
            return "No todos found"

        if status:
            df = df[df['status'] == status]

        return df.to_string(index=False)

    def complete_todo(self, todo_id) -> str:
        """Mark a todo as completed"""
        df = self.load_todos()
        if todo_id in df['id'].values:
            df.loc[df['id'] == todo_id, 'status'] = 'completed'
            if self.save_todos(df):
                return f"Todo with ID {todo_id} marked as completed"
        return f"Todo with ID {todo_id} not found"

    def delete_todo(self, todo_id) -> str:
        """Delete a todo"""
        df = self.load_todos()
        if todo_id in df['id'].values:
            df = df[df['id'] != todo_id]
            if self.save_todos(df):
                return f"Todo with ID {todo_id} deleted successfully"
        return f"Todo with ID {todo_id} not found"

    def get_upcoming_todos(self):
        """Get todos due within the next 24 hours"""
        df = self.load_todos()
        if df.empty:
            return []

        upcoming = []
        now = datetime.now()

        for _, todo in df.iterrows():
            if todo['status'] == 'pending':
                try:
                    due_datetime = datetime.strptime(f"{todo['due_date']} {todo['due_time']}", "%Y-%m-%d %H:%M")
                    time_diff = due_datetime - now

                    # Check if due within 24 hours
                    if time_diff < timedelta(hours=24):
                        upcoming.append(todo)
                except Exception as e:
                    print(f"Error parsing date for todo {todo['id']}: {e}")

        return upcoming