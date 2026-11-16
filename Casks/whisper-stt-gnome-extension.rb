cask "whisper-stt-gnome-extension" do
  version "c15803bd4f22bb025b5e25e58fb2179b3c8e492a"
  sha256 "9a691aae5dc2311325e93f068062f334d1afd0f370b883dd0f7ba0ff2082f2a7"

  url "https://github.com/FarisZR/whisper-stt-gnome-extension/releases/download/build-c15803bd4f22bb025b5e25e58fb2179b3c8e492a/whisper-stt-gnome-extension.tar.gz"
  name "Whisper STT GNOME Extension"
  desc "GNOME dictation using an OpenAI-compatible speech-to-text endpoint"
  homepage "https://github.com/FarisZR/whisper-stt-gnome-extension"

  depends_on :linux

  artifact "whisper-stt@fariszr.com",
           target: "~/.local/share/gnome-shell/extensions/whisper-stt@fariszr.com"

  caveats <<~EOS
    Requires GNOME Shell 49 or 50, GStreamer tools/plugins (including pulseaudio),
    curl, and libcanberra's canberra-gtk-play for notification sounds.
    Log out and back in, then enable the extension:
      gnome-extensions enable whisper-stt@fariszr.com
    Configure your transcription endpoint in:
      gnome-extensions prefs whisper-stt@fariszr.com
    After upgrading, log out and back in to load the new build.
  EOS
end
