const checkRoot = async (user_id: number) => {
    const ROOTS = process.env.ROOTS || "";

    if(ROOTS.includes(user_id.toString())) return true;
}; 

export default checkRoot