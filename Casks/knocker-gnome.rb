cask "knocker-gnome" do
  version "6194492be2769d0c338a844a3d1f2add75f0f344"
  sha256 "d2cd86d935eabbe61fd8292162890817ebf84d3a00312de33c48a78b17f025db"

  url "https://github.com/FarisZR/knocker-gnome/releases/download/build-6194492be2769d0c338a844a3d1f2add75f0f344/knocker-gnome.tar.gz"
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
