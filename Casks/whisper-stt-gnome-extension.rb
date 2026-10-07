cask "whisper-stt-gnome-extension" do
  version "90e5463fcba843e8f3cf2cf93e882cd9e723a284"
  sha256 "e0bc793fef5ee4b38506e53313305d5ffa78b1821c9f7370de701ed2e64cc600"

  url "https://github.com/FarisZR/whisper-stt-gnome-extension/releases/download/build-90e5463fcba843e8f3cf2cf93e882cd9e723a284/whisper-stt-gnome-extension.tar.gz"
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
