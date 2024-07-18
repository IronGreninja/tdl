{python3Packages, ...}:
python3Packages.buildPythonApplication {
  pname = "tdl";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  build-system = with python3Packages; [
    setuptools
  ];

  dependencies = [];

  meta = {
    # ...
  };
}
