cask "jabra-gnome-integration" do
  version "1d4808e0e67cac78357b9ca8af1dfc3b59ca5e69"
  sha256 "b359317c475a344d200a0d86ed35ea2203c18052a9f2e694b1de891cc6d0631a"

  url "https://github.com/FarisZR/jabra-gnome-integration/releases/download/build-1d4808e0e67cac78357b9ca8af1dfc3b59ca5e69/jabra-gnome-integration.tar.gz"
  name "Jabra GNOME Integration"
  desc "Jabra headset auto-connect and pause-on-disconnect for GNOME"
  homepage "https://github.com/FarisZR/jabra-gnome-integration"

  depends_on :linux

  artifact "jabra-integration@fariszr.com",
           target: "~/.local/share/gnome-shell/extensions/jabra-integration@fariszr.com"

  caveats <<~EOS
    Requires GNOME Shell 48/49/50/51 and a configured jabridge user service.
    Install jabridge and run jabridge setup before enabling the extension.
    Configure settings with gsettings; see the project README for commands.
    Log out and back in, then enable the extension:
      gnome-extensions enable jabra-integration@fariszr.com
    After upgrading, log out and back in to load the new build.
  EOS
end
