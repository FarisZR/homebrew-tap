cask "komodo-agentic-cli" do
  arch arm: "aarch64", intel: "x86_64"

  version "2.3.3-agentic"
  sha256 arm64_linux:  "80b2569b0edc559ae262f1733c8e067aa52454ac96f1fdd5e09bf43b1765986f",
         x86_64_linux: "6b10af9b45ecce0f047919c0d130bce6c1c26bfde90284ca83dc847b7369ddfb"

  url "https://github.com/FarisZR/komodo-agentic-cli/releases/download/v2.3.3-agentic/km-#{arch}"
  name "Komodo Agentic CLI"
  desc "Agent-oriented CLI for Komodo deployment management"
  homepage "https://github.com/FarisZR/komodo-agentic-cli"

  depends_on :linux
  container type: :naked

  binary "km-#{arch}", target: "km"
end
