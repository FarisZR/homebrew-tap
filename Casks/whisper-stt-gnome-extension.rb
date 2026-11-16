cask "whisper-stt-gnome-extension" do
  version "16c654b34d8d77a1f8e75ae300d9328a70a9822f"
  sha256 "8ddf8f6540d9790ede5821ee6c4e93235dd5d0d5b03791c7d4039f2712f7b899"

  url "https://github.com/FarisZR/whisper-stt-gnome-extension/releases/download/build-16c654b34d8d77a1f8e75ae300d9328a70a9822f/whisper-stt-gnome-extension.tar.gz"
  name "Whisper STT GNOME Extension"
  desc "GNOME dictation using an OpenAI-compatible speech-to-text endpoint"
  homepage "https://github.com/FarisZR/whisper-stt-gnome-extension"

  depends_on :linux

  artifact "whisper-stt@fariszr.com",
           target: "~/.local/share/gnome-shell/extensions/whisper-stt@fariszr.com"

  caveats <<~EOS
    Requires GNOME Shell 49/50/51, GStreamer tools/plugins (including pulseaudio),
    curl, and libcanberra's canberra-gtk-play for notification sounds.
    Log out and back in, then enable the extension:
      gnome-extensions enable whisper-stt@fariszr.com
    Configure your transcription endpoint in:
      gnome-extensions prefs whisper-stt@fariszr.com
    After upgrading, log out and back in to load the new build.
  EOS
end
