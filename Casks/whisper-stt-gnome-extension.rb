cask "whisper-stt-gnome-extension" do
  version "1ef737692a36fd435e4fb68f74f5987d71699abb"
  sha256 "09d7b042833f56d226b1b51abcb96f1495953fbe515ffdc5ef546ee8776fdf5c"

  url "https://github.com/FarisZR/whisper-stt-gnome-extension/releases/download/build-1ef737692a36fd435e4fb68f74f5987d71699abb/whisper-stt-gnome-extension.tar.gz"
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
