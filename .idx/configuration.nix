programs.nix-ld.enable = true;
programs.nix-ld.libraries = with pkgs; [
    pkgs.uv
];