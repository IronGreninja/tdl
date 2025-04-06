{
  description = "An over-engineered todolist";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = {
    self,
    nixpkgs,
    uv2nix,
    pyproject-nix,
    pyproject-build-systems,
    ...
  }: let
    inherit (nixpkgs) lib;

    # Load a uv workspace from a workspace root.
    workspace = uv2nix.lib.workspace.loadWorkspace {workspaceRoot = ./.;};

    # Create package overlay from workspace.
    overlay = workspace.mkPyprojectOverlay {
      # Prefer prebuilt binary wheels as a package source.
      sourcePreference = "wheel";
    };

    hacks = pkgs.callPackage pyproject-nix.build.hacks {};
    # Extend generated overlay with build fixups
    pyprojectOverrides = _final: _prev: {
      setuptools-git-versioning = hacks.nixpkgsPrebuilt {
        from = python.pkgs.setuptools-git-versioning;
      };
    };

    pkgs = nixpkgs.legacyPackages.x86_64-linux;

    # Use Python 3.12 from nixpkgs
    python = pkgs.python312;

    # Construct package set
    pythonSet =
      # Use base package set from pyproject.nix builders
      (pkgs.callPackage pyproject-nix.build.packages {
        inherit python;
      })
      .overrideScope
      (
        lib.composeManyExtensions [
          pyproject-build-systems.overlays.default
          overlay
          pyprojectOverrides
        ]
      );
  in {
    # Package a virtual environment as our main application.
    #
    # Enable no optional dependencies for production build.
    packages.x86_64-linux.default = pythonSet.mkVirtualEnv "tdl-env" workspace.deps.default;

    # Make tdl runnable with `nix run`
    apps.x86_64-linux = {
      default = {
        type = "app";
        program = "${self.packages.x86_64-linux.default}/bin/tdl";
      };
    };

    devShells.x86_64-linux = rec {
      default = impure;
      impure = pkgs.mkShell {
        packages = [
          python
          pkgs.uv
          pkgs.ruff
        ];
        env =
          {
            # Prevent uv from managing Python downloads
            UV_PYTHON_DOWNLOADS = "never";
            # Force uv to use nixpkgs Python interpreter
            UV_PYTHON = python.interpreter;
          }
          // lib.optionalAttrs pkgs.stdenv.isLinux {
            # Python libraries often load native shared objects using dlopen(3).
            # Setting LD_LIBRARY_PATH makes the dynamic library loader aware of libraries without using RPATH for lookup.
            LD_LIBRARY_PATH = lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
          };
        shellHook = ''
          unset PYTHONPATH
        '';
      };
    };
  };
}
