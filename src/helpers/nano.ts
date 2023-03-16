import NanoClient from 'nano-node-rpc';

export default new NanoClient({
    apiKey: process.env.NANO_API,
})