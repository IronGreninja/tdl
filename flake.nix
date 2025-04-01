{
  description = "An over-engineered todolist";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    nixpkgs,
    pyproject-nix,
    ...
  }: let
    project = pyproject-nix.lib.project.loadPyproject {
      projectRoot = ./.;
    };

    pkgs = nixpkgs.legacyPackages.x86_64-linux;

    python = pkgs.python3;
  in {
    devShells.x86_64-linux.default = let
      arg = project.renderers.withPackages {inherit python;};

      pythonEnv = python.withPackages arg;
    in
      pkgs.mkShell {packages = [pythonEnv];};

    packages.x86_64-linux.default = let
      attrs = project.renderers.buildPythonPackage {inherit python;};
    in
      python.pkgs.buildPythonPackage (attrs // {env.CUSTOM_ENVVAR = "hello";});
  };
}
