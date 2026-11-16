cask "knocker-gnome" do
  version "b978a04bdd77208cb4a59a371e558d41a232859b"
  sha256 "2a1365b80c3a771b2c1ac68cb66f187d590eb3c4db6fcfdfd52275364e6a2bf6"

  url "https://github.com/FarisZR/knocker-gnome/releases/download/build-b978a04bdd77208cb4a59a371e558d41a232859b/knocker-gnome.tar.gz"
  name "Knocker GNOME Extension"
  desc "GNOME Quick Settings for the Knocker port knocking service"
  homepage "https://github.com/FarisZR/knocker-gnome"

  depends_on :linux

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
