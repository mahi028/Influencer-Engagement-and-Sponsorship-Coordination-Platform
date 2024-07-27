from flask import render_template
from application import create_app

app = create_app()

#search widget for navbar
@app.context_processor
def base():
    from application.form import SeachForm
    form = SeachForm()
    return dict(search_form = form)

#error pages
@app.errorhandler(404)
def notFound(e):
    return render_template('uni/error_template.html', error = 404, error_msg = 'Page Not Found')
@app.errorhandler(401)
def notFound(e):
    return render_template('uni/error_template.html', error = 401, error_msg = 'You Are Not Authorised to access this page.')
@app.errorhandler(500)
def notFound(e):
    return render_template('uni/error_template.html', error = 404, error_msg = 'Internal Server Error')

if __name__ == "__main__":
    app.run(debug = True)

# To delete if not used: python-dateutil, pyparsing, pillow, packaging, numpy, kiwisolver, fonttools, cycler, contourpy, matplotlib