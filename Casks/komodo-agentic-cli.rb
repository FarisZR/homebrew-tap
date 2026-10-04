cask "komodo-agentic-cli" do
  arch arm: "aarch64", intel: "x86_64"

  version "2.2.0-agentic"
  sha256 arm64_linux:  "61ad942eae8089ba6c2d94ab137f572fc268a54dd5de4325f7d25f49a584d33c",
         x86_64_linux: "0d90be8257a8fbb08287ab76d00328704f97d5d179223bea5b52c517c9f6e782"

  url "https://github.com/FarisZR/komodo-agentic-cli/releases/download/v2.2.0-agentic/km-#{arch}"
  name "Komodo Agentic CLI"
  desc "Agent-oriented CLI for Komodo deployment management"
  homepage "https://github.com/FarisZR/komodo-agentic-cli"

  depends_on :linux
  container type: :naked

  binary "km-#{arch}", target: "km"
end
