from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True)

# To delete if not used python-dateutil, pyparsing, pillow, packaging, numpy, kiwisolver, fonttools, cycler, contourpy, matplotlib