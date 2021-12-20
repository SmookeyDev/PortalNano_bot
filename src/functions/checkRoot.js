require('../../.env')

const checkRoot = async (user_id) => {
    if(ROOTS.includes(user_id)) return true;
}; 

module.exports = checkRoot