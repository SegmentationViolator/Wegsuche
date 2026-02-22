{
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
        flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { nixpkgs, flake-utils, ... }:
        flake-utils.lib.eachDefaultSystem (system:
            let
                pkgs = import nixpkgs {
                    inherit system;
                };
            in
            {
                devShells.default =
                    pkgs.mkShell {
                        packages = with pkgs; [
                            libGL
                            glfw

                            python314
                            python314Packages.glfw
                            python314Packages.numpy
                            python314Packages.pyopengl
                            python314Packages.pyopengl-accelerate

                            ruff
                            uv
                        ];
                        shellHook = ''
                            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
                                pkgs.stdenv.cc.cc.lib
                                pkgs.glfw
                                pkgs.libGL
                            ]}
                        '';
                    };
            }
        );
}
