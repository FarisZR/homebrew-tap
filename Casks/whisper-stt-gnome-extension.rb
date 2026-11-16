cask "whisper-stt-gnome-extension" do
  version "b917481ae8e32d8db98e6ff6d0bc0330f65c628c"
  sha256 "bf922a0ad99a389c512f2e4ae15744cdf036af34c636f255d741438617fa06e5"

  url "https://github.com/FarisZR/whisper-stt-gnome-extension/releases/download/build-b917481ae8e32d8db98e6ff6d0bc0330f65c628c/whisper-stt-gnome-extension.tar.gz"
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
