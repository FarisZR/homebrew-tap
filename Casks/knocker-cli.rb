cask "knocker-cli" do
  arch arm: "arm64", intel: "x86_64"

  version "1.0.0"
  sha256 arm64_linux:  "0e84761c3b39d008cfda0fd0ac66f2d566d1711f0c1d56d2bfc2015a658273ca",
         x86_64_linux: "235c9679fb6c8c2b0aa00e9d7ddf9ce588ae0562cb75633001d74fe2d6b9e2ff"

  url "https://github.com/FarisZR/knocker-cli/releases/download/v1.0.0/knocker-cli_Linux_#{arch}.tar.gz"
  name "Knocker CLI"
  desc "Keep your external IP address whitelisted"
  homepage "https://github.com/FarisZR/knocker-cli"

  depends_on :linux

  binary "knocker"
end
