from nox import session


@session(reuse_venv=True)
def docs(session):
    session.install("jupyter-book", "sphinx-sitemap", "jupyterbook-latex")
    # we need _config.yml _toc.yml
    session.run("jb", "build", ".")
