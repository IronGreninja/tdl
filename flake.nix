{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    forAllSystems = nixpkgs.lib.genAttrs ["x86_64-linux"];
  in {
    devShells = forAllSystems (system: {
      default = nixpkgs.legacyPackages.${system}.callPackage ./nix/shell.nix {};
    });
    packages = forAllSystems (system: {
      default = nixpkgs.legacyPackages.${system}.callPackage ./nix/build.nix {};
    });
  };
}
