with import <nixpkgs> {};

let python = python36Packages;
in stdenv.mkDerivation {
    name = "dev";
    shellHook = "source venv/bin/activate";
    buildInputs = [ python.pip ];
}
