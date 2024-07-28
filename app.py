from flask import render_template
from application import create_app

app = create_app()

#search widget for navbar
@app.context_processor
def base():
    from application.form import SeachForm
    form = SeachForm()
    return dict(search_form = form)

if __name__ == "__main__":
    app.run(debug = True)