cask "whisper-stt-gnome-extension" do
  version "d4048fc37740adea30b365f7d224d16f7890c55e"
  sha256 "09ede2a81c637996ee1158e80aab3b26b13582f215b04e1160a771b55e7f625f"

  url "https://github.com/FarisZR/whisper-stt-gnome-extension/releases/download/build-d4048fc37740adea30b365f7d224d16f7890c55e/whisper-stt-gnome-extension.tar.gz"
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
