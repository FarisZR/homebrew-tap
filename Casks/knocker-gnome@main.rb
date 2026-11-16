cask "knocker-gnome@main" do
  version "20570fd67a08dc5ed4e5a0553894a3f08c3c07d6"
  sha256 "69481b0b2bcecf5e8cf8105923685fac6ffec5d5df0cd91bdebff8efc793fd67"

  url "https://github.com/FarisZR/knocker-gnome/releases/download/build-20570fd67a08dc5ed4e5a0553894a3f08c3c07d6/knocker-gnome.tar.gz"
  name "Knocker GNOME Extension (main)"
  desc "GNOME Quick Settings for the Knocker port knocking service"
  homepage "https://github.com/FarisZR/knocker-gnome"

  depends_on :linux
  conflicts_with cask: "knocker-gnome"

  artifact "Knocker@fariszr.com",
           target: "~/.local/share/gnome-shell/extensions/Knocker@fariszr.com"

  caveats <<~EOS
    Requires GNOME Shell 48/49/50/51 and a configured knocker.service user unit.
    Install the CLI separately: brew install --cask fariszr/tap/knocker-cli
    Log out and back in, then enable the extension:
      gnome-extensions enable Knocker@fariszr.com
    Configure extension preferences in:
      gnome-extensions prefs Knocker@fariszr.com
    After upgrading, log out and back in to load the new build.
  EOS
end
