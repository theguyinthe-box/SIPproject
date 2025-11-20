#! bin/bash
apt install -y curl unzip npm
curl -fsSL https://fnm.vercel.app/install | bash
~/.local/share/fnm/fnm install 24
npm install --prefix ./SIP-GUI/