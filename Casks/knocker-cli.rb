cask "knocker-cli" do
  arch arm: "arm64", intel: "x86_64"

  version "1.1.0"
  sha256 arm64_linux:  "c82d82437ed027d9cf7c1e5e7b39a5f2370be28020ccb4e581dfb47f4377d02d",
         x86_64_linux: "54bbc7bac6c552b23d8ceee01f15a5053a4087d209f52e23d4793d089f369ee1"

  url "https://github.com/FarisZR/knocker-cli/releases/download/v1.1.0/knocker-cli_Linux_#{arch}.tar.gz"
  name "Knocker CLI"
  desc "Keep your external IP address whitelisted"
  homepage "https://github.com/FarisZR/knocker-cli"

  depends_on :linux

  binary "knocker"
end
