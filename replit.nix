{ pkgs }: {
  deps = [
    pkgs.speedtest_cli
    pkgs.hello
    pkgs.sudo
    pkgs.wrangler
    pkgs.openssh_with_kerberos
    pkgs.minify
    pkgs.gh
    pkgs.sass
    pkgs.sass
    pkgs.nodejs-16_x
    pkgs.python38Full
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      # Needed for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
      # Needed for matplotlib
      pkgs.xorg.libX11
    ];
    PYTHONBIN = "${pkgs.python38Full}/bin/python3.8";
    LANG = "en_US.UTF-8";
  };
}