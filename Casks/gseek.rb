cask "gseek" do
  arch arm: "aarch64", intel: "x86_64"

  version "0.1.0"
  sha256 arm64_linux:  "dda3109cff07231b744310dbb492a7dbc8efc6adca2a4d6c4576b00ddab245f6",
         x86_64_linux: "85004aedb2eb8d20dbeae327e74d7b09359c3ca55c7563477adbc16692c95737"

  url "https://github.com/FarisZR/GSeek/releases/download/v0.1.0/gseek-linux-#{arch}.tar.gz"
  name "GSeek"
  desc "Private multilingual semantic file search for GNOME"
  homepage "https://github.com/FarisZR/GSeek"

  depends_on :linux
  depends_on formula: %w[ffmpeg poppler libarchive openssl@3]

  artifact "gseek", target: "~/.local/share/gseek-app"
  binary "#{Dir.home}/.local/share/gseek-app/bin/gseek", target: "gseek"

  # Homebrew replaces HOME and preserves desktop variables as HOMEBREW_*.
  # Give the registration command the actual user's XDG and session paths.
  integration_env = {}
  {"XDG_DATA_HOME" => ".local/share", "XDG_CONFIG_HOME" => ".config",
    "XDG_CACHE_HOME" => ".cache"}.each do |name, fallback|
    value = ENV["HOMEBREW_#{name}"] || ENV[name]
    integration_env[name] = if value && Pathname.new(value).absolute?
      value
    else
      File.join(Dir.home, fallback)
    end
  end
  %w[DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR].each do |name|
    value = ENV["HOMEBREW_#{name}"] || ENV[name]
    integration_env[name] = value if value && !value.empty?
  end
  user_paths = [File.join(Dir.home, ".local/share"),
                *integration_env.values_at("XDG_DATA_HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME")].uniq

  app_launcher = File.join(Dir.home, ".local/share/gseek-app/bin/gseek")

  postflight_steps do
    run "/usr/bin/install",
        args: ["-D", "-m", "644", "{{staged_path}}/gseek-search-provider.ini",
               "/usr/local/share/gnome-shell/search-providers/io.github.FarisZR.GSeek.ini"],
        sudo: true
    write_file "~/.local/share/gseek-app/homebrew-prefix", "{{HOMEBREW_PREFIX}}\n"
    run app_launcher,
        args: ["integrate"],
        env: integration_env,
        writable_paths: user_paths
  end

  uninstall_preflight_steps do
    run app_launcher,
        args: ["unintegrate"],
        env: integration_env,
        writable_paths: user_paths
  end

  uninstall_postflight_steps do
    remove "/usr/local/share/gnome-shell/search-providers/io.github.FarisZR.GSeek.ini", sudo: true
  end

  caveats <<~EOS
    Open GSeek from your application menu to finish setup. The model downloads
    once (865 MB). GNOME 51 is the supported desktop; your files stay local.
    GSeek can enable its provider and disable Files search during setup.
    The system search-provider registration requires administrator permission.
    Settings and the search index are preserved on upgrade and uninstall.
  EOS
end
