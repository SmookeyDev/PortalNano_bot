import config from '../config';

const checkRoot = async (user_id: number) => {
  if (config.ROOTS.includes(user_id.toString())) return true;
};

export default checkRoot;
