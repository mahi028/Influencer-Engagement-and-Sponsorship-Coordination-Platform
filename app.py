from application import create_app

app = create_app()

@app.context_processor
def base():
    from application.form import SeachForm
    form = SeachForm()
    return dict(search_form = form)

if __name__ == "__main__":
    app.run(debug = True)

# To delete if not used: python-dateutil, pyparsing, pillow, packaging, numpy, kiwisolver, fonttools, cycler, contourpy, matplotlib