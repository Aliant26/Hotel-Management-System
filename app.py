from views.login import LoginApp
from models.users import init_users_db

init_users_db()

app = LoginApp()
app.mainloop()