# nix-shell with venv: https://nixos.org/manual/nixpkgs/stable/#how-to-consume-python-modules-using-pip-in-a-virtual-environment-like-i-am-used-to-on-other-operating-systems
{pkgs, ...}: let
  pythonPackages = pkgs.python3Packages;
in
  pkgs.mkShell {
    name = "impurePythonEnv";

    venvDir = "./.venv";

    buildInputs = [
      pythonPackages.python
      pythonPackages.venvShellHook

      pkgs.pyright
      pkgs.isort
      pkgs.black
    ];

    postVenvCreation = ''
      unset SOURCE_DATE_EPOCH
      # pip install -r requirements.txt
    '';

    # postShellHook = ''
    #   # unset SOURCE_DATE_EPOCH
    # '';
  }
