module.exports = {
  apps: [
    {
      name: 'PortalNano_bot',
      script: 'pnpx',
      args: 'yarn start',
      autorestart: true,
      max_memory_restart: '1G',
    },
  ],
};
