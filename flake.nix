{
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
        flake-utils.url = "github:numtide/flake-utils";
        poetry2nix.url = "github:nix-community/poetry2nix";
    };

    outputs = { self, nixpkgs, flake-utils, poetry2nix }:
        flake-utils.lib.eachDefaultSystem (system:
            let
                pkgs = import nixpkgs {
                    inherit system;
                };

                poetry2nixLib = poetry2nix.lib.mkPoetry2Nix {
                    inherit pkgs;
                };
            in
            {
                packages.default =
                    poetry2nixLib.mkPoetryApplication {
                        projectDir = self;
                    };

                devShells.default =
                    pkgs.mkShellNoCC {
                        packages = [
                            (poetry2nixLib.mkPoetryEnv {
                                projectDir = self;
                            })
                            pkgs.poetry
                        ];
                    };
            }
        );
}
