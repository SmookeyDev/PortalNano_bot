import Big from 'big.js';

const toMnano = (value: number, fixed: number) => {
  const multNANO = Big('1000000000000000000000000000000');
  return Big(value).div(multNANO).toFixed(fixed).toString();
};

export default toMnano;
