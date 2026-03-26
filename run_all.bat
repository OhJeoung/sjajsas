cd /d C:\Users\Admin\Desktop\개발

start cmd /k python main.py
timeout /t 3
start http://localhost:8501
start cmd /k python -m streamlit run dashboard.py